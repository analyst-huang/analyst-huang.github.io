---
title: "用 Pandoc 将 Pandoc AST JSON 生成 EPUB（稳定可复现工作流）"
date: 2026-01-26T23:00:00-08:00
draft: false
---

# 背景

当你的内容已经被整理成 **Pandoc AST JSON**（即 Pandoc 的抽象语法树 JSON：顶层包含 `pandoc-api-version / meta / blocks`），Pandoc 可以直接把它转换成 EPUB，而不需要再走「拼 Markdown」的路径。

这条路线的优势是：

- 结构严格：章节、段落、目录都由 AST 明确表达
- 自动化友好：适合爬虫/批处理/流水线
- 输出稳定：避免 “把 `\n` 塞进字符串却不换行” 等语义问题

> 本文默认你的 JSON 已经是 **Pandoc AST JSON**。如果你的 JSON 是业务结构（例如 `chapters/paras`），需要先转换为 Pandoc AST，再继续。

---

# 0. 快速自检：你的 JSON 是否是 Pandoc AST

打开 JSON 文件，顶层应类似：

- `pandoc-api-version`: 版本数组
- `meta`: 元数据
- `blocks`: 块级节点数组（`Header` / `Para` 等）

也可以用 Pandoc 做一次“反向转换”来验证能否被解析：

```bash
pandoc -f json book.json -t markdown -o check.md
```

如果能生成合理的 Markdown（章节、段落结构正确），基本就没问题。

---

# 1. 最小命令：JSON → EPUB

```bash
pandoc -f json -t epub book.json -o book.epub
```

参数说明：

- `-f json`：输入格式为 Pandoc AST JSON
- `-t epub`：输出为 EPUB
- `-o book.epub`：输出文件名

---

# 2. 生成目录（TOC）

```bash
pandoc -f json -t epub book.json -o book.epub --toc --toc-depth=2
```

- `--toc`：生成目录
- `--toc-depth=2`：目录深度（通常 `1`=章节，`2`=章节+小节）

> 目录层级来源于 `Header` 的 level：`1/2/3...`。建议不要跳级（例如直接从 1 到 3）。

---

# 3. 元数据（书名/作者/语言）

你有两种方式设置元数据：

## 3.1 在命令行覆盖/补充

```bash
pandoc -f json -t epub book.json -o book.epub   --metadata title="书名"   --metadata author="作者"   --metadata language="zh-CN"
```

## 3.2 在 JSON 的 `meta` 中写入

例如书名：

```json
"meta": {
  "title": { "t": "MetaString", "c": "书名" }
}
```

> 实务上更推荐：**meta 写在 JSON 里**（可版本控制），命令行只负责构建。

---

# 4. 封面与样式（CSS）

## 4.1 添加封面

```bash
pandoc -f json -t epub book.json -o book.epub --epub-cover-image=cover.jpg
```

## 4.2 自定义排版（尤其是中文缩进）

写一个 `epub.css`（示例）：

```css
p {
  text-indent: 2em;
  line-height: 1.7;
  margin: 0 0 0.9em 0;
}
```

然后：

```bash
pandoc -f json -t epub book.json -o book.epub --css=epub.css --toc
```

> 重要提示：**不要靠在字符串里塞空格实现缩进**。HTML/EPUB 会折叠空格，缩进应交给 CSS。

---

# 5. 调试与验收：先转成 HTML/Markdown 看结构

当你怀疑 EPUB 显示异常时，先把同一份 AST 转成更易读的格式：

```bash
pandoc -f json book.json -t html -o check.html
pandoc -f json book.json -t markdown -o check.md
```

建议重点检查：

- 每个段落是否对应一个 `Para` block
- 章节是否用 `Header` block（level 是否合理）
- 是否把整段文本塞进一个 `Str`（这会导致换行被压缩）

---

# 6. 常见坑：为什么 `\n\n` 不会自动变成段落

在 Pandoc AST 里：

- **段落分隔是结构**：多个 `Para` block
- `Str` 是“纯文本 token”，其内部的 `\n` 不会被当作段落语义解析

正确做法：

- 按 `\n\n`（或你定义的段落规则）拆分文本
- 为每一段生成一个 `Para` block

如果只是段内换行，可用 inline 节点 `LineBreak`（但小说正文通常不建议滥用）。

---

# 7. 一个可复现的构建命令（建议固化到脚本）

## Windows PowerShell 示例

```powershell
pandoc -f json -t epub .\book.json -o .\book.epub `
  --toc --toc-depth=2 `
  --metadata language="zh-CN" `
  --css .\epub.css `
  --epub-cover-image .\cover.jpg
```

## Bash 示例

```bash
pandoc -f json -t epub ./book.json -o ./book.epub \
  --toc --toc-depth=2 \
  --metadata language=zh-CN \
  --css ./epub.css \
  --epub-cover-image ./cover.jpg
```

---

# 8. 输出校验（可选但推荐）

- 用 Calibre 打开预览（阅读器兼容性较好）
- 需要严格校验可用 `epubcheck`（常见于出版流程）

---

# 总结

如果你已经有 **Pandoc AST JSON**：

1. `pandoc -f json -t epub book.json -o book.epub`
2. `--toc` 自动目录
3. `--css` 做中文排版（缩进/行距/段落间距）
4. 用 `-t html/-t markdown` 先做结构验收，避免在 EPUB 里盲查问题

这套流程适合爬虫与批量生成电子书：结构可控、输出稳定、可复现。
