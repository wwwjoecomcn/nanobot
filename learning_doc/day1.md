# Day 1: 项目初探与架构概览

## 目标
建立对 nanobot 项目运作方式的第一印象，安装启动本地版本。

## 阅读建议
今天的主要目标是不看具体代码实现，先通过 `README.md` 和配置文件结构感受这个系统是如何组合在一起的。

## 学习任务

1. **阅读官方 README**
   - 了解项目的轻量级哲学和与 OpenClaw 的关系。
   - 看看官方支持的通讯渠道 (Channels) 有哪些。

2. **跑通环境并启动控制台**
   - 创建虚拟环境 (或使用 `uv`)并安装依赖: `pip install -e .`
   - 使用终端快速体验设置流：运行 `nanobot onboard --wizard`，熟悉它的自动配置生成。
   - 打开 `~/.nanobot/config.json`，检查自动生成的配置与 `nanobot/config/` 中的 `defaults.json` 的对应关系。
   - 运行命令行测试：直接运行 `nanobot agent` 输入 "你好" 测试。

3. **梳理目录结构**
   - 根目录下有 `nanobot` 核心包，进入查看子文件夹。
   - 了解以下文件夹的高水平各自职责：
     - `cli/`: 命令行互动与初始化配置入口。
     - `agent/`: 智能体的主逻辑。
     - `providers/`: 大语言模型 API 接入。
     - `channels/`: 通用信息通道的实现 (如 Telegram)。

## 思考题
- 为什么不直接把 LLM 的回答打印到屏幕，而是把所有的通讯过程都抽象出 `Channel` 概念？
- `nanobot agent` 与 `nanobot gateway` 这两个命令的本质区别是什么？
