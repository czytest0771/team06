<!-- BEE-STATUS-START -->
# Team · 进度仪表盘

> 由 `.github/workflows/milestone-check.yml` 在每次 push 后自动更新。详细规则见 `BeeFintech 比赛进度系统 spec v3`。

## 📊 进度

| Code | 名称 | 截止 | 必须 | 状态 | 说明 |
|------|------|------|------|------|------|
| **M1** | 组队 + team.yml | 5/9 | 必须 | ✅ | M1 通过：3 人，2 个不同办公室 |
| **M2** | Brainstorm Q&A | 5/10 | 可选 | ❌ | brainstorm.md 至少 8 个 Q&A（当前 2 个） |
| **M3** | design.md | 5/10 | 必须 🔴 | ✅ | M3 通过：5 必填章节齐全 + marker 存在 |
| **M4** | plan.md | 5/10 | 必须 🔴 | ✅ | M4 通过：6 个 Phase |
| **M4.5** | UI/UX 设计稿 | 5/10 | 可选 | ❌ | docs/ui-mock/ 下没有非空设计稿文件 |
| **M.PEER1** | 互评他队文档 | 5/15 | 必须 (评委侧聚合) | ⏳ | 尚未运行（push 任意 commit 触发） |
| **M5** | Phase 1 首页骨架 | 5/15 | 必须 | ❌ | src/ 下未找到源码文件（支持: .astro, .cjs, .htm, .html, .js, .jsx, .mjs, .svelte, .ts, .tsx, .vue） |
| **M6** | Phase 2 核心功能 | 5/15 | 必须 | ❌ | src/ 下未找到源码文件 |
| **M7** | Phase 3+4 部署 | 5/15 | 必须 🔴 | ❌ | src/ 下未找到源码文件，无法校验移动端适配 |
| **M7+** | ≥ 2 分支 | 5/15 | 必须 🔴 | ✅ | M7+ 通过：分支 ['feature/docs-grill-update', 'main'] |
| **M8A** | 测试文档 (≥300 字) | 5/15 | 必须 🔴 | ❌ | M8a 测试文档 与原始模板完全一致（未实际编辑） |
| **M8B** | AI 协作记录 (≥500 字) | 5/15 | 必须 🔴 | ❌ | M8b AI 协作记录 与原始模板完全一致（未实际编辑） |
| **M8C** | 复盘文档 (≥500 字) | 5/15 | 必须 🔴 | ❌ | M8c 复盘文档 与原始模板完全一致（未实际编辑） |

> 图例：✅ 通过 / ❌ 未通过 / ⏳ 尚未运行 · 「必须 🔴」= 不通过将影响硬规则评分

## 🎯 下一步

用 `/superpowers:brainstorming` 写 `docs/brainstorm.md`：≥ 8 个 Q&A（M2 可选但建议做）

<!-- BEE-STATUS-END -->

## 📚 比赛资料

- [比赛简报包 v3](https://github.com/lifebee-vibe-coding/ops/wiki)
- [话题圈发帖模板](docs/brainstorm.md)
- [提示词档案模板](prompts/README.md)

## 🛠 技术约定

- **提交规范：** `M3: 完成 design.md` 前缀写当前 milestone
- **分支：** main 必有；M7+ 要求至少 2 分支
- **不接受邮件提交**，全部通过 GitHub repo 完成

## 🤖 AI Review（限频）

在 PR 评论里写 `/review` 触发 AI 反馈。每个 milestone 限 1 次。
