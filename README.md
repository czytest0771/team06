<!-- BEE-STATUS-START -->
# Team · 进度仪表盘

> 由 `.github/workflows/milestone-check.yml` 在每次 push 后自动更新。详细规则见 `BeeFintech 比赛进度系统 spec v3`。

## 📊 进度

| Code | 名称 | 截止 | 必须 | 状态 | 说明 |
|------|------|------|------|------|------|
| **M1** | 组队 + team.yml | 5/9 | 必须 | ✅ | M1 通过：3 人，2 个不同办公室 |
| **M2** | Brainstorm Q&A | 5/10 | 可选 | ✅ | M2 通过：9 个 Q&A |
| **M3** | design.md | 5/10 | 必须 🔴 | ✅ | M3 通过：5 必填章节齐全 + marker 存在 |
| **M4** | plan.md | 5/10 | 必须 🔴 | ✅ | M4 通过：6 个 Phase |
| **M4.5** | UI/UX 设计稿 | 5/10 | 可选 | ❌ | docs/ui-mock/ 下没有非空设计稿文件 |
| **M.PEER1** | 互评他队文档 | 5/15 | 必须 (评委侧聚合) | ⏳ | 尚未运行（push 任意 commit 触发） |
| **M5** | Phase 1 首页骨架 | 5/15 | 必须 | ✅ | M5 通过：2 个源码文件，部署配置 OK，首页含队名「绝对王者」 |
| **M6** | Phase 2 核心功能 | 5/15 | 必须 | ✅ | M6 通过：src/ 含预约表单 + API 调用 |
| **M7** | Phase 3+4 部署 | 5/15 | 必须 🔴 | ✅ | M7 通过：部署 URL `https://github.com/lifebee-vibe-coding/ops/wiki)`，含`，含`，含`，含 viewport meta |
| **M7+** | ≥ 2 分支 | 5/15 | 必须 🔴 | ✅ | M7+ 通过：分支 ['feature/docs-grill-update', 'main'] |
| **M8A** | 测试文档 (≥300 字) | 5/15 | 必须 🔴 | ✅ | M8a 测试文档 通过：1772 字符 |
| **M8B** | AI 协作记录 (≥500 字) | 5/15 | 必须 🔴 | ✅ | M8b AI 协作记录 通过：2056 字符 |
| **M8C** | 复盘文档 (≥500 字) | 5/15 | 必须 🔴 | ✅ | M8c 复盘文档 通过：2042 字符 |

> 图例：✅ 通过 / ❌ 未通过 / ⏳ 尚未运行 · 「必须 🔴」= 不通过将影响硬规则评分

## 🎯 下一步

在 `docs/ui-mock/` 下放至少 1 张设计稿（手绘/Figma 截图均可，M4.5 可选）

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

<!-- GRILL-REVIEW-START -->

## 🔥 M3 / M4 文档 Grill Review（2026-05-11）

> 评估方法：[grill-me skill](https://www.aihero.dev/skills-grill-me) 风格 · 评估人：Claude（未调用 DeepSeek） · 仅评文档本身质量

### M3 design.md · 4.5/5

**亮点**
- 文档**最开头**显式贴 "DEMO SCOPE NOTICE"——**第一段就明确「不投产 + 含未授权第三方 logo」**，scope 边界顶级
- §3.2 i18n 三级覆盖范围用 P0/P1/P2/不做 矩阵——**唯一一队做了显式优先级分级的**
- §3.3 Credits state machine 9 项规格表（存储介质/扣减时机/跨 tab 同步/隐私模式...）——工程级的状态机定义
- §3.5 预约提交"design.md v1 曾尝试把扩展字段拼接到 notification 中，但 Gateway API 字段表里没有 `notification` 或 `message` 字段可承载——**此方案物理上做不到，已废弃**"——**唯一一队显式记录了「被废弃的决策路径」**
- §6 D1-D10 验收标准矩阵——第三方可独立验证

**Grill 问题**
1. §3.3 "数据真实性说明 (Q12 grill 结果): 3 张产品卡的产品名+价格来自真实 Bee AI Broker 产品库简化版，**数据准确**；但 ManuLife/AIA/FWD 商标 + 公开展示具体保费**未经书面 marketing 授权**——投产化前需取得授权或改用类别名+模糊价格区间"——**demo 期都用未授权数据了，比赛截图发圈不会引发 IP 风险？** 文档识别了问题但没给"比赛阶段的处理决议"
2. §3.4 表单字段 7 个（姓名/公司/职位/手机/邮箱/关注模块/备注），但 §3.5 Gateway API 只接 3 个（name/phone/email）——**剩下 4 个字段去哪了？** 文档说"需 Gateway 后端扩展或经中转代理（Vercel Function / 自建 backend）"，但**比赛 demo 走哪条？** localStorage mock 时这 4 个字段被保留到本地了，但投产化前不知道——这个含糊
3. §3.2 简中/繁中差异原则"以简中为底版，繁中只做术语替换"——**香港业务为什么用简中做底版？** 客户主要语言是繁中，底版反向了

### M4 plan.md · 4/5

**亮点**
- 顶部声明 "**已不再是 prospective to-do list**——Phase 1-4 大部分已通过部署完成。本文档采用 **retrospective + 剩余工作** 模型，每个 task 标注 ✅ 已完成 / 🟡 部分完成 / ❌ 未做 / ❓ 状态待确认"——**唯一一队明确标注 plan 性质转换的**
- §当前完成状态总览表格 6 个 Phase × 状态——一眼看完
- §Milestone 映射表——把 hard rule 跟 phase 对齐
- §剩余实际工作清单按 owner / 优先级分组——**唯一一队做 owner 分工的**
- §自动校验清单跟 `check_milestones.py` 对齐——闭环

**Grill 问题**
1. Phase 3 "✅ 已部署"，但 Task 3.11 "提交前端骨架到 team-06/src/" 标 ❌——**「已部署 in Vercel」≠「代码在 repo」**，这种 inconsistency 应该被显性标注："已部署但代码仍在队员本地，M5 不通过"
2. §剩余工作清单 Owen 列了 7 项 "PUSH"——**Owen 一个人 PUSH 7 件需要多久？** plan 没估时间，会不会到 deadline 前 push 不完
3. 队员（邓梁/骏鹏）那一栏列了 7 项 (A-G)——**他们看过这个 plan 吗？接受吗？** 单向分配 vs 双向确认没区分

---

<!-- GRILL-REVIEW-END -->
