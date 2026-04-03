import asyncio
import os
import sys
import inspect

sys.path.insert(0, os.path.abspath('..'))

async def main():
    print("==============================")
    print(" Day 6: Tools 生成与 Python 函数自省映射测试")
    print("==============================")
    print("大模型是如何知道某个 Python 函数该怎么调用的呢？答案是通过解析你的函数签名！")
    
    # 尝试引入内置的某个工具函数
    from nanobot.skills.builtins.basic import get_current_time
    from nanobot.agent.tools.registry import ToolRegistry
    
    registry = ToolRegistry()
    registry.register_callable(get_current_time)
    
    # 拿出注册的 JSON Schema 签名
    definitions = registry.get_definitions()
    
    print("\n🧐 [解析 Python 源码]:\n```python\n" + inspect.getsource(get_current_time) + "```")
    
    print("\n🛠️ [通过 nanobot 的 registry 生成给 OpenAI/Anthropic 看的 JSON Schema]:")
    import json
    print(json.dumps(definitions[0], indent=2, ensure_ascii=False))
    
    print("\n[✅] 我们可以看到，您完全不需要手写复杂的 Schema 结构对象，nanobot 在内部自动根据您的 Python Docstrings 与参数类型把映射做好了！然后抛给大语言模型进行调用。")

if __name__ == "__main__":
    asyncio.run(main())
