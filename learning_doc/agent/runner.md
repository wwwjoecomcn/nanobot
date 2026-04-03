# Agent 核心驱动解析：`runner.py`

`runner.py` 是大模型走向“自主化执行系统”的最底层驱动器。全篇仅 200 多行代码，却撑起了极其复杂的 Agent 自治执行流程。全篇主要定义了 **2 个数据包裹类**（负责入参和出参）以及 **1 个核心动作类**（负责开启死循环）。

下面是对 `runner.py` 的全面解析：

---

## 一、 外置打包材料 (`AgentRunSpec` 与 `AgentRunResult`)

这两个 `@dataclass` 是用来和外面的世界（比如 `loop.py`）做信息交换的包裹。

### 1. `AgentRunSpec` (入参图纸)
要把机器人跑起来，传递所需的配置和信息：
- `initial_messages`：聊天的历史记录（提问就藏在这里面）。
- `tools`：注册好的工具库清单 `ToolRegistry`（提供大模型能使用的所有工具 Schema 规范）。
- `max_iterations`：极其关键的参数，**防止大模型发疯死循环**。如果它调用工具反复失败，达到该限制（默认 10 或 15 轮）就会被立刻强制拦截。

### 2. `AgentRunResult` (结案报告)
大模型折腾完之后，带回给外部系统的结果：
- `final_content`: 最终告诉用户的回复文本。
- `usage`: 消耗了多少底层平台 Token（算力计费）。
- `tool_events`: 偷偷执行的工具历史日志事件列表，用于给 UI 打点或排查。

---

## 二、 核心大轴 ⚙️ `AgentRunner.run()` 机制

整个大模型的终极奥义都在 `run()` 方法的 `for` 循环中：
```python
for iteration in range(spec.max_iterations):
    ...
```
它实现了大模型“推断问题 -> 发现需要工具 -> 调用工具 -> 获取结果再次推断”的核心自循环心智：

### 步骤 1：触发推理与发送
系统将包含系统指令的 `messages` 历史记录和 `tools` 定义书，一并传递给后端的云服务商发送网络请求（`chat_with_retry`）。

### 步骤 2：命运的分叉点（检测 `has_tool_calls`）
大模型回复后，程序会拦截判断 `response.has_tool_calls`：

- **如果为 `False`**：说明大模型已经推算出了最终想要告诉您的文字答案，直接执行 `break` 结束死循环并返回结案报告！
- **如果为 `True`（重头戏）**：
  1. `run()` 暂时挂起大模型的输出。
  2. 提取出大模型想要的函数名和参数，形如 `{"name": "web_search", "arguments": "..."}`。
  3. 执行 **本地步骤**：跳转到 `_execute_tools` 执行该 Python 本地函数，拿到实际运算结果（如搜索页面的 HTML），以 `{"role": "tool", "content": result}` 追加到历史记录数组末尾。
  4. 触发 `continue`，**带着工具最新探测到的知识，跳回循环顶部再次问大模型该怎么办！**

### 步骤 3：工具底层执行兜底 (`_execute_tools`)
当被调起 `_execute_tools` 时，框架展现了极强的健壮性：
- **并发支持 (`concurrent_tools`)**：如果大模型一次性输出了 5 条读文件的命令，`runner.py` 会借助 `asyncio.gather` 并发读取，极大提升响应速度！
- **返回特质 `tuple`**：底层 `_run_tool` 会返回包括喂给大模型真实结果的 `result`、展示给人类屏幕事件简述的 `event`，以及专门监控 Python 原生代码级别抛错的 `error` 对象。
- **自我纠偏**：工具中的一切 Bug 引发的宕机崩溃会被捕捉成普通字符串 `"Error: ValueError: xxx"` 丢给大模型，让大模型读懂报错，形成**自主容错修复能力**。

---

## 三、 扩展总结：完全解耦的架构优势

`runner.py` 中**没有处理任何关于外部业务的逻辑**（比如对接什么消息频道、存了什么长期记忆）。一切与外界显示的挂钩仅仅依靠生命周期探针 `hook`：

```python
await hook.before_execute_tools(context)
```
每当进入生命周期的某个节点，`runner.py` 会通知 `hook`。这种高度解耦意味着：这 200 行代码不仅可以放在服务器跑自动微信机器人，被终端 CLI 调用跑本地助手，甚至未来还可以打包塞进微型开发板或者客户端程序中！
