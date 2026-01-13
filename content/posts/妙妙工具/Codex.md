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

# 并行使用Codex
在优化代码的时候，Codex提出有三个优化的点，完全可以每个点创建一个branch，让codex在不同的分支工作，最后再让codex把这几个branch merge起来，实现功能的并行化实现。Codex不是一个员工，而且可以是一群员工！

# 使用 git worktree + AI 进行本地多分支并行开发（实践指南）

本指南总结了如何使用 **git worktree**
在本地为多个分支创建独立工作目录，并配合多个 AI 会话（如 Codex / Claude
Code / 本地 Agent）实现**并行开发、互不干扰、可控合并**的工作流。

------------------------------------------------------------------------

## 一、为什么需要 git worktree

在传统 Git 工作流中：

-   一个工作目录一次只能 checkout 一个分支
-   切分支前需要 stash 或提交
-   AI 会话上下文容易因切分支而失效
-   不能真正并行推进多个功能

**git worktree
允许同一仓库拥有多个工作目录（工作树）**，每个目录可检出不同分支：

-   各自拥有独立的 HEAD / index / 工作区文件
-   共享同一个 Git 对象数据库（不重复存储历史）
-   可以同时运行多个构建、测试、AI 会话

适合： - 多 feature 并行开发 - AI 代理并行改代码 - 长时间运行实验（训练
/ 编译）同时推进其他任务

------------------------------------------------------------------------

## 二、核心概念速览

-   **主仓库（primary worktree）**：最初 clone 下来的目录
-   **附加工作树（linked worktrees）**：通过 `git worktree add`
    创建的其他目录
-   所有 worktree：
    -   共享 `.git/objects`
    -   但各自有独立工作区和分支 checkout 状态
-   一个分支只能被一个 worktree checkout（Git 会强制约束）

------------------------------------------------------------------------

## 三、推荐目录结构

建议把 worktree 放在主仓库的**平级目录**：

    ~/projects/
      myrepo/                 # main 分支（主工作树）
      myrepo-featureA/        # worktree: featureA
      myrepo-featureB/        # worktree: featureB

避免把 worktree 放进主仓库子目录，防止： - 目录混乱 - 工具误扫描 -
.gitignore 误配置

------------------------------------------------------------------------

## 四、创建 worktree 的标准命令

### 1. 从 main 新建分支并创建 worktree

``` bash
git worktree add -b featureA ../myrepo-featureA main
```

参数说明： - `-b featureA`：创建新分支 featureA -
`../myrepo-featureA`：新工作目录路径 - `main`：基于哪个分支创建

### 2. 使用已有分支创建 worktree

``` bash
git worktree add ../myrepo-featureB featureB
```

含义： - 在新目录中 checkout 已存在的 featureB 分支

### 3. 查看当前所有 worktree

``` bash
git worktree list
```

### 4. 删除 worktree（完成开发后）

``` bash
git worktree remove ../myrepo-featureA
git worktree prune
```

`prune` 用于清理已删除目录的残留记录。

------------------------------------------------------------------------

## 五、与 AI 并行开发的推荐流程

目标：每个任务 = 一个分支 = 一个 worktree = 一个 AI 会话

### Step 1：创建多个 worktree

``` bash
git worktree add -b reward-refactor ../repo-reward main
git worktree add -b replay-clean   ../repo-replay  main
git worktree add -b memory-opt     ../repo-memory  main
```

### Step 2：在不同终端 / IDE / 会话中进入各自目录

终端 A：

``` bash
cd ../repo-reward
启动 AI Agent（只处理 reward 相关修改）
```

终端 B：

``` bash
cd ../repo-replay
启动 AI Agent（只处理 replay 逻辑）
```

终端 C：

``` bash
cd ../repo-memory
启动 AI Agent（只处理 memory / CUDA 优化）
```

每个 AI 都看到的是**稳定、单一分支上下文**，不会因切分支而丢失理解。

### Step 3：各自分支提交

在各自 worktree 内：

``` bash
git status
git add .
git commit -m "Implement reward refactor for bimanual grasp"
```

所有提交都会立即写入同一个仓库历史中。

### Step 4：回主工作树合并

``` bash
cd ~/projects/myrepo
git checkout main
git pull origin main
git merge reward-refactor
git merge replay-clean
git merge memory-opt
```

如有冲突： - 人工解决，或 - 把冲突片段交给 AI 单独修复

### Step 5：推送或创建 PR

``` bash
git push origin main
```

或对每个 feature 分支创建 PR 再合并。

------------------------------------------------------------------------

## 六、与多 clone 的对比

  方式             并行分支   磁盘占用   Git 历史
  ---------------- ---------- ---------- ------------
  多次 git clone   可以       高         各自独立
  git worktree     可以       低         共享对象库

worktree 只复制工作区文件，不复制 `.git/objects`。

------------------------------------------------------------------------

## 七、常见注意事项

### 1. 同一分支不能被两个 worktree 同时 checkout

Git 会直接拒绝，这是保护机制。

### 2. 不要在 worktree 之间复制 .git 目录

所有 worktree 都应由 `git worktree add` 创建和管理。

### 3. 分支命名与目录名保持一致

有利于脚本管理和快速定位：

    repo-reward  -> reward-refactor
    repo-replay  -> replay-clean

### 4. 长期不用的 worktree 要清理

避免残留锁定分支、污染开发环境。

------------------------------------------------------------------------

## 八、适用场景总结

特别适合以下情况：

-   多个 AI 并行推进多个 feature
-   RL / Robotics 项目中 env / reward / policy / replay 同时改
-   一个分支在跑长时间实验，另一个分支继续开发
-   避免频繁 stash / checkout

本质优势：

> 用空间换并行度，用目录隔离换上下文稳定性。

------------------------------------------------------------------------

## 九、最小可用模板（复制即用）

``` bash
# 从 main 创建三个并行开发分支
git worktree add -b taskA ../repo-taskA main
git worktree add -b taskB ../repo-taskB main
git worktree add -b taskC ../repo-taskC main

# 各自进入目录启动 AI 开发

# 完成后合并
cd ../repo
git checkout main
git merge taskA
git merge taskB
git merge taskC
```

------------------------------------------------------------------------

如果你在使用 Codex / Claude Code / VS Code Agent，可以进一步叠加：

-   每个 worktree 一个独立 Agent 会话
-   明确限制每个 Agent 的修改范围
-   最终由人工控制 merge 顺序与冲突解决

这是当前本地多 Agent 并行开发的最稳健实践之一。
