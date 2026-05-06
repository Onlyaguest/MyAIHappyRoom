# Generic External Status Bridge (P0)

`scripts/external_status_bridge.py` 用于把外部系统状态桥接到 HappyRoom 的 `/agent-push`。

目标：替代硬编码的 `sync-mata-state.sh`，支持可配置 source、状态映射、重试和日志。

## 支持的状态源

- `command`：执行外部命令读取状态。
- `json_file`：读取 JSON 文件。
- `http_json`：调用 HTTP JSON 接口。

## 核心能力

1. 状态映射：`stateMap` + 通用关键词兜底。
2. 重试与回退：`--max-retries`、`--retry-backoff`。
3. 可观测日志：输出原始状态、映射结果、推送结果与失败原因。
4. 安全默认：sample 配置不带真实 token、绝对路径、私有网关。

## 快速开始

```bash
cd MyAIHappyRoom
python3 scripts/external_status_bridge.py \
  --config scripts/external_status_bridge.file.sample.json \
  --join-key YOUR_JOIN_KEY \
  --office-url http://127.0.0.1:19000 \
  --dry-run --once
```

去掉 `--dry-run` 后会实际调用 `/agent-push`。

## Sample 配置

- `scripts/external_status_bridge.command.sample.json`
- `scripts/external_status_bridge.file.sample.json`
- `scripts/external_status_bridge.http.sample.json`
- `scripts/external_status_input.sample.json`

## 约束

- 桥接目标当前为 `/agent-push`（访客/外部 agent 路径）。
- 不会改写 PM/Builder/Reviewer 的 `/team-status` 数据。
- 若要桥接到 `team-status`，建议新开任务做权限与冲突规则设计。
