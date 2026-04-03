# Day 4: 大模型提供商 (Providers)

## 目标
搞明白不同厂商的大模型 (OpenAI、Anthropic、DeepSeek 等) 的 API 层面是不尽相同的，nanobot 是怎么把它们包成统一样子的？

## 学习任务

1. **研究 Providers 包 (`nanobot/providers/`)**
   - 看看目前支持的厂商文件 (如 `openai.py`, `anthropic.py` 或基类 `base.py`)。
   - 回忆 `README.md` 中提到 “去除了 litellm 并更换为 native 抽象”的内容。为什么要做这种解耦？
   - 了解一个 Provider 最需要实现的两个核心功能是什么？(通常是阻塞请求与流式流(Streaming)回复)。

2. **多模态与工具调用的差异兼容**
   - 并不是所有大模型都支持同样的系统提示格式 (System prompt) 与多模态 (Vision / Image input)。
   - 在各家底层 Provider 实现中，如何抹平 `nanobot` 自己的中间数据结构与各家私有 JSON 结构体系 (比如 OpenAI 的 Message 与 Anthropic 的 Message 格式不同)。

3. **测试 Provider 切换**
   - 在 `config.json` 里，将原本的 OpenAI 或 OpenRouter 配置尝试切换到另外一家免费或你已有的厂商 (如 DeepSeek、Kimi 或者 Ollama)。
   - 对话测试：功能是否一切如旧？如果用不同的提供商，终端的 Debug JSON 信息里是否不一样？

## 思考题
- 假如明天出现了一个全新的模型厂商 "AcmeAI"，它的流式规则非常奇怪。如果我要在 nanobot 中集成，我应该实现哪些最核心的 Provider 基类方法？
- "提示词缓存"(Prompt Caching) 在不同厂商侧的原理和体现是什么样的？
