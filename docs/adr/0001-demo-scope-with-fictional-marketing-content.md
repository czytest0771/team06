# 0001 - Vibe Coding 比赛 demo scope，允许虚构的营销内容

**Status:** accepted (2026-05-10，updated 2026-05-10 经 Q12 grill)

## Context

`design.md` / 部署在 `https://new-website-ten-steel.vercel.app/` 的 BeeFintech 营销官网包含若干**真假混合**的内容。正式 B2B 营销官网部署虚构 / 未授权部分会触发商标 / 香港 IA GL14·GL20 / PDPO / 不实陈述等多重合规风险。

## Decision

接受此项目作为 **Vibe Coding 比赛 demo**，**不投产**，因此允许保留虚构 / 未授权的营销内容来追求演示冲击力。

## Consequences

- ⚠️ 站点必须做 **公网访问限制**：Vercel password protection、`<meta name="robots" content="noindex,nofollow">`、首屏 banner 标注「Contest demo — illustrative content only」
- ⚠️ 仓库 README + `design.md` 顶部必须写明「此内容为比赛演示用素材，含未授权使用第三方品牌」
- ⚠️ 一旦未来有商用化、对外宣传、面向真实客户的需求 → 需作废本 ADR + 替换为合规版本
- ⚠️ 所有 git remote 必须保持 private 或受限可见

---

## ✅ 真实可保留（投产时不要误改）

经 Q12 grill 确认，以下内容是 BeeFintech 公司真实事实：

### 公司信息
- Founded **2017**
- HQ **Unit 505, InnoCentre, Kowloon Tong**
- **40+ engineers & insurance experts**

### 资质 / Awards
- **HKSTP InnoCentre Resident**
- **HK ICT Awards 2020**
- **ITC TVP Qualified Vendor**
- **Government D-Biz Vendor**
- **Alibaba Cloud HK Strategic Partner**
- **Manulife BOOST Finalist**
- **Microsoft Azure 用户**（作为 cloud vendor）

### 合规 / Security
- **HK PDPO 合规**
- **ISO 27001 (in progress)** ← caveat 写法已 OK
- **AES-256 at rest**
- **TLS 1.3 in flight**
- **7-year audit retention**
- **PIBA-2023 alignment**

### Bee AI 3 张产品卡（特殊：真数据 + 假授权）
- 内容：ManuRetire 5 HK$4,800/mo / AIA Pro Annuity HK$5,200/mo / FWD Easy Save HK$4,400/mo
- **数据真实**（来自 Bee AI Broker 产品库的简化版）
- 但**ManuLife / AIA / FWD 商标 + 公开展示具体保费**未授权 → 投产化时仍需处理（见 🔴 列表）

---

## 🔴 必须替换的内容清单（投产化时）

| # | 类别 | 当前 demo 内容 | 投产替换方向 |
|---|---|---|---|
| 1 | Approved By 7 logo | YF Life · FWD · 中国人壽 · HKSTP · HK ICT 2020 · Microsoft Azure · Alibaba Cloud HK | **Q12 确认全部无书面 marketing 授权** → 仅保留实际授权过的（HKSTP / Microsoft / Alibaba 已是真合作可能 OK），其他改为 "Trusted by leading HK broker firms" 文字模糊 |
| 2 | Customer 3 条证言 | "Director, mid-size HK broker firm" 等 3 条 quote | **Q12 确认 quote 文本由 BeeFintech 同事编写** → 投产化必须换成已授权真客户 quote，或改成调研报告聚合数据 |
| 3 | Bee AI 3 产品卡 | ManuRetire 5 / AIA Pro / FWD Easy Save + HK$ 价格 | 数据真实但商标未授权 → 取得 ManuLife/AIA/FWD 书面 marketing 授权 **或** 改用产品类别名 + 模糊价格区间 + IA GL14/GL20 disclaimer |
| 4 | Phone 1 (FNA Overview) | "Chan Dawen" + 产品名 | **Q12 (d) 确认全虚构** → "Sample Customer" + watermark "Demo data only" |
| 5 | Phone 2 (AI Proposal) | "35-yr-old, married, 2 kids" + YF Life / ManuLife / CTF + 92%/87%/82% fit scores | **Q12 (d) 确认全虚构** → "Sample data" + watermark + 不显示真实保险公司商标 |
| 6 | Phone 3 (Policy Dashboard) | Margaret Wong / Andrew Lee / Cassie Chan + AUM HK$4,287,520 | **Q12 (d) 确认全虚构** → "Sample Customer" + watermark |

---

## ❓ 待 Owen 后续 confirm 的灰色项

下列内容真假未定，投产前必须挨个核实：

- **Hero 4 个 stats**：`95%+ annual renewal rate` / `8 yrs zero data breaches` / `60%+ long-term life broker share` / `20,000+ pros use our AI daily`
- **Hero 副标**：`Nine years. 150+ broker firms. 130+ insurers. Zero breaches.`
- **Web Console 运营数字**：`1,247 active policies` / `100K+ daily policy capacity` / `16+ data sources unified` / `95% process automation` / `96.4% renewal rate`
- **Footer**：`99.99% uptime` / **`"YF Life & FWD approved"`** ← 这条尤其严重（明确商业关系声明）
- **Security**：`SOC 2 Type II (annual review)` ← 真做过吗？

每条投产化前需提供数据来源 / 审计依据，否则归入 🔴 必须替换。
