<!-- generated-by: superpowers-brainstorming -->

> ⚠️ **DEMO SCOPE NOTICE** — 本文档与对应站点为 **Vibe Coding 比赛 demo**，**不投产**。
> 内容含未授权使用的第三方品牌 logo / 产品名 / 价格、虚构客户姓名、未经审计的 stats 等。
> 详见 [`adr/0001-demo-scope-with-fictional-marketing-content.md`](./adr/0001-demo-scope-with-fictional-marketing-content.md)。
> 域内术语见 [`../CONTEXT.md`](../CONTEXT.md)。

# BeeFintech 保险科技营销官网 Design 文档

## 1. 目标

本项目目标是从 0 到 1 建设一个面向保险经纪公司、保险机构、渠道团队和保险科技生态伙伴的 BeeFintech 官网。网站需要同时承担品牌宣传、产品介绍、服务体验、预约演示和后续 API 接入的职责，最终成为一个可访问、可演示、可交付的保险科技 Web 服务平台。

本项目不是 C 端保险销售网站，也不是单纯的 SaaS 模板页，而是一个 B2B PaaS 型官网。页面需要体现 BeeFintech 在香港保险经纪业务数字化中的可信度、专业感和产品深度。

核心目标：

- 建立 BeeFintech 的专业品牌形象。
- 让用户快速理解平台服务对象、核心价值和业务覆盖范围。
- 展示 BeeFintech 在保险经纪业务全流程中的数字化能力。
- 提供 **Bee AI demo** 轻量演示（Bee AI Broker 的公开试用版），让用户感受到增值服务能力。
- 通过预约演示表单承接潜在客户线索。
- 为后续接入真实预约 API 预留清晰接口。
- 输出完整文档和代码，提交到 GitHub 比赛仓库。

目标用户：

- 保险经纪公司老板和管理层。
- 保险经纪业务负责人、产品经理和运营负责人。
- 保险机构渠道团队、IT 负责人和合规负责人。
- 比赛评委和项目验收人员。

成功标准：

- 用户在 30 秒内能判断 BeeFintech 是面向保险经纪业务的保险科技平台。
- 用户能看到产品能力、AI 服务、安全背书、客户信任和公司资质。
- 用户可以完成 Bee AI 演示体验。
- 用户可以提交预约演示表单。
- 项目代码和文档满足比赛提交要求。

## 2. 页面架构

网站采用单页长滚动官网结构，桌面端优先，兼顾移动端适配。页面从品牌认知到功能理解，再到信任建立和预约转化，形成完整浏览路径。

页面结构如下：

1. 顶部导航
   - BeeFintech Logo。
   - Platform。
   - Bee AI。
   - Security。
   - Customers。
   - Company。
   - 语言切换。
   - Book a demo。

2. Hero 首屏
   - 主标题。
   - 副文案。
   - Try Bee AI 主按钮。
   - Book a demo 次按钮。
   - 可信数据侧栏。

3. Approved By 背书条
   - 展示合作伙伴和认证背书。

4. Bee AI demo（试用 Bee AI Broker）
   - 展示可交互的 Bee AI demo（Bee AI Broker 的公开试用版）。
   - 用户选择 mode（3 选 1）→ 输入问题 → 获得**该 mode 对应的固定演示回答**。
   - 体验次数限制为 3 次（详见 §3.3 state machine）。
   - 次数用完后引导预约。

5. 产品展示：移动端 + Web Console
   - 展示 FNA、AI Proposal、Policy Dashboard 三个手机场景。
   - 展示 Brokerage HQ / Dashboard Web Console。

6. Platform 能力模块
   - 展示 LifeBee CRM、LifeBee EBA、LifeBee POS、LifeBee BI、Bee AI Broker、LifeBee Quote 六个能力。

7. Security 安全模块
   - 展示 HK PDPO、ISO 27001、Encryption、Audit trail。

8. Customers 客户背书模块
   - 展示客户证言和业务价值。

9. Awards & Credentials 奖项资质模块
   - 展示 6 张奖项/资质卡片。

