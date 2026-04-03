# Day 2: Agent 核心运行流

## 目标
深入理解 `nanobot/agent` 模块，这也是一切基于 LLM 对话引擎的核心组件。

## 学习任务

1. **核心文件 `loop.py`**
   - 深入阅读 `nanobot/agent/loop.py`。
   - 理解核心 `agent_loop(…)` 算法的思想：
     系统提示词(System Prompt)是如何与用户最新提问(User Query)及历史(memory)拼接的？
   - 追踪在请求遇到工具调用 (Tool Calls/Function Calling) 时的重入 (Re-entry) 机制。

2. **`runner.py` 与 `context.py` 的作用**
   - `runner.py`: 关注如何封装一次会话。它是串联 `Agent` 与 `LLM` 引擎之间的桥梁，管理运行周期与钩子回调。
   - `context.py`: 阅读如何将不同消息的数据结构 (User, Assistant, System, Tool) 标准化。

3. **研究钩子回调 (Hooks)**
   - 了解 `hook.py`。
   - Agent在请求前、流式生成中、以及执行结束后，抛出了哪些事件？
   - 这些事件在通道 (Channels) 中是如何被消费并实时流式推送文字的？ (解决心跳与长连接体验)

## 代码实验
- 在 `agent_loop` 函数中加入一个 `print`，将最终组合给提供商 (Provider) 的全量数组打印出来。在 CLI 里聊几句，观察每一轮发送的底层 JSON 数组长什么样。

## 思考题
- 如果模型返回了 Tool Call 指令，主死循环是如何执行工具响应结果并重新发出的？
- 所谓的流式 (Streaming) 回复，在架构上是如何跨过整个架构推送到前端 (例如微信/飞书/终端)的？
