<!-- generated-by: superpowers-writing-plans -->

> ⚠️ **DEMO SCOPE NOTICE** — 本计划对应的站点为 **Vibe Coding 比赛 demo**，**不投产**。
> 详见 [`adr/0001-demo-scope-with-fictional-marketing-content.md`](./adr/0001-demo-scope-with-fictional-marketing-content.md)。

# BeeFintech 营销官网 实施计划（Retrospective + Remaining Work）

> **执行模式说明：** 本 plan 已不再是 prospective to-do list —— Phase 1-4 大部分已通过部署在 `https://new-website-ten-steel.vercel.app/` 完成。本文档采用 **retrospective + 剩余工作** 模型，每个 task 标注 ✅ 已完成 / 🟡 部分完成 / ❌ 未做 / ❓ 状态待确认。
>
> **For agentic workers:** 实际剩余可执行工作集中在文末「§ 剩余实际工作清单」。Phase 1-5 主体保留作为历史追溯依据 + milestone 评分锚点。

**Goal:** 从 0 到 1 完成 BeeFintech 保险科技 Web 服务平台官网，包括需求确认、UI/UX 设计稿生成、前端开发、核心交互、预约表单与 API 预留、移动端适配、测试文档和 GitHub 比赛仓库提交。

**Architecture:** 先用 `docs/design.md` 明确产品目标、页面架构、核心功能、技术栈和移动端适配，再生成 UI/UX 设计稿作为前端实现依据。前端采用静态 HTML/CSS/JavaScript，复杂视觉使用高清图片，Bee AI demo 和预约弹窗用原生 JavaScript 实现，预约表单 demo 期使用 mock 提交（不 POST 真实 API），投产化时替换为 Gateway Booking POST。

**Tech Stack:** HTML、CSS、JavaScript、PNG/WebP assets、`localStorage`、Git、GitHub。

---

## § 当前完成状态总览