10. Company 公司介绍模块
    - 展示成立时间、总部、团队、生态背书。

11. CTA 和页脚
    - 引导预约演示。
    - 展示可信信息和基础状态信息。

页面信息流原则：

- 先建立“可信的保险科技平台”认知。
- 再展示“能做什么”和“怎么提效”。
- 接着用安全、客户、奖项、公司信息强化信任。
- 最后通过预约表单完成转化。

## 3. 核心功能含预约表单 + API

### 3.1 顶部固定导航

导航需要在页面滚动时保持可见，方便用户随时跳转到不同模块。

导航项：

- Platform。
- Bee AI。
- Security。
- Customers。
- Company。

右侧功能：

- 语言切换。
- Book a demo。

导航点击后需要平滑跳转到对应模块，并避免固定导航遮挡模块标题。

### 3.2 多语言切换（分级 i18n 策略）

网站需要支持 **English / 简体中文 / 繁体中文** 三种语言。

切换要求：

- 不刷新页面，使用 `data-i18n` 字典动态替换。
- 用户刷新页面后保留上次语言选择（`localStorage` 键 `beefintech_lang`）。

#### 三级覆盖范围

| Tier | 内容范围 | 三语全做 |
|---|---|---|
| **P0 必做** | 顶部导航 / Hero 主副标题 / Trust stats / 所有 CTA 按钮 / Platform 6 模块标题 + 一句话描述 / Security 6 项标题 / Customers 区标题 / Footer 主要 link / 预约表单字段 + 成功提示 / Bee AI demo 3 个 mode 名 + 输入提示 | ✅ |
| **P1 应做** | Bee AI demo 3 mode 的固定回答内容（产品名保留英文，描述译） / Phone 3 个 demo 内文 / Web Console mockup 内文 | ✅ |
| **P2 可不做** | Customer 证言全文（保留原 quote 语言） / Awards 详细描述 / Company 段落（仅做关键词） | 🟡 |
| **不做** | Approved By 机构名 / Awards 奖项名 / 保险产品名（ManuRetire 5 等） | ❌ 保留原文（专有名词 / 商标） |

#### 简中 / 繁中差异原则

以**简中为底版**，繁中只做术语替换（如「计画书」/「計劃書」、「数据」/「數據」），不重写整段。

### 3.3 Bee AI demo 详细规格

> **Bee AI demo 是 Bee AI Broker 在公开网站的轻量演示版本**：3 次 credit 限制 + 每个 mode 返回**预设的固定 demo 回答**。
> 真实产品 Bee AI Broker 接入 4,400+ 保险产品库，仅向已签约客户开放。
> 访客通过本 demo 体验 RAG/KAG 输出形态，**不替代真实 fact-finding**。

#### 初始状态

- 顶部显示 `Bee AI · ready`
- 右侧显示 `Credits 3 / 3`
- 显示**三个模式按钮**（已删 Generate proposal —— demo 不展示 proposal 输出形态）：
  - **Compare products**
  - **Visualize a scenario**
  - **Ask Bee anything**
- 显示输入框
- 未提交问题前不显示回答区

#### 输入框默认提示语

```text
EN: Enter your question. Example: I'm 35, want retirement protection, budget HK$5,000/month. Compare 2-3 options.
简中: 请输入您的问题 示例：我 35 岁，希望配置退休保障，预算每月 HK$5,000。比较 2-3 个选项。
繁中: 請輸入您的問題 示例：我 35 歲，希望配置退休保障，預算每月 HK$5,000。比較 2-3 個選項。
```

#### 3 个 mode 各自的固定 demo 输出

| Mode | demo 输出 | 状态 |
|---|---|---|
| **Compare products** | 3 张产品卡（ManuRetire 5 HK$4,800/mo / AIA Pro Annuity HK$5,200/mo / FWD Easy Save HK$4,400/mo，带横向进度条对比） | ✅ 已部署 |
| **Visualize a scenario** | 静态图：35 岁退休现金流 / 受益预测时间线（SVG 或 PNG） | 🟡 待实现 |
| **Ask Bee anything** | 对话气泡形式的固定问答片段（约 3-4 轮假设对话） | 🟡 待实现 |

