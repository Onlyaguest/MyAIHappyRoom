# MATAHappyRoom 对照清单

更新时间：2026-05-06
对照对象：<https://github.com/Onlyaguest/MATAHappyRoom>

## 已做（MyAIHappyRoom 已覆盖）

1. 基础状态看板能力：状态映射、气泡、办公室场景。
2. 昨日小记：`/yesterday-memo` 可用。
3. 多 Agent 协作：`/join-agent`、`/agent-push`、`/leave-agent` 可用。
4. 多语言/移动端/资产抽屉/Gemini 生图/安全配置能力保留。
5. 桌面壳能力（`desktop-pet/`、`electron-shell/`）保留。
6. 在 MATA 基线之上新增了：
   - PM/Builder/Reviewer 像素人与状态联动；
   - 拖拽到电脑一键总结；
   - Yesterday Notes 汇总写入；
   - 角色独立皮肤；
   - 壁炉看板（链接 + 上传 + 演讲位）。

## 部分做（有基础能力，但缺 MATA 的专用实现）

1. 外部 Agent 状态同步：
   - 已有通用推送链路（`office-agent-push.py` + `/agent-push`）。
   - 但没有 MATA 仓库里的 `sync-mata-state.sh` 那种针对 `bb status` 的现成桥接脚本。
2. 日志/总结能力：
   - 已有昨日小记 + 一键总结。
   - 但没有 MATA 前端里“最近 3 天日志”的远程拉取流程。

## 未做（MATA 有、当前 MyAI 未实现）

1. MATA Gateway 聊天面板与 Token 流程：
   - `window.MATA_WS_TOKEN`、`wss://gw.viewspark.ai/ws-live`、`/knock` 对话接口（MATA `frontend/index.html` 中存在）。
2. MATA 专用脚本：
   - `sync-mata-state.sh`（依赖本地 `bb status` 命令和 `~/mata` 目录）。
3. `scripts/gen-yesterday-memo.sh` 与 `frontend/assets-list.json` 这两个文件级能力未迁入。

## 不建议做（当前 HappyRoom 方向不匹配）

1. 直接复刻 MATA 的默认 Token 提示/硬编码网关地址。
   - 风险：安全性差，环境耦合重，不利于公开部署。
2. 强绑定 `bb status` 的本地路径脚本。
   - 风险：只适配单一团队环境，跨机器不可复用。

## 建议进入 Backlog

### P0

1. 通用“外部状态桥接器”脚本（替代 `sync-mata-state.sh` 的硬编码版本）。
   - 目标：支持可配置命令/HTTP 源，把外部多 agent 状态映射到 `/agent-push`。
   - 依赖：状态映射表、重试策略、错误日志。

### P1

1. 可插拔聊天/日志面板（不绑定 MATA 网关）。
   - 目标：前端保留聊天 UI，后端新增可配置 provider 代理层（例如自建 webhook / gateway）。
   - 依赖：鉴权方案、provider 抽象、超时与失败回退。

2. 最近 N 天工作日志视图。
   - 目标：在不依赖外部私有网关的前提下，展示统一日志源。
   - 依赖：日志存储接口、查询 API、分页/过滤。

### P2

1. 资产清单导出（`assets-list.json`）与 Yesterday Memo 生成脚本化工具。
   - 目标：增强运维可追溯性。
   - 依赖：脚本规范、CI/手动触发方式。