| Phase | 主题 | 整体状态 | 备注 |
|---|---|---|---|
| Phase 1 | 需求与设计文档 | ✅ 已完成 | docs/design.md 满足 M3 hard rule（marker + 5 必填章节） |
| Phase 2 | 生成 UI/UX 设计稿 | 🟡 部分完成 | 高保真 mockup 在 `docs/ui-mock/20260506110510.jpg`；plan 要求的 `homepage-design.md` 未生成（mockup 图本身已等价交付） |
| Phase 3 | 首页前端骨架 | ✅ 已部署 | 部署在 Vercel；代码在队员（邓梁/骏鹏）处，**待 push 到 team-06/src/** |
| Phase 4 | 核心交互 | 🟡 部分完成 | i18n 字典 / Visualize a scenario / Ask Bee anything / Credits state machine 完整规格仍待落实 |
| Phase 5 | 移动端适配 | ❓ 未验证 | 需在真实手机 / 平板上测过 |
| Phase 6 | 测试 / 文档 / 提交 | ❌ 未做 | test.md / ai-collab-log.md / retrospective.md 在 repo 里都是 stub；M7+ 仅 main 分支 |

---

## § Milestone 映射表（M1 - M8C）

| Milestone | Hard Rule（来自 `scripts/check_milestones.py`） | 现状 | 我们 Phase 对应 |
|---|---|---|---|
| M1 | team.yml ≥3 人 + ≥2 office | ✅ 已通过 | （前置条件） |
| M2 | (Layer-2 人工审，非硬规则) | ⏳ | 不直接对应 |
| M3 | docs/design.md 含 marker + 5 必填章节 | ✅ 已通过（stub）；待 push 真版 | Phase 1 |
| M4 | docs/plan.md 含 marker + ≥4 个 Phase | ✅ 已通过（stub）；待 push 真版（本文件） | Phase 2-5 总骨架 |
| M4.5 | (Layer-2) | ⏳ | 不直接对应 |
| M.PEER1 | (跨组互评) | ⏳ | 不直接对应 |
| M5 | src/ 首页骨架 | ❌ src/ 仅有 README.md | Phase 3 + Phase 4 |
| M6 | (Layer-2) | ⏳ | 对应 Phase 5 |
| M7 | (Layer-2) | ⏳ | 对应 Phase 6 polish |
| **M7+** | **≥2 分支（main + 1 个 non-main 有 commit）** | **❌ 仅 main 分支** | **Phase 6 必做** |
| M8A | docs/test.md ≥300 字 | ✅ stub 通过（511 字）；内容是模板 | Phase 6 Task 6.1 |
| M8B | docs/ai-collab-log.md ≥500 字 | ❌ stub 443 字 < 500 | Phase 6 Task 6.2 |
| M8C | docs/retrospective.md ≥500 字 | ❌ stub 286 字 < 500 | Phase 6 Task 6.3 |

---

## Phase 1：需求定义与设计文档 ✅

目标：先完成项目定义，不直接进入开发。

交付物：

- ✅ `docs/design.md`（已完成，14K，已应用 grill 全部 12 项决议）
- 🟡 `docs/brainstorm.md` 可选 → repo 里有 358 字 stub

任务清单：

- ✅ **Task 1.1：确认项目定位**（B2B 营销官网，PaaS 私有部署 + 代码共用 —— 见 CONTEXT.md）
- ✅ **Task 1.2：定义目标用户**
- ✅ **Task 1.3：定义页面架构**
- ✅ **Task 1.4：定义核心功能**
- ✅ **Task 1.5：定义技术栈和移动端适配**
- ❌ **Task 1.6：提交设计文档到 team-06/docs/** → 当前 docs/design.md 在 Owen 本地，待 push 替换 repo stub

---

## Phase 2：生成 UI/UX 设计稿 🟡

目标：在开发前先生成可执行的 UI/UX 设计稿，作为前端开发依据。

交付物：

- 🟡 `docs/ui-mock/` 下高保真 mockup 图（`20260506110510.jpg` 等）已归档；plan 原要求的 `homepage-design.md` 或 `homepage-preview.html` **未单独生成**，因高保真图本身已传达全部信息。

任务清单：

- ✅ **Task 2.1：确定视觉方向**（白色纸感 / BeeFintech 蓝 / 克制专业 / 避免泛 SaaS 模板）
- ✅ **Task 2.2：生成首页设计稿**（高保真 PNG/JPG mockup 已存在）
- ✅ **Task 2.3：明确前端实现 vs 图片资产**
- 🟡 **Task 2.4：输出 UI/UX 设计稿文件** → 高保真图已有；可选生成 `homepage-design.md` 文字版（demo 不阻塞）
- ❌ **Task 2.5：提交 UI/UX 设计稿** → 待 push 到 team-06/docs/ui-mock/

---

## Phase 3：首页前端骨架开发 ✅（已部署）

目标：根据设计稿完成官网首页骨架和主要视觉结构。

交付物：

- ✅ `index.html`（已部署在 Vercel）
- ✅ `assets/`（图片资源已部署）
- ❌ **代码在队员处未 push 到 team-06/src/** → M5 未通过的核心原因

任务清单：

- ✅ **Task 3.1：创建页面基础结构**
- ✅ **Task 3.2：实现顶部固定导航**（含语言切换）
- ✅ **Task 3.2.5（新增）：实现 Approved By 背书条** —— design.md §2 列了但原 plan 漏建 task；线上有部署，retrospective 补记
- ✅ **Task 3.3：实现 Hero 模块**（主标题 / 副文案 / Try Bee AI / Book a demo / 4 个 trust stats）
- ✅ **Task 3.4：实现产品展示**（3 手机 demo + Web Console mockup）
- ✅ **Task 3.5：实现 Platform 6 能力**（LifeBee CRM / EBA / POS / BI / Bee AI Broker / Quote）
- ✅ **Task 3.6：实现 Security 模块**（HK PDPO / ISO 27001 / SOC 2 / AES-256 / TLS 1.3 / 7-yr audit）—— 原 Task 3.5 拆分
- ✅ **Task 3.7：实现 Customers 3 条证言**（匿名角色：Director / COO / Head of Compliance）—— 原 Task 3.5 拆分
- ✅ **Task 3.8：实现 Awards 6 张卡**（HKSTP / ITC TVP / HK ICT 2020 / Alibaba Cloud HK / D-Biz / Manulife BOOST）—— 原 Task 3.5 拆分
- ✅ **Task 3.9：实现 Company 介绍**（2017 / InnoCentre / 40+ team）—— 原 Task 3.5 拆分
- ✅ **Task 3.10：实现 CTA + Footer** —— 原 Task 3.5 拆分
- ❌ **Task 3.11：提交前端骨架到 team-06/src/** —— 当前 src/ 是空 README

---

## Phase 4：核心交互开发 🟡

目标：完成 Bee AI demo、语言切换、预约弹窗和 mock 提交。

交付物：

- 🟡 `index.html` 内交互脚本（部分已部署，部分待补）

任务清单：

- 🟡 **Task 4.1：实现 i18n 字典**（P0 必做范围已部分实现 / P1 应做范围待补） → 详见新增 Task 4.10
- ✅ **Task 4.2：实现语言状态保存**（`localStorage` 键 `beefintech_lang`）
- 🟡 **Task 4.3：实现 Bee AI demo**（仅 Compare products mode 已实现固定 3 张产品卡，Visualize / Ask Bee 模式待补）
- ✅ **Task 4.4：实现 0/3 时的预约引导**（额度用完点提交直接打开预约弹窗）
- ✅ **Task 4.5：实现预约弹窗**（7 字段表单 + 成功提示）
- ✅ **Task 4.6：实现 mock 提交**（console.log + localStorage `beefintech_bookings_demo`，**不 POST**；源码注释保留 Gateway POST 模板供投产替换）
- ❌ **Task 4.7（新增）：实现 Visualize a scenario 静态图**（35 岁退休现金流 / 受益预测时间线 SVG 或 PNG）
- ❌ **Task 4.8（新增）：实现 Ask Bee anything 固定对话片段**（约 3-4 轮假设对话气泡）
- 🟡 **Task 4.9（新增）：实现 Bee AI Credits state machine 完整规格**（详见 design.md §3.3 表格 9 项规格 —— `localStorage` + `storage` event + 防双击 + 0/3 UI + soft gate 接受重置）
- ❌ **Task 4.10（新增）：i18n 字典 `i18n.json`**（P0 + P1 范围 key-value 三语；代码侧 `data-i18n` 切换实现）
- ❌ **Task 4.11：提交核心交互到 team-06/src/**

---

## Phase 5：移动端适配与视觉打磨 ❓

目标：保证桌面端专业，移动端可用。

任务清单：

- ❓ **Task 5.1：桌面端 100% 缩放检查**（需在浏览器实测）
- ❓ **Task 5.2：平板断点适配**（`@media (max-width: 768px)`）
- ❓ **Task 5.3：手机断点适配**（`@media (max-width: 480px)`）
- ❓ **Task 5.4：检查高清资产**（Logo / 奖项 / 手机图 / Dashboard 不模糊）
- ❌ **Task 5.5：提交移动端适配到 team-06/src/**

---

## Phase 6：测试、文档与提交 ❌

目标：完成比赛提交所需文档和 GitHub 交付。

交付物：

- ❌ `docs/test.md`（M8A — repo 里 511 字 stub，内容是模板）
- ❌ `docs/ai-collab-log.md`（M8B — repo 里 443 字 stub，<500）
- ❌ `docs/retrospective.md`（M8C — repo 里 286 字 stub，<500）
- ❌ GitHub 至少 2 个分支（M7+ — 当前仅 main）
- ❌ 非 main 分支有提交（M7+）

任务清单：

- ❌ **Task 6.1：编写测试文档** `docs/test.md`，≥ 300 字，覆盖：页面结构 / 导航跳转 / 语言切换 / Bee AI demo 3 mode / 预约弹窗 / 移动端适配 / mock 提交校验
- ❌ **Task 6.2：编写 AI 协作记录** `docs/ai-collab-log.md`，≥ 500 字，记录：grill-with-docs / superpowers-brainstorming / superpowers-writing-plans / Codex / 其他 AI 工具的具体使用片段
- ❌ **Task 6.3：编写复盘总结** `docs/retrospective.md`，≥ 500 字，记录：完成情况 / 设计与开发得失 / 团队协作经验 / 后续 Gateway API 接入计划 / 可继续优化的方向
- ❌ **Task 6.4：满足 M7+ 分支要求** —— 创建 1 个非 main 分支（如 `feature/docs-grill-update`）+ 至少 1 个 commit
- ❌ **Task 6.5：提交最终文档到 team-06**
- ❌ **Task 6.6：推送 GitHub 比赛仓库**（替换 stub design.md / plan.md / test.md / ai-collab-log.md / retrospective.md）

---

## § 剩余实际工作清单（按 owner / 优先级）

### Owen（planner / doc 角色）—— 自己能 ship

1. **PUSH** 当前 docs/design.md (14K) 替换 team-06/docs/design.md (1167 字 stub) → 满足 M3 内容质量
2. **PUSH** 当前 docs/plan.md (本文件) 替换 team-06/docs/plan.md (400 字 stub) → 满足 M4 内容质量
3. **PUSH** docs/CONTEXT.md + docs/adr/0001-* + docs/archive/* + docs/ui-mock/* 到 team-06
4. **写并 PUSH** team-06/docs/test.md（≥300 字真实测试笔记）→ M8A 内容质量
5. **写并 PUSH** team-06/docs/ai-collab-log.md（≥500 字真实 AI 协作记录）→ M8B 通过
6. **写并 PUSH** team-06/docs/retrospective.md（≥500 字真实复盘）→ M8C 通过
7. **创建分支** `feature/docs-grill-update` + 把上面 6 项 push 到这条分支 → 满足 M7+

### 队员（邓梁 / 骏鹏）—— 代码侧需配合

A. **PUSH** 部署在 Vercel 的源码到 team-06/src/ → 解锁 M5
B. **实现** Bee AI demo Visualize a scenario 静态图（Task 4.7）
C. **实现** Bee AI demo Ask Bee anything 固定对话（Task 4.8）
D. **实现** Bee AI Credits state machine 完整规格（Task 4.9）
E. **实现** i18n 字典 `i18n.json` + `data-i18n` 切换（Task 4.10）
F. **替换** booking 提交为 mock（console.log + localStorage），删除 Gateway 真 fetch（Task 4.6）
G. **手机 / 平板实测** 移动端断点（Task 5.1-5.4）

---

## § 自动校验清单（更新版）

通过 `python scripts/check_milestones.py --milestone all` 跑：

- [x] `docs/design.md` 包含 marker `<!-- generated-by: superpowers-brainstorming -->`
- [x] `docs/design.md` 包含 5 个必填章节：目标、页面架构、核心功能、Tech Stack、移动端适配
- [x] `docs/plan.md` 包含 marker `<!-- generated-by: superpowers-writing-plans -->`
- [x] `docs/plan.md` 至少包含 4 个 Phase（本文件含 6 个）
- [x] `docs/plan.md` 包含任务清单
- [ ] `docs/test.md` 非空且不少于 300 字 ← 当前 stub，需 Owen 重写
- [ ] `docs/ai-collab-log.md` 非空且不少于 500 字 ← 当前 stub 443 字
- [ ] `docs/retrospective.md` 非空且不少于 500 字 ← 当前 stub 286 字
- [ ] GitHub 至少有 2 个分支 ← 当前仅 main
- [ ] 非 main 分支有提交 ← 当前无