> **数据真实性说明**（Q12 grill 结果）：3 张产品卡的产品名 + 价格来自真实 Bee AI Broker 产品库简化版，**数据准确**；但 ManuLife / AIA / FWD 商标 + 公开展示具体保费**未经书面 marketing 授权** —— 投产化前需取得授权或改用类别名 + 模糊价格区间。

回答区底部统一显示：`<800ms` / `No data stored` / 香港区旗 + `HK`。

#### 提交逻辑

1. 用户选择 mode → 输入任意问题 → 点击提交
2. 前端校验通过 → Credits 扣减 1
3. 下方展示**该 mode 对应**的固定 demo 输出
4. 提交期间提交按钮 disabled 防双击

#### Credits state machine（3/3）

| 维度 | 规格 |
|---|---|
| 存储介质 | `localStorage` 键 `beefintech_bee_ai_credits`，值为剩余整数 |
| 初始值 | 用户首次访问写入 3 |
| 扣减时机 | 提交按钮点击 + 前端校验通过后扣 1（失败不扣，校验前不扣） |
| 跨 tab 同步 | 监听 `storage` 事件刷新 UI 显示 |
| 同 tab 防双击 | 提交按钮在请求 + 渲染期 disabled |
| 隐私模式 / 清 storage | **明确接受会重置**（这是 soft gate）；投产化时换后端真额度 |
| 切换语言 | 保留剩余次数（语言 ≠ 用户） |
| 0/3 时 UI | 提交按钮文案变为 "Book a demo →"，点击直接打开预约弹窗（详见 §3.4） |
| 补 credits | demo 期不存在 |

### 3.4 预约表单

预约表单用于承接官网访问者的销售线索。所有预约入口必须复用同一个弹窗或同一套表单逻辑。

触发入口：

- 顶部导航 Book a demo。
- Hero 区 Book a demo。
- CTA 区 Book a demo。
- Bee AI demo 额度用完后的预约引导。

表单字段：

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| 姓名 | 是 | 预约人姓名 |
| 公司名称 | 是 | 所属公司 |
| 职位 | 是 | 预约人职位 |
| 手机号 | 是 | 联系手机号 |
| 邮箱地址 | 否 | 联系邮箱 |
| 关注产品模块 | 否 | 用户关注的 BeeFintech 产品模块 |
| 备注 | 否 | 需求或问题补充 |

提交成功提示：

```text
已收到您的预约，我们会在一个工作日内联系您。
```

### 3.5 预约提交（Demo 期：mock 提交）

#### Demo 阶段提交方式：mock 提交

表单提交逻辑：

1. 前端字段校验通过后，将 7 个字段（姓名/公司/职位/手机号/邮箱/关注模块/备注）写入：
   - `console.log("[BOOKING DEMO]", formData)` 便于调试 / 评委审查
   - `localStorage` 键 `beefintech_bookings_demo`（数组追加）
2. **不发送任何真实 HTTP 请求**
3. UI 显示 §3.4 的成功提示文案
4. 副作用：CORS / 跨域 / Gateway API 可用性问题在 demo 期不会触发

#### 投产化路径

投产时把 mock 替换为 Gateway POST。源码注释保留以下模板供投产替换：

```js
// ❌ DEMO ONLY: 替换前请通过 IA / PDPO 合规审查 + 取得 Gateway 后端扩展字段支持
// const body = new URLSearchParams({ name, phone, email });
// await fetch("https://api.lifebee.tech/api/v3/gateway/booking", {
//   method: "POST",
//   headers: { "Content-Type": "application/x-www-form-urlencoded" },
//   body
// });
```

| API 字段 | 来源 |
|---|---|
| name | 预约表单姓名 |
| phone | 预约表单手机号 |
| email | 预约表单邮箱 |

