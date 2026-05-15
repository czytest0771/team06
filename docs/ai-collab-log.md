# AI 协作记录文档（M8b）

## 使用的 AI 工具

本项目主要使用 Codex 作为代码协作和交付整理工具，用于接手旧项目、恢复工作现场、阅读仓库结构、定位真实项目目录、修改前端预约表单、验证 Gateway API、整理 `src/` 目录并推送 GitHub。前期设计和计划文档中也保留了 superpowers brainstorming、writing-plans、grill-with-docs 等工作流痕迹，用来帮助明确官网定位、页面结构、交互范围和比赛提交要求。

## 关键协作时刻 1：恢复工作现场

任务：上一轮上下文压缩后，先不要写代码，只恢复项目状态。

AI 初始动作是读取当前工作区的 `package.json`、README、`src` 目录和最近修改文件。第一次定位到了另一个 BeeFintech 项目，随后根据用户截图重新判断真实目录在 `C:\Users\Administrator\Desktop\New Website (1)\design_handoff_concept_d_safe_marketing`。这一轮体现了 AI 协作中最重要的一点：不要只相信当前终端路径，要结合用户截图、文件夹名、最近修改时间和 git 状态重新定位现场。最后确认真实项目是静态 H5 官网，入口为 `index.html`，设计源稿在 `source/`，真实交付页不依赖传统 `src` 目录。

## 关键协作时刻 2：预约 API 接入方案修正

任务：用户要求“预约 API 不要放后端，放前端就行”，并提供 Gateway Booking API 文档。

AI 先读取桌面上的接口文档，确认接口要求 `POST https://api.lifebee.tech/api/v3/gateway/booking`，参数通过 `application/x-www-form-urlencoded` 传递，字段为 `name`、`phone`、`email`。一开始项目中曾出现后端代理方案：`server.js` 提供 `/api/booking`，前端走同源代理。用户明确要求前端直连后，AI 将 `index.html` 中的 `bookingApiUrl` 改为真实 Gateway 地址，删除后端代理路径，并新增 `frontend.test.cjs` 检查页面不再引用 `/api/booking`。这一步不是单纯“写代码”，而是把实现与接口文档重新对齐。

## 关键协作时刻 3：真实接口返回验证

任务：用户追问“API 返回的是什么”，要求不要只看页面成功状态。

AI 先承认第一次只验证了前端成功提示，没有抓原始 JSON。随后直接用 `fetch` 请求 Gateway API，使用带时间戳的测试姓名和邮箱，避免接口文档中提到的 10 分钟重复提交限制。最终抓到原始返回：

```json
{
  "status": 200,
  "code": 1000,
  "message": null,
  "timestamp": "1778852892",
  "path": null,
  "data": true
}
```

这次协作的价值在于，用户推动 AI 从“页面看起来成功”进一步走到“原始 API 返回可核验”。因此前端成功判断也可以更明确地围绕 `code === 1000 && data === true` 理解。

## 关键协作时刻 4：整理并推送 GitHub

任务：将完成的网站代码放入 `lifebee-vibe-coding/team-06` 仓库的 `src/` 目录，结构包含 `frontend`、`public`、`deploy`。

AI 发现当前网站项目的 `origin` 指向个人仓库 `enjiang0571/new-website`，并不是目标仓库，因此没有直接推错 remote，而是定位本机已有的 `team-06` checkout。随后将 H5 页面放入 `src/frontend`，将图片资源放入 `src/public/assets`，补充 `src/deploy/README.md`，并调整页面图片路径。推送时第一次命令超时，后续通过 reflog 和 `git pull` 确认远端已接收网站提交，且远端自动追加了 milestone 状态更新。

## 一个反思

AI 协作最有效的地方是快速读代码、查路径、调整实现并做验证；最容易出错的地方是“以为自己知道上下文”。本项目中两次关键纠偏都来自用户：一次是指出真实文件夹位置，一次是指出 API 必须前端直连。后续如果重做流程，应先让 AI 输出“我现在操作的是哪个目录、哪个 remote、哪个入口文件”，再进入修改；每次接口接入也应同时记录页面状态和原始响应体，避免只用 UI 成功提示替代真实验证。
