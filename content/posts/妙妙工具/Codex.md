---
title: "Codex"
date: 2026-01-07
draft: False 
---

由于最近发现Codex非常好用，并且众多业界大牛一起指出Vibe Coding是未来的趋势，所以系统学习一下Codex。或许人类真的已经来到了理解*复杂系统*的时候了。

感觉总体来说使用方法是相当自然的，唯一需要注意的是最近新增加的*skill*功能。原来是anthropic提出的标准，现在被大量采纳，估计会是一个会持续很多年的标准，值得学习。

# Agent Skills 基本格式

> 官网与完整规范：https://agentskills.io/

---

## 1) 目录结构

一个 Skill 就是一个文件夹，至少包含一个 `SKILL.md`：

```

skill-name/
└── SKILL.md

```

可选：
- `scripts/`：可执行脚本
- `references/`：参考文档
- `assets/`：模板或资源

---

## 2) SKILL.md 格式

`SKILL.md` 分为两部分：

### (A) YAML Frontmatter（必需）

```yaml
---
name: skill-name
description: 该技能做什么，以及在什么情况下使用
---
```

约束：

* `name` 必须与文件夹名一致
* 仅允许小写字母、数字、连字符 `-`
* 1–64 字符，不能以 `-` 开头或结尾，不能有连续 `--`
* `description` 为 1–1024 字符

### (B) Markdown 正文（指令内容）

Frontmatter 之后是普通 Markdown，用来写操作步骤、示例、注意事项等，结构不强制。

---

## 3) 最小示例

```md
---
name: pdf-processing
description: 提取 PDF 文本与表格，用于后续分析或填表。
---

# PDF Processing

## When to use
当用户需要处理 PDF 文件时。

## Procedure
1. 读取 PDF
2. 提取文本与表格
3. 输出结构化结果
```

---

这就是 Agent Skill 的基本格式。更多细节见官网：[https://agentskills.io/](https://agentskills.io/)


# 在Codex中使用Skill
- /skill 或 $ 显式调用skill
- skill可层级override
- 内置了installer和creator（也是skill，一个自然语言安装，一个自然语言生成skill）
- 重启插件即可看到新安装的skill
