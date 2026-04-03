import asyncio
import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath('..'))
from nanobot.config.loader import load_config, get_config_path
config = load_config(get_config_path())

async def main():
    print("==============================")
    print(" Day 5 & 7: 统一通道抽象 (Channels) 与路由命令 (/status 等)")
    print("==============================")
    
    # 通道的生命周期就是死循环拉或者接 WebSocket，然后把消息传递给 Dispatcher。
    # 我们这里写一个迷你的虚拟 Channel 实现：
    from nanobot.channels.base import ChatChannel, ChatMessage, FileInput
    
    class FakeTerminalChannel(ChatChannel):
        async def connect(self):
            print("[FakeChannel] 已连接！")
            
        async def send_text(self, reply_to: ChatMessage, text: str) -> None:
            print(f">>> [终端UI展示] (给用户 {reply_to.user_id}): {text}")
            
    channel = FakeTerminalChannel()
    await channel.connect()
    
    # 模拟外部事件：某位用户在 Telegram 或者飞书敲下了一个带有控制命令 /status 的消息。
    incoming_msg = ChatMessage(
        channel=channel,
        session_id="terminal_session_1",
        user_id="yingda",
        text="/status" # 注意这是斜杠命令
    )
    
    # 通常通道的 dispatch_message 会交给全局 Bus / Gateway
    # 我们在这里直接调用 nanobot 里面的 Command 处理路由。它不会走大模型额度。
    from nanobot.command.registry import CommandRegistry
    from nanobot.command.builtins import StatusCommand
    
    registry = CommandRegistry()
    registry.add(StatusCommand())
    
    print(f"\n[模拟用户输入了一段话]: {incoming_msg.text}")
    print("网关拦截检查中...")
    handler = registry.get("status")
    if handler:
        print(f"✅ 成功命中拦截路由: {handler.__class__.__name__}")
        # 该拦截器直接在内存运算，不需要去耗费 LLM Token
        await handler.execute(incoming_msg, None)
    else:
        print("未命中拦截路由，将走常规 LLM Agent Loop。")

if __name__ == "__main__":
    asyncio.run(main())
