# Day 6: 工具、技能与 MCP

## 目标
掌握 nanobot 操控外部世界的能力机制，即工具调用 (Tool Call/Function Calling) 和外部通用协议 (MCP)。

## 学习任务

1. **基本工具包 (`nanobot/agent/tools.py` 与 `skills/`)**
   - 查看内置了哪些原始技能，比如联网搜索信息 (Web Search) 或者终端命令执行 (Shell commands) 以及读取文件等。
   - 阅读其实现，弄明白一个 Python 函数是如何带上类型标注与 docstring 被解析成标准的 JSON Schema 并抛给 LLM 调用的？
   - LLM 调用完成后，Python 代码通过什么方法拿到返回参数？返回的 `stdout` 是如何插回到 `Message` 然后开启下一次对话重试的？

2. **MCP (Model Context Protocol)**
   - 搞清楚 MCP 是一个什么样的开放工业标准。
   - nanobot 目前是如何集成它的：是否允许第三方开启一个 MCP 服务器 (Server)，然后我们在 `config.json` 里添加它，nanobot 就会自动发现并透传对应的功能给当前选中的大模型？

3. **动手实践**
   - 按照教程编写一个非常非常简单的第三方 Python Skill 或手动在 `tools` 里新加一个能够返回你本地城市随机天气的函数。
   - 运行它，提问“今天我这边的城市天气如何”，看控制台调试日志，观察大模型选择了你开发的这个函数。

## 思考题
- 让智能体拥有了能够“执行终端命令”的能力是非常危险的。你觉得 nanobot 哪些代码行是用来兜底恶意删除 (`rm -rf`) 一类请求的？
- 调用工具时，如果超时 (Timeout) 或者返回崩溃信息，机制应该如何将“报错信息”优雅地塞给 LLM 让他自我反思？
