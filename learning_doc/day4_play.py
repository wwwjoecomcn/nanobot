import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from nanobot.config.loader import load_config, get_config_path
config = load_config(get_config_path())

async def main():
    print("==============================")
    print(" Day 4: 暴露底层的 Provider API 调用 (绕开 Agent 与记忆机制)")
    print("==============================")
    
    # 我们不用 Agent Runner 也不用任何循环，直接手工组装 JSON，喂到底层的 Anthropic / OpenAI 兼容类里面。
    # 比如我们直接导入底层抽象文件里的基类
    from nanobot.cli.commands import _make_provider
    provider = _make_provider(config)
    model = config.agents.defaults.model
    
    messages = [
        {"role": "user", "content": "这几天你在干嘛？随便回一句就好，假装我是老朋友。"}
    ]
    
    # `chat_with_retry` 是所有 Provider 都要继承和实现的最小可用阻塞接口。
    print(f"[⌛️ 发送请求中...] Provider: {provider.name()} -> Model: {model}\n")
    try:
        response = await provider.chat_with_retry(messages=messages, model=model)
        print("🤖 [底层返回包]:\n", response.content)
        print("\n⚙️ [系统用量]:\n", response.usage)
        
    except Exception as e:
        print(f"❌ 请求提供商失败，原因: {e}")
        
    print("\n[✅] 今天您学习了如何手工拼接报文。任何新模型只要继承 Provider，按照这种格式把响应打出来，nanobot 就能直接无缝挂载！")

if __name__ == "__main__":
    asyncio.run(main())
