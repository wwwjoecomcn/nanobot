# Day 5: 通讯渠道与接入层 (Channels)

## 目标
理解通道 (Channel) 抽象，这是 nanobot 作为“各种平台上的私人助理”的骨架。

## 学习任务

1. **通道管理机制 (`nanobot/channels/`)**
   - 什么是 `gateway` 服务？`nanobot gateway` 启动后发什么了什么？
   - 阅读并理解某个常用的独立信道：如 `telegram.py` (长轮询机制) 或 `feishu.py` (长链接 WebSocket 机制)。理解“收信”和“发信”的对应关系。
   - 什么是“事件驱动(Event-driven)消息分发”？从 Telegram 的 API 层获取一次消息到触发 Agent 的整个调用栈是什么样的？

2. **阅读开发者文档: `CHANNEL_PLUGIN_GUIDE.md`**
   - 在 `docs/` 目录下阅读通道插件的新手指北。
   - 整理出：自定义一个 Channel 需要开发哪些核心的生命周期 (如 `connect()`,`dispatch_message()`)？

3. **处理平台独有特性 (多模态、富文本等)**
   - 思考：如何把 Feishu 的独特卡片 (CardKit) 原样推送，或者如何让 Slack 呈现复杂的 Thread 并保持上下文？
   - 微信长轮询网关/二维码机制 ( `weixin.py` 及其 `login` 逻辑) 是怎么设计的。

## 理论作业
- 在纸上画一画：从用户打开 Telegram App 并发送一句文字到 nanobot 后端接收、传给 LLM 并且边推边发的**数据流向图**。

## 思考题
- 如果不同的平台对图片的支持情况不同(有的必须要 URL，有的必须传二进制，有的最大体积有限)，nanobot 抽象层是怎么处理这些多模态发送瓶颈的？
