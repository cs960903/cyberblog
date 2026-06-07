---
title: "Astro 快速上手指南"
description: "半小时搭建一个现代静态博客，使用 Astro + GitHub Pages 零成本部署。"
pubDate: 2026-06-04
tags: ["astro", "tutorial", "web"]
draft: false
---

## 什么是 Astro？

Astro 是一个现代化的静态站点生成器，它的核心理念是：

1. **零 JS 开销** — 默认输出纯 HTML/CSS，按需加载 JS
2. **岛屿架构** — 可以嵌入 React/Vue/Svelte 组件
3. **内容集合** — 内置 Markdown/MDX 支持，类型安全
4. **性能优先** — 天生满分 Lighthouse

## 安装

```bash
npm create astro@latest -- --template basics
cd my-blog
npm install
npm run dev
```

就这么简单，`http://localhost:4321` 已经可以访问了。

## 内容集合

Astro 的 Content Collections 让你用类型安全的方式管理博客文章：

```ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    tags: z.array(z.string()).default([]),
  }),
});
```

每篇文章就是一个 Markdown 文件，Frontmatter 会被自动校验类型。

## 部署到 GitHub Pages

只需要一个 GitHub Actions 配置：

```yaml
name: Deploy to GitHub Pages
on:
  push: { branches: [main] }
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: withastro/action@v3
```

Push 到 main 分支，Actions 自动构建，几秒后网页上线。

## 为什么推荐 Astro？

| 特性 | Astro | 其他框架 |
|------|-------|---------|
| 构建速度 | ⚡ 极快 | 一般 |
| 页面体积 | 极小（无 JS） | 较大 |
| 学习曲线 | 低 | 中 |
| 扩展性 | 极高 | 高 |

如果你是个人博客、文档站、企业官网——**Astro 是目前的最佳选择**。
