# HappyRoom Requirements

更新时间：2026-05-06

## 当前需求主线

1. 角色可视化：`PM / Builder / Reviewer` 作为像素人首屏可见，并可区分身份与状态。
2. 拖拽总结：拖像素人到电脑附近需稳定触发“项目状态总结 + 催办建议”。
3. 看板能力：壁炉上方常驻可见看板入口；支持链接展示 + PPT 上传 fallback。
4. 体验增强：
   - 猫猫四态具备明确产品语义（owner 状态映射）；
   - 角色移动落点更细密；
   - 一键总结同步到 Yesterday Notes；
   - 支持每角色独立换皮肤。

## 范围说明（MVP）

- PPT/PPTX 当前为文件卡片 + 打开/下载 fallback，不包含内嵌逐页播放。
- 催办动作 v1 在总结中给出“催谁/催什么”建议；真实 Slock 催办消息由 PM 执行。

## 后续增强候选

- 看板内嵌 PPT 逐页预览与翻页控制。
- Presenter 的语音讲解/脚本讲解接口。
- Summary 与 Yesterday Notes 的筛选、历史浏览。