> 4 个 extension 字段（公司名称 / 职位 / 关注模块 / 备注）需 Gateway 后端扩展或经中转代理（Vercel Function / 自建 backend）。design.md v1 曾尝试把它们"拼接到通知内容中"，但 Gateway API 字段表里没有 `notification` 或 `message` 字段可承载 —— **此方案物理上做不到，已废弃**。

### 3.6 高清资产使用原则

以下内容应使用高清图片：

- BeeFintech Logo。
- 奖项资质图片。
- 手机产品界面。
- Dashboard / Web Console 截图。

以下内容应使用 HTML/CSS 实现：

- 导航。
- 标题。
- 按钮。
- 文字说明。
- 卡片。
- 表单。
- Bee AI demo 对话框结构。

这样可以兼顾清晰度和设计准确性。

## 4. Tech Stack

前端技术：

- HTML。
- CSS。
- 原生 JavaScript。

资产：

- PNG / WebP 图片。
- 本地 `assets/` 目录管理 Logo、奖项和产品截图。

交互：

- 原生 DOM 事件。
- `localStorage` 保存语言和 Bee AI demo 剩余额度。
- 表单提交函数预留 API 接入。

代码托管：

- Git。
- GitHub 比赛仓库。

部署目标：

- 项目完成后可部署为静态网站。
- 如需代理 Gateway API，可增加轻量后端接口或 serverless function。

文档：

- `docs/design.md`。
- `docs/plan.md`。
- `docs/test.md`。
- `docs/ai-collab-log.md`。
- `docs/retrospective.md`。

选择该技术栈的原因：

- 官网以静态展示和轻量交互为主，原生 HTML/CSS/JS 足够完成。
- 不引入复杂框架可以降低比赛交付风险。
- 预约 API 接入可以集中在少量 JavaScript 函数或后端代理中。
- 静态站更容易托管、检查和提交。

## 5. 移动端适配

移动端目标：

- 保证内容可读。
- 保证导航、Bee AI demo 和预约表单可用。
- 保证图片不横向撑破页面。
- 保证按钮和输入框触控区域足够大。

适配策略：

- 桌面端使用两栏布局。
- 移动端改为单栏布局。
- Hero 数据侧栏在移动端放到主标题下方。
- Bee AI demo 在移动端宽度占满容器。
- 产品展示中的手机和 Dashboard 在移动端纵向排列。
- 平台能力卡片由三列/两列改为单列。
- 奖项卡片由三列改为单列或两列。
- 表单字段在移动端单列显示。

移动端断点建议：

```css
@media (max-width: 768px) {
  /* tablet and mobile layout */
}

@media (max-width: 480px) {
  /* compact mobile layout */
}
```

移动端验收标准：

- 不出现横向滚动。
- 主要文字不重叠。
- 导航可使用。
- Bee AI demo 输入和提交可使用。
- 预约弹窗可完整填写和关闭。

## 6. 验收标准

| 编号 | 验收项 | 标准 |
| --- | --- | --- |
| D1 | 页面架构 | 页面包含顶部导航、Hero、Approved By、Bee AI demo、产品展示、Platform、Security、Customers、Awards、Company、CTA、页脚 |
| D2 | 品牌表达 | 页面能清晰传达 BeeFintech 是 B2B 保险科技 PaaS 平台 |
| D3 | AI 演示 | Bee AI 可输入、提交、展示固定回答、扣减额度 |
| D4 | 额度引导 | 额度用完后再次提交会打开预约弹窗 |
| D5 | 预约表单 | 表单字段完整，提交后显示成功提示 |
| D6 | 提交规划 | demo 期使用 mock 提交（console.log + localStorage），投产化路径（Gateway POST）在源码注释保留 |
| D7 | 多语言 | 英文、简体中文、繁体中文关键文案可切换 |
| D8 | 高清资产 | Logo、奖项、产品截图清晰 |
| D9 | 移动端 | 移动端无横向滚动，核心功能可用 |
| D10 | GitHub | 代码和文档提交到 GitHub 比赛仓库 |
