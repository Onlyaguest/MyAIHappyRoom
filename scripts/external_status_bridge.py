#!/usr/bin/env python3
"""Generic external status bridge for HappyRoom.

Push external agent states to /agent-push using a configurable source.
Supports:
- source.type = "command"
- source.type = "json_file"
- source.type = "http_json"

Examples:
  python3 scripts/external_status_bridge.py \
    --config scripts/external_status_bridge.command.sample.json \
    --join-key YOUR_JOIN_KEY \
    --office-url http://127.0.0.1:19000

  python3 scripts/external_status_bridge.py \
    --config scripts/external_status_bridge.file.sample.json \
    --join-key YOUR_JOIN_KEY \
    --dry-run --once
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

VALID_STATES = {"idle", "writing", "researching", "executing", "syncing", "error", "offline"}


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    print(f"[{now()}] {msg}", flush=True)


def short_text(value: str, limit: int = 120) -> str:
    text = (value or "").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def normalize_state(state: str) -> str:
    s = (state or "").strip().lower()
    aliases = {
        "busy": "writing",
        "working": "writing",
        "write": "writing",
        "run": "executing",
        "running": "executing",
        "exec": "executing",
        "thinking": "researching",
        "research": "researching",
        "search": "researching",
        "sync": "syncing",
        "failed": "error",
        "dead": "error",
    }
    s = aliases.get(s, s)
    return s if s in VALID_STATES else "idle"


def map_state_from_text(raw: str, state_map: dict[str, str], default_state: str) -> str:
    text = (raw or "").lower()
    for key, target in state_map.items():
        if key.lower() in text:
            return normalize_state(target)

    # Generic heuristics when explicit map misses
    if any(k in text for k in ["error", "dead", "failed", "异常", "报错", "bug"]):
        return "error"
    if any(k in text for k in ["sync", "同步"]):
        return "syncing"
    if any(k in text for k in ["research", "thinking", "调研", "搜索"]):
        return "researching"
    if any(k in text for k in ["exec", "run", "busy", "work", "执行", "推进", "处理中"]):
        return "writing"
    if any(k in text for k in ["idle", "done", "待命", "完成"]):
        return "idle"
    return normalize_state(default_state)


@dataclass
class AgentSpec:
    agent_id: str
    name: str
    crew: str
    agent: str
    source_key: str
    detail_template: str


def extract_snapshot_from_data(data: Any, agent: AgentSpec) -> dict[str, str]:
    # Shape A: dict keyed by source_key/agent_id/name
    if isinstance(data, dict):
        obj = data.get(agent.source_key) or data.get(agent.agent_id) or data.get(agent.name)
        if isinstance(obj, dict):
            return {
                "raw": json.dumps(obj, ensure_ascii=False),
                "state": str(obj.get("state", "") or ""),
                "detail": str(obj.get("detail", "") or obj.get("message", "") or ""),
            }

    # Shape B: list of objects
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            key = str(item.get("sourceKey", "") or item.get("agentId", "") or item.get("name", ""))
            crew = str(item.get("crew", ""))
            ag = str(item.get("agent", ""))
            if key in {agent.source_key, agent.agent_id, agent.name} or (crew == agent.crew and ag == agent.agent):
                return {
                    "raw": json.dumps(item, ensure_ascii=False),
                    "state": str(item.get("state", "") or ""),
                    "detail": str(item.get("detail", "") or item.get("message", "") or ""),
                }

    return {"raw": "", "state": "", "detail": ""}


class CommandSource:
    def __init__(self, conf: dict[str, Any]) -> None:
        self.command = str(conf.get("command", "")).strip()
        self.cwd = os.path.expanduser(str(conf.get("cwd", "") or "")) or None
        self.timeout_sec = int(conf.get("timeoutSec", 12))
        self.line_filter_template = str(conf.get("lineFilter", "")).strip()
        self.parse_regex = str(conf.get("parseRegex", "")).strip()
        if not self.command:
            raise ValueError("source.command is required for command source")

    def _run_command(self, agent: AgentSpec) -> str:
        fmt = {
            "crew": agent.crew,
            "agent": agent.agent,
            "agentId": agent.agent_id,
            "name": agent.name,
            "sourceKey": agent.source_key,
        }
        cmd = self.command.format(**fmt)
        proc = subprocess.run(
            shlex.split(cmd),
            cwd=self.cwd,
            capture_output=True,
            text=True,
            timeout=self.timeout_sec,
            check=False,
        )
        out = (proc.stdout or "")
        err = (proc.stderr or "")
        merged = (out + "\n" + err).strip()
        return merged

    def get_snapshot(self, agent: AgentSpec) -> dict[str, str]:
        raw = self._run_command(agent)
        selected = raw

        if self.line_filter_template:
            token = self.line_filter_template.format(
                crew=agent.crew,
                agent=agent.agent,
                agentId=agent.agent_id,
                name=agent.name,
                sourceKey=agent.source_key,
            )
            lines = [ln for ln in raw.splitlines() if token in ln]
            if lines:
                selected = lines[0]

        state = ""
        detail = ""
        if self.parse_regex:
            m = re.search(self.parse_regex, selected)
            if m:
                state = (m.groupdict().get("state") or "").strip()
                detail = (m.groupdict().get("detail") or "").strip()

        return {
            "raw": selected,
            "state": state,
            "detail": detail,
        }


class JsonFileSource:
    def __init__(self, conf: dict[str, Any]) -> None:
        self.path = os.path.expanduser(str(conf.get("path", "")).strip())
        if not self.path:
            raise ValueError("source.path is required for json_file source")

    def _load(self) -> Any:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_snapshot(self, agent: AgentSpec) -> dict[str, str]:
        data = self._load()
        return extract_snapshot_from_data(data, agent)


class HttpJsonSource:
    def __init__(self, conf: dict[str, Any]) -> None:
        self.url = str(conf.get("url", "")).strip()
        self.method = str(conf.get("method", "GET")).strip().upper() or "GET"
        self.timeout_sec = int(conf.get("timeoutSec", 10))
        self.body = conf.get("body")
        self.headers = conf.get("headers") or {}
        if not isinstance(self.headers, dict):
            self.headers = {}
        if not self.url:
            raise ValueError("source.url is required for http_json source")

    def _fetch(self) -> Any:
        kwargs: dict[str, Any] = {
            "method": self.method,
            "url": self.url,
            "timeout": self.timeout_sec,
            "headers": {str(k): str(v) for k, v in self.headers.items()},
        }
        if self.body is not None:
            kwargs["json"] = self.body
        resp = requests.request(**kwargs)
        resp.raise_for_status()
        return resp.json()

    def get_snapshot(self, agent: AgentSpec) -> dict[str, str]:
        data = self._fetch()
        return extract_snapshot_from_data(data, agent)


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        conf = json.load(f)
    if not isinstance(conf, dict):
        raise ValueError("config must be a JSON object")
    return conf


def build_agents(conf: dict[str, Any]) -> list[AgentSpec]:
    arr = conf.get("agents")
    if not isinstance(arr, list) or not arr:
        raise ValueError("config.agents must be a non-empty array")

    agents: list[AgentSpec] = []
    for i, obj in enumerate(arr):
        if not isinstance(obj, dict):
            raise ValueError(f"agents[{i}] must be object")
        agent_id = str(obj.get("agentId", "")).strip()
        name = str(obj.get("name", "")).strip()
        crew = str(obj.get("crew", "")).strip()
        agent = str(obj.get("agent", "")).strip()
        if not agent_id or not name:
            raise ValueError(f"agents[{i}] missing agentId/name")

        source_key = str(obj.get("sourceKey", "")).strip() or f"{crew}.{agent}" if crew or agent else agent_id
        detail_template = str(obj.get("detailTemplate", "{name} | {state}"))
        agents.append(
            AgentSpec(
                agent_id=agent_id,
                name=name,
                crew=crew,
                agent=agent,
                source_key=source_key,
                detail_template=detail_template,
            )
        )
    return agents


def push_agent(
    office_url: str,
    join_key: str,
    agent: AgentSpec,
    state: str,
    detail: str,
    timeout_sec: int,
    max_retries: int,
    retry_backoff_sec: float,
) -> bool:
    url = office_url.rstrip("/") + "/agent-push"
    payload = {
        "agentId": agent.agent_id,
        "joinKey": join_key,
        "state": state,
        "detail": detail,
        "name": agent.name,
    }

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout_sec)
            data: dict[str, Any] = {}
            try:
                data = resp.json() if resp.text else {}
            except Exception:
                data = {"msg": resp.text}

            if resp.status_code in (200, 201) and data.get("ok"):
                area = data.get("area", "unknown")
                log(f"push ok: {agent.name} -> {state} ({area})")
                return True

            msg = str(data.get("msg") or data.get("error") or resp.text)
            log(f"push failed[{attempt}/{max_retries}]: {agent.name} status={resp.status_code} msg={msg}")

            if resp.status_code in (403, 404):
                return False
        except Exception as e:
            log(f"push error[{attempt}/{max_retries}]: {agent.name} err={e}")

        if attempt < max_retries:
            sleep_sec = retry_backoff_sec * attempt
            time.sleep(sleep_sec)

    return False


def build_detail(agent: AgentSpec, state: str, raw: str, from_source: str) -> str:
    detail = (from_source or "").strip()
    if detail:
        return detail
    return agent.detail_template.format(
        name=agent.name,
        crew=agent.crew,
        agent=agent.agent,
        sourceKey=agent.source_key,
        state=state,
        raw=(raw or "").strip(),
    )[:220]


def make_source(source_conf: dict[str, Any]) -> Any:
    source_type = str(source_conf.get("type", "")).strip().lower()
    if source_type == "command":
        return CommandSource(source_conf)
    if source_type == "json_file":
        return JsonFileSource(source_conf)
    if source_type == "http_json":
        return HttpJsonSource(source_conf)
    raise ValueError("source.type must be command, json_file, or http_json")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generic external status bridge")
    p.add_argument("--config", required=True, help="Path to JSON config file")
    p.add_argument("--join-key", required=True, help="Join key used by /agent-push")
    p.add_argument("--office-url", default="http://127.0.0.1:19000", help="HappyRoom base URL")
    p.add_argument("--interval", type=float, default=10.0, help="Polling interval seconds")
    p.add_argument("--timeout", type=int, default=10, help="HTTP timeout seconds")
    p.add_argument("--max-retries", type=int, default=3, help="Retry times per push")
    p.add_argument("--retry-backoff", type=float, default=1.5, help="Retry backoff base seconds")
    p.add_argument("--once", action="store_true", help="Run one cycle only")
    p.add_argument("--dry-run", action="store_true", help="Print payload only, do not POST")
    return p.parse_args()


def run_once(
    source: Any,
    agents: list[AgentSpec],
    state_map: dict[str, str],
    default_state: str,
    args: argparse.Namespace,
) -> None:
    for agent in agents:
        try:
            snap = source.get_snapshot(agent)
            raw = str(snap.get("raw", "") or "")
            state_hint = str(snap.get("state", "") or "")
            detail_hint = str(snap.get("detail", "") or "")

            if state_hint:
                state = normalize_state(state_hint)
            else:
                state = map_state_from_text(raw, state_map, default_state)

            detail = build_detail(agent, state, raw, detail_hint)
            log(
                f"map: {agent.name} raw='{short_text(raw)}' "
                f"hint='{short_text(state_hint)}' -> state={state} detail='{short_text(detail)}'"
            )

            if args.dry_run:
                payload = {
                    "agentId": agent.agent_id,
                    "name": agent.name,
                    "state": state,
                    "detail": detail,
                }
                log("dry-run payload: " + json.dumps(payload, ensure_ascii=False))
                continue

            push_agent(
                office_url=args.office_url,
                join_key=args.join_key,
                agent=agent,
                state=state,
                detail=detail,
                timeout_sec=args.timeout,
                max_retries=args.max_retries,
                retry_backoff_sec=args.retry_backoff,
            )
        except Exception as e:
            log(f"agent cycle error: {agent.name} err={e}")


def main() -> int:
    args = parse_args()
    config_path = str(Path(args.config).expanduser())
    conf = load_config(config_path)
    source_conf = conf.get("source") or {}
    if not isinstance(source_conf, dict):
        raise ValueError("config.source must be object")

    source = make_source(source_conf)
    agents = build_agents(conf)

    state_map = conf.get("stateMap") or {}
    if not isinstance(state_map, dict):
        state_map = {}
    state_map = {str(k): str(v) for k, v in state_map.items()}

    default_state = normalize_state(str(conf.get("defaultState", "idle")))

    log(
        f"bridge start: source={source_conf.get('type')} agents={len(agents)} "
        f"interval={args.interval}s dry_run={args.dry_run}"
    )

    while True:
        run_once(source, agents, state_map, default_state, args)
        if args.once:
            break
        time.sleep(max(0.5, args.interval))

    log("bridge exit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
