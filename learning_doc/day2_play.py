import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from nanobot.config.loader import load_config, get_config_path
config = load_config(get_config_path())

from nanobot.agent.runner import AgentRunner, AgentRunSpec
from nanobot.agent.tools.registry import ToolRegistry
from nanobot.agent.hook import AgentHook, AgentHookContext
import nanobot.providers

# 为了在屏幕上直观看到流式输出，定一个简易的 Hook
class ConsoleStreamingHook(AgentHook):
    def wants_streaming(self) -> bool:
        return True
    
    async def on_stream(self, context: AgentHookContext, delta: str) -> None:
        # 直接把模型吐出的字逐针打印到屏幕
        sys.stdout.write(delta)
        sys.stdout.flush()
        
    async def before_iteration(self, context: AgentHookContext) -> None:
        if context.iteration == 0:
            print("\n[Hook] 🟢 Agent Runner 开始接收提问，并在控制台执行流式通信...\n")

async def main():
    print("==============================")
    print(" Day 2: 触发底层的 Agent 核心循环并观测流")
    print("==============================")
    
    from nanobot.cli.commands import _make_provider
    provider = _make_provider(config)
    
    print(f"正在准备向 {config.agents.defaults.model} 提问...")
    messages = [
        {"role": "system", "content": "你是一个幽默的人，接下来请用一句搞笑的话回应。"},
        {"role": "user", "content": "我的肚子现在有点饿了。"}
    ]
    
    runner = AgentRunner(provider)
    spec = AgentRunSpec(
        initial_messages=messages,
        tools=ToolRegistry(),
        model=config.agents.defaults.model,
        max_iterations=1,
        hook=ConsoleStreamingHook(),
    )
    result = await runner.run(spec)
    
    print(f"\n\n[✅] Agent 完毕！总计使用的系统算力 Tokens 消耗为: {result.usage}")

if __name__ == "__main__":
    asyncio.run(main())
