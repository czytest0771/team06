# BeeFintech 官网 (Marketing Site) Context

本上下文定义 BeeFintech 公司的 B2B 营销官网项目。这个网站本身**不是产品**，而是用于展示 BeeFintech PaaS 平台、收集潜在客户线索的对外宣传站点。

> **Project scope:** Vibe Coding 比赛 demo，**不投产**。允许虚构营销内容（真实品牌 logo、写死保险产品价格、虚构客户姓名等）以追求演示冲击力。投产化前必须替换 —— 详见 [`docs/adr/0001-demo-scope-with-fictional-marketing-content.md`](./docs/adr/0001-demo-scope-with-fictional-marketing-content.md)。

## Language

**BeeFintech**:
一家面向香港保险经纪公司的 B2B 保险科技公司，其核心产品是 PaaS 平台。
_Avoid_: 单纯写「平台」「系统」，会与下文术语冲突。

**BeeFintech Platform** (BeeFintech 的产品):
BeeFintech 提供给保险经纪公司的 PaaS，**代码共用、数据私有部署**（multi-tenant by code, single-tenant by data）。
_Avoid_: 「SaaS」「云服务」（BeeFintech 不是 multi-tenant data SaaS）；「服务平台」（已弃用）。

**本网站** (This Website / 营销官网):
BeeFintech 用于品牌展示、产品介绍、收集销售线索的**对外营销网站**（marketing site）。访客在网站上**不消费任何业务能力**，只浏览介绍 + 提交预约。
_Avoid_: 「Web 服务平台」「服务门户」「门户」—— 这些词在 SPEC 早期版本里出现过，已统一为「营销官网」。

**预约 / Booking**:
访客在网站上提交的销售线索表单（7 字段）。**demo 期使用 mock 提交**（写入 `console.log` + `localStorage`，不 POST 真实 API），投产化时替换为 Gateway Booking POST 由销售人工跟进。
_Avoid_: 「订单」「Demo 申请」「Lead」—— 后者是英文同义词但中文统一用「预约」。

**访客 / Visitor**:
浏览营销官网的外部用户。访客 ≠ BeeFintech Platform 的最终用户。
_Avoid_: 「用户」「客户」（这两个词在不同语境下指向不同主体，禁止裸用）。

### Bee AI 三层命名（重要，禁止混用）

**Bee AI Broker** (产品全名):
BeeFintech 的真实 AI 产品：RAG/KAG 引擎，对比 4,400+ 真实保险产品，向已签约客户开放。出现在 Platform 6 大能力列表、内部 SKU 文档、合同里。
_Avoid_: 「AI Broker」单独使用（容易跟 human broker / AI agent 混淆）；「Chatbot」（技术形态描述，跟 Broker 不在同一语义层）。

**Bee AI** (品牌简称):
**Bee AI Broker** 在营销场景的简称。出现在 Hero CTA 按钮（"Try Bee AI"）、顶部导航锚、用户口语。
_Avoid_: 「Bee AI / AI Broker」（斜杠并列写法）；「我们的 AI」「our AI」泛指。

**Bee AI demo** (演示形态名):
公开营销官网首屏的演示组件，**Bee AI Broker 的轻量预览**：3 次 credit + 3 个 mode（Compare products / Visualize a scenario / Ask Bee anything），每个 mode 返回**预设的固定 demo 回答**。**功能上 ≠ Bee AI Broker 真实产品**。
_Avoid_: 「Bee AI Chatbot」「AI Chatbot」（技术形态描述，且不传达"演示"边界）。

## Relationships

- **本网站** 是 **BeeFintech** 的营销渠道，介绍 **BeeFintech Platform** 的能力
- **访客** 在 **本网站** 提交 **预约**（demo 期 mock 提交，投产期 POST Gateway）
- **Bee AI Broker** 是 **BeeFintech Platform** 的 6 大能力之一
- **Bee AI demo** 是 **Bee AI Broker** 在 **本网站** 的轻量演示版本（不替代真实 fact-finding）
- **Bee AI** 是 **Bee AI Broker** 在营销文案里的品牌简称

## Flagged ambiguities

- ❌→✅ **「Web 服务平台 / 服务门户 / 网站升级 / 官网」** 在早期 SPEC §1 §2 §11 中混用 —— 已统一为 **「本网站 = 营销官网」**（2026-05-10 锁定，design.md 已应用）。
- ❌→✅ **「Bee AI / AI Broker / Bee AI Chatbot / AI Chatbot」** 在 design.md + 线上站里 6 处混用 —— 已锁定三层命名 **Bee AI Broker / Bee AI / Bee AI demo**（2026-05-10，design.md 已应用）。
- ❌→✅ **预约表单 7 字段 vs Gateway API 3 字段的 extension 处理** 之前给了两条互相冲突且物理上做不到的方案 —— 已统一为 **demo 期 mock 提交、投产化时再处理**（2026-05-10，design.md §3.5 已重写）。
- ❌→✅ **Bee AI demo 4 mode 按钮但只有 1 个固定回答** 是误导性 UX —— 已删 Generate proposal、剩 3 mode 各做不同回答（2026-05-10，design.md §3.3 已应用）。
- ❌→✅ **多语言"均需跟随语言变化"** 措辞模糊 —— 已锁定 P0/P1/P2 分级 i18n 策略（2026-05-10，design.md §3.2 已重写）。
- ❌→✅ **Bee AI Credits state machine** 仅 4 句模糊描述 —— 已落实 9 项完整规格（2026-05-10，design.md §3.3 已增补）。
- ❌→✅ **plan.md vs 现实状态严重脱节** —— 已重写为 retrospective + remaining work + milestone 映射表（2026-05-10）。
- 🟢 SPEC §3 「目标用户表」audience 混乱问题：SPEC 已被 design.md 取代并归档至 `docs/archive/`，不再阻塞当前 scope。
- 🟡 **Trust stats / Web Console 数字 / Footer "99.99% uptime" / Footer "YF Life & FWD approved" / SOC 2 Type II** 的真实性 —— 待 Owen 后续 confirm（详见 ADR-0001 ❓ 待确认清单）。
