# Nanobot 核心架构与运行框架

基于最新的代码库（截至当前分支），结合 GitNexus 的拓扑和执行流数据（如 Community 聚类和 Execution Processes 流程追踪），本文档重新梳理了 Nanobot 的整个技术架构和边界。

## 1. 宏观模块 (Communities / Modules)

Nanobot 采用高度解耦的插件式、面向数据流的架构。根据 GitNexus 分析，整个项目主要被抽象为以下几个大型依赖网络：

### 📡 1. Channels (边界感知与消息接收)
- **体积与集中度**：项目最大的子聚类 (`symbolCount: 123` 核心方法)。
- **职责**：充当 Nanobot 的“五官”和“四肢”，对接各种 Chat 应用（微信、飞书、钉钉、Slack、Matrix、Discord等）甚至系统交互（CLI / Email）。
- **核心机制**：实现了 `base.py` 中规范出的统一通讯总线。通过 `manager.py` 和 `registry.py`，各类异构消息体被序列化为标准的事件模型并发往内置消息总线（Bus）。

### 🧠 2. Agent (自主运行时与决策大脑)
- **体积与集中度**：系统的心脏模块。
- **职责**：控制逻辑循环、思考、工具调用以及上下文约束。不关心消息来自于 Slack 还是 Console。
- **关键组件**：
  - `runner.py`: 实现了非绑定终端的裸 LLM Reasoning Loop (`AgentRunner`)，管理从对话开始到最后得出结论的自主迭代，包含并发工具派发和限流。
  - `loop.py`: 在 Runner 外包装上了生命周期和事件绑定回调（通过 `_LoopHook`）。
  - `memory.py`: 基于 Token 滑动窗口管理的 `MemoryConsolidator`，并能在逼近 context window 极限时使用 LLM 自动回溯总结为存续的 `MEMORY.md` 知识与长时事实。
  - `context.py` & `hook.py`: 定义迭代过程中的生命周期事件与状态机。
  - `skills.py` & `subagent.py`: 提供模块化的多智能体分形/委托子任务。

### 🔌 3. Providers (模型后端适配层)
- **职责**：对接底层真正的推理引擎侧，屏蔽 OpenAI、Anthropic、Azure OpenAI、Github Copilot 之间的接口差异。
- **核心机制**：通过基类提取通用的 Generator、Streamer、Embedder 特质。

### 🛠️ 4. Tools (工具链与技能箱)
- **职责**：LLM 模型与真实世界交互的“双手”。包含文件系统读写、终端命令执行、网络搜索等预定义的函数签名规范。

### ⚙️ 5. Infrastructure (基础调度/存储与通讯设施)
- **bus**: 消息中间件（Event Queue），负责把 Channels 的输入路由到 Agent，Agent 的输出推回 Channel 的长连接。
- **config**: 全局 YAML/JSON `Schema` 初始化和 `Workspace` 解析抽象。
- **session**: 会话级的上下文管理。分离用户会话，避免记忆串联。
- **cron**: 自动任务守护进程。
- **cli**: 启动入口 (`nanobot.py`) 以及命令行交互 (`__main__.py`) 设置。

---

## 2. 核心执行流 (Execution Processes)

基于 GitNexus Trace 流水线提取的调用分析，Nanobot 的活动核心是：

### Process: `Chat_stream` / `Chat`
这是系统最核心的**跨模块业务请求生命周期** (`cross_community` 类型，长达 8+ steps)。

1. **Input (Channel 层)**: 聊天工具如微信、Slack 监听抓取消息（如 `@nanobot help`）。
2. **Translation**: `manager.py` 把底层 API 的消息形态组装为一个抽象请求抛入 `MessageBus`。
3. **Dispatch (Nanobot / Loop 层)**: 取出消息，并确定它所属的 `SessionId`。
4. **AgentRunner (Agent 层)**:
   - 前置处理 (Context Management): 检查 `MemoryConsolidator`，如果不溢出 Token 就保留，溢出则归档历史总结。
   - LLM Request: 打包 System Prompt + Tools Definition + User Prompt 让 `Provider` 推理。
   - Check LLM response:
     - 包含工具? (`response.has_tool_calls`) -> 触发工具回调 -> 获取 Result -> 开启下一轮迭代投递回给模型。
     - 包含最终文本? -> 停止。
5. **Output (Channel 层)**: AgentRunner 返回 `RunResult`，MessageBus 自动捕获该响应，交由目标 Channel 的 `send_message()` 封包原路发送回终端客户端。

### Process: `Start` / `Stop`
1. Nanobot 通过 `cli` 创建 `Config` 解析。
2. 初始化 Provider 驱动、MessageBus 会话，最后启动 Channel Listeners。

---

## 3. 设计心得与建议 (Architectural Values)
- **高解耦的依赖树**：Channels **根本不依赖** Agent 具体的工具链；Agent **不关心** Channel 存在的重连接报错机制。由于由中心化 `bus` 和 `schema` 中转，项目极其方便插入新的聊天工具和底层模型。
- **自动归档的自我约束力 (Self-governed Token Context)**：`memory.py` 在 `Runner` 的每次调用中透明检查 Tokens 预算是非常巧妙的设计，保证了 Agent 的持久心智稳定性且防止崩溃。
- **强类型的状态机**：`AgentRunSpec` 和 `AgentRunResult` 强制限定了任何对模型的查询返回都必须是一个固定的枚举类型结局（比如 Tool_Call，或 Success_Finish, Error 等），对保证工具不会陷入无休止请求循环做了 `_MAX_FAILURES_BEFORE_RAW_ARCHIVE` 级别的保护。
