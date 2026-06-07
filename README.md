# CyberBlog 🦞

一个赛博朋克风格的个人博客，基于 [Astro](https://astro.build) v6 构建，部署在 GitHub Pages。

## 特性

- ⚡ **纯静态** — 零后端，零数据库
- 🌙 **赛博朋克主题** — 霓虹暗色、玻璃态、网格背景
- 📝 **Markdown 写作** — 内容集合自动校验 Frontmatter
- 💬 **Giscus 评论** — 基于 GitHub Discussions
- 🔍 **站内搜索** — Pagefind 构建时索引
- 📡 **RSS** — 自动生成 RSS Feed
- 🚀 **GitHub Actions** — push 即部署

## 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 本地开发
npm run dev

# 3. 构建
npm run build

# 4. 本地预览构建结果
npm run preview
```

## 写作

在 `src/content/blog/` 下新建 `.md` 文件：

```markdown
---
title: "文章标题"
description: "文章描述"
pubDate: 2026-06-04
tags: ["tag1", "tag2"]
draft: false
---

这里是文章内容，支持 Markdown 语法。
```

## 部署到 GitHub Pages

### 1. 建仓库
创建一个 GitHub 仓库，比如 `your-username/your-username.github.io`

### 2. 推代码
```bash
git init
git add .
git commit -m "init cyberblog"
git remote add origin https://github.com/your-username/your-username.github.io.git
git push -u origin main
```

### 3. 配置 GitHub Pages
- 仓库 → Settings → Pages
- Source: **GitHub Actions**

Push 到 main 分支后，Actions 自动构建部署。

### 4. 配置 Astro
修改 `astro.config.mjs` 中的 `site` 为你的 GitHub Pages 地址。

### 5. （可选）配置 Giscus 评论
1. 在仓库开启 Discussions
2. 安装 [Giscus GitHub App](https://github.com/apps/giscus)
3. 打开 [giscus.app](https://giscus.app) 获取配置
4. 更新 `src/components/Giscus.astro` 中的属性

## 项目结构

```
cyberblog/
├── src/
│   ├── content/
│   │   └── blog/          ← 你的所有博文（.md）
│   ├── components/        ← UI 组件
│   ├── layouts/           ← 布局模板
│   ├── pages/             ← 页面路由
│   ├── styles/            ← 全局样式
│   └── content.config.ts  ← 内容集合配置
├── public/                ← 静态资源
├── .github/workflows/     ← GitHub Actions
└── astro.config.mjs       ← Astro 配置
```

## License

MIT
