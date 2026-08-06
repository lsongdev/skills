---
name: reverse-engineering
description: Cybersecurity skill router pack for reverse engineering, authorized penetration testing, and security research. Automatically routes tasks to the right methodology, checks locally available tools, and executes reproducible workflows instead of guessing commands. Supports Claude Code, Codex CLI, Kiro, Cursor, Cline. Trigger when the user faces APK/Android, iOS/mobile, binary reverse engineering (exe/dll/so/elf), .NET/C#, frontend JS obfuscation/encryption, DSL VM, HTTP traffic capture/replay, malware/YARA, pentesting/scanning, attack chain/red team, CTF challenges, firmware/IoT, patch diffing N-day, Pwn/exploit development, EDR bypass, API/GraphQL security, supply chain/SBOM, LLM security, OLLVM deobfuscation, or security report/chart generation.
version: 1.0.0
---

# reverse-engineering (逆向/渗透技能路由包)

完整文档见 <https://github.com/zhaoxuya520/reverse-skill>。本 SKILL 仅为功能摘要，方便 Agent 了解其能力与触发场景。

## What It Is

网络安全技能路由包（MIT License），支持多个 AI 编程客户端。核心价值：**路由 + 工具链自举 + 经验复用**——当 Agent 遇到 APK、二进制、前端 JS 加密、CTF 挑战或渗透目标时，自动路由到对应方法论、检查可用工具并执行可复现的工作流，而不是猜测命令，避免在 jadx/apktool/Frida/IDA/radare2/BurpSuite 等工具间选错或重复犯错。

## Key Files

- `RULES.md` / `skills/MASTER-ROUTING.md` — 全局路由规则与主路由（先 scope gate 再 ACT）
- `skills/routing.md` — 任务 → 技能路由矩阵
- `skills/tool-index.md` — 本地工具检测状态（自动生成）
- `scripts/master-route.ps1` / `case-init.ps1` — 一键分流与案例初始化（scope/timeline/workitems）
- `skills/ops/` — scope、证据链、角色、时间线等操作契约
- `field-journal/` — 自进化经验库

## Coverage

APK/Android、iOS/移动逆向、二进制逆向（exe/dll/so/elf）、.NET/C#、前端 JS 逆向（加密参数）、DSL VM/自定义 opcode VM、HTTP 抓包重放、恶意软件/YARA、渗透测试/扫描、攻击链/红队编排、CTF（40+ 子技能）、固件/IoT、补丁对比 N-day、Pwn/exploit 开发、EDR 绕过、API/GraphQL 安全、供应链/SBOM、LLM 安全、OLLVM 混淆还原、图表与报告生成。

## When to Use

- 用户提到 APK、二进制、so/elf/exe、加固脱壳、反混淆
- 前端 JS 加密参数、小程序逆向、抓包重放
- CTF、渗透测试、红队、恶意软件分析
- 安全报告/图表生成、补丁对比、N-day 利用

## Notes

- 仅用于授权渗透测试与安全研究
- CTF-Sandbox-Orchestrator 为 GPLv3，其余依赖工具遵循各自许可证
