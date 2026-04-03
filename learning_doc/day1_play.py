import asyncio
import os
import sys

# 临时挂载核心库路径
sys.path.insert(0, os.path.abspath('..'))
from nanobot.config.loader import load_config, get_config_path
config = load_config(get_config_path())

async def main():
    print("==============================")
    print(" Day 1: 配置文件挂载与系统状态监测")
    print("==============================")
    print(f"[✅] 成功加载您在 ~/.nanobot/config.json 的配置！")
    print(f"- 当前全量通道(Channels)开启状态: {list(config.channels.model_dump().keys())}")
    print(f"- 您当前默认设定的 LLM 厂商: {config.agents.defaults.provider}")
    print(f"- 您当前默认使用的具体模型: {config.agents.defaults.model}")
    print("\n恭喜！如果在上方看到了您的配置数据，说明核心的全局变量加载正常。")

if __name__ == "__main__":
    asyncio.run(main())
