---
name: wooyun
description: WooYun Legacy security testing skill based on 22,132 WooYun (2010-2016) business logic vulnerability cases. Provides real-company case references, quantitative statistics, and data-driven test priority ordering across 6 domains and 33 vulnerability categories (auth bypass, IDOR/privilege escalation, financial security, information disclosure, logic flaws, misconfiguration). Trigger when doing web security testing, e-commerce payment security, SaaS IDOR/privilege escalation audits, password reset/weak credential/verification code bypass testing, race condition analysis, SRC bug bounty planning, writing evidence-backed security reports for Chinese enterprises (government OA, telecom, banking), or security training/compliance support. Not a replacement for pentest technique training; it augments existing testing skills with real cases and data backing.
version: 1.0.0
---

# WooYun Legacy (wooyun-skills)

外部项目，无需 clone。完整文档见 <https://github.com/lsongdev/wooyun-skills>。本 SKILL 仅为功能摘要，方便 Agent 了解其能力与触发场景。

## What It Is

Claude Code 安全测试插件（fork 自 tanweai/wooyun-legacy，CC BY-NC-SA 4.0）。基于乌云（2010–2016）收录的 **22,132 个业务逻辑漏洞案例**，为安全测试注入**真实公司案例引用、量化统计（高危占比）、数据驱动的测试优先级排序**。

不教授新的渗透手法，而是给已有安全测试能力补充"真实案例 + 数据背书"。

## Knowledge Structure (3 layers, load on demand)

1. `references/` — 方法论与攻击模式矩阵（触发时优先加载）
2. `knowledge/` — 8 个技术手册（根因分析、Payload 矩阵、WAF 绕过）
3. `categories/` — 15 个漏洞案例分类索引（真实案例标题 + 高频参数 + 攻击模式分布）

## Coverage

6 大领域 33 类漏洞：

- **认证绕过**：密码重置（88% 高危）、弱口令、验证码绕过
- **越权访问**：IDOR、任意账号/查看/修改/删除
- **金融安全**：支付绕过、金额篡改、订单篡改
- **信息泄露**
- **逻辑缺陷**：状态机滥用、竞态条件
- **配置不当**

## When to Use

- 电商支付安全测试、SaaS 越权/IDOR 测试
- 代码安全审计、SRC 赏金挖洞优先级规划、竞态条件专项
- 给甲方写有说服力的安全报告
- 中国本土业务安全测试（政务 OA、运营商、银行）
- 安全培训与等保合规支撑

## Limitations

- 数据时效为 2010–2016，云原生/GraphQL/Serverless 覆盖有限
- 业务逻辑漏洞的攻击模式比技术栈更稳定，仍具参考价值
