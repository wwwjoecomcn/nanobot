# Nanobot学习计划概览 (Overview)

## 项目简介
**nanobot** 是一个受 OpenClaw 启发而编写的超轻量级个人 AI 助手项目。它旨在用最小的依赖和极简的代码来实现一个生产可用的智能体(Agent)。该项目已经集成了多种 LLM 模型厂商 (Providers) 和各大主流沟通渠道 (Channels，如 Telegram、Discord、微信、飞书、钉钉、Slack 等)，并支持内存管理、插件技能以及 Model Context Protocol (MCP)。

## 学习目标
通过这一个为期 7 天的学习计划，您将能够从头开始，系统性地掌握：
1. 项目的整体架构和模块依赖。
2. 核心智能体 `Agent` 是如何处理输入、构建上下文和控制执行流的。
3. 对话上下文(Session)与记忆(Memory)机制的实现原理。
4. 如何接入和适配不同的 LLM 模型 (Providers)。
5. 聊天渠道 (Channels) 插件机制的设计方式。
6. 辅助工具 (Tools) 与外部技能 (Skills / MCP) 是如何拓展大模型能力的。
7. 定时任务 (Cron)、命令路由管控与高级功能 (Docker 部署等) 的实现细节。

## 目录结构
每天的内容按模块进行进阶分解：

- [**Day 1: 项目初探与架构概览**](./day1.md)
  熟悉项目背景、启动运行方法、以及整体的工程源码目录结构。
- [**Day 2: Agent核心运行流**](./day2.md)
  重点剖析 `nanobot/agent` 核心包，理解 `runner.py` 与 `loop.py`，以及大模型回复的核心循环。
- [**Day 3: 上下文与记忆机制**](./day3.md)
  研究 `session` 与 `memory.py`，了解持久化历史记录与 Token 上限的截断策略。
- [**Day 4: 大模型提供商 (Providers)**](./day4.md)
  学习不同的大模型基座是如何统一被 `nanobot` 调用的。
- [**Day 5: 通讯渠道与接入层 (Channels)**](./day5.md)
  了解各种社交通讯软件 (如 Telegram、飞书等) 消息是如何与系统互通对接，了解消息的收发流。
- [**Day 6: 工具、技能与 MCP**](./day6.md)
  探索大语言模型是如何调用外部 `Tools` 的，以及 MCP (Model Context Protocol) 机制。
- [**Day 7: 定时任务、路由及其余高级特性**](./day7.md)
  综合掌握定时任务功能、控制台命令系统、系统安全性兜底与项目发布运维。

准备好之后，从 [**第一天**](./day1.md) 开始您的 nanobot 学习之旅！
