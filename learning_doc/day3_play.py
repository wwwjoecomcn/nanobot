import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from nanobot.session.manager import SessionManager
from nanobot.agent.memory import TokenEstimator, SessionMemory

async def main():
    print("==============================")
    print(" Day 3: 测试 Session 记忆与记忆截断 (Token 滑动窗口)")
    print("==============================")
    
    # 手动创建一个虚拟的上下文 Memory 对象 (不实际写盘)
    memory = SessionMemory(max_tokens=50) # 注意：这里故意设置得非常小 (50 Token上限)
    
    # 填入一些假对话历史
    memory.add_message({"role": "system", "content": "你是一个非常强大的 AI，帮助用户解决所有日常问题。由于这段话很长，它会消耗很多 Token。"})
    memory.add_message({"role": "user", "content": "第一句话，这里是第一天说的话。"})
    memory.add_message({"role": "assistant", "content": "收到了，我已记下。"})
    memory.add_message({"role": "user", "content": "我是小明，请记住我的名字，因为我很重要。"})
    memory.add_message({"role": "assistant", "content": "好的小明。"})
    memory.add_message({"role": "user", "content": "那么告诉我，我叫什么？"})
    
    print("[-] 截断前的总对话轮数: ", len(memory.messages))
    print("[-] 当前总体估算 Token: ", memory.estimate_tokens())
    
    # 强制执行自动截断 (因为我们上限设成了 50，过去的无用废话会被滑掉)
    pruned_msgs = memory.get_context()
    
    print("\n[✅] 经过 Token 滑动窗口截断后，实际取出的数组轮数:", len(pruned_msgs))
    for msg in pruned_msgs:
        print(f"   Role: {msg.get('role')} | content: {msg.get('content')[:15]}...")
        
    print("\n结论：你会发现，系统提示始终保留在最前面，而最老的用户对话由于 Token 溢出已经被抛弃！")

if __name__ == "__main__":
    asyncio.run(main())
