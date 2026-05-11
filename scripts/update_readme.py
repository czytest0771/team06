"""根据 milestone-results.json 更新 README.md 中的 BEE-STATUS 区块。

仪表盘表头：Code / 名称 / 截止 / 必须 / 状态 / 说明
说明列：成功时显示通过详情，失败时显示失败原因（来自 milestone-results.json.message）。
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ICON = {True: "✅", False: "❌"}
ICON_PENDING = "⏳"

# 列展示顺序 + 元数据（与 spec v3 第 199-211 行对齐）。
# 字段：key（results dict 里的 key）/ label（README 列显示）/ name / due / required
MILESTONES = [
    {"key": "m1",       "label": "M1",      "name": "组队 + team.yml",         "due": "5/9",  "required": "必须"},
    {"key": "m2",       "label": "M2",      "name": "Brainstorm Q&A",          "due": "5/10", "required": "可选"},
    {"key": "m3",       "label": "M3",      "name": "design.md",               "due": "5/10", "required": "必须 🔴"},
    {"key": "m4",       "label": "M4",      "name": "plan.md",                 "due": "5/10", "required": "必须 🔴"},
    {"key": "m4_5",     "label": "M4.5",    "name": "UI/UX 设计稿",            "due": "5/10", "required": "可选"},
    {"key": "m_peer1",  "label": "M.PEER1", "name": "互评他队文档",            "due": "5/15", "required": "必须 (评委侧聚合)"},
    {"key": "m5",       "label": "M5",      "name": "Phase 1 首页骨架",        "due": "5/15", "required": "必须"},
    {"key": "m6",       "label": "M6",      "name": "Phase 2 核心功能",        "due": "5/15", "required": "必须"},
    {"key": "m7",       "label": "M7",      "name": "Phase 3+4 部署",          "due": "5/15", "required": "必须 🔴"},
    {"key": "m7_plus",  "label": "M7+",     "name": "≥ 2 分支",                "due": "5/15", "required": "必须 🔴"},
    {"key": "m8a",      "label": "M8A",     "name": "测试文档 (≥300 字)",      "due": "5/15", "required": "必须 🔴"},
    {"key": "m8b",      "label": "M8B",     "name": "AI 协作记录 (≥500 字)",   "due": "5/15", "required": "必须 🔴"},
    {"key": "m8c",      "label": "M8C",     "name": "复盘文档 (≥500 字)",      "due": "5/15", "required": "必须 🔴"},
]

# 下一步指引（key → 鼓励性提示）。仅对失败/未做的第一个 milestone 给提示。
NEXT_HINTS = {
    "m1": "完成 `team.yml`：队名 / 队长 / 成员 / 办公室（M1 必须）",
    "m2": "用 `/superpowers:brainstorming` 写 `docs/brainstorm.md`：≥ 8 个 Q&A（M2 可选但建议做）",
    "m3": "用 `/superpowers:brainstorming` 生成 `docs/design.md`：5 必填章节 + marker（M3 必须 🔴）",
    "m4": "用 `/superpowers:writing-plans` 生成 `docs/plan.md`：≥ 4 个 Phase + marker（M4 必须 🔴）",
    "m4_5": "在 `docs/ui-mock/` 下放至少 1 张设计稿（手绘/Figma 截图均可，M4.5 可选）",
    "m5": "Phase 1：在 `src/` 实现首页骨架；首页要出现队名；同时确保有部署配置（vercel.json / netlify.toml / GitHub Pages workflow 等）",
    "m6": "Phase 2：在 `src/` 实现预约表单（`<form>`）+ 调用 API（`fetch` / `axios`）",
    "m7": "Phase 3+4：把部署 URL 写进 README，并在源码加 `<meta name=\"viewport\">`",
    "m7_plus": "GitHub 至少 2 个分支（main + feature/dev），都有提交（M7+ 必须 🔴）",
    "m8a": "完成 `docs/test.md`：删除顶部 `TEMPLATE_UNTOUCHED` 标记并写真实测试记录（≥ 300 字）",
    "m8b": "完成 `docs/ai-collab-log.md`：删除 `TEMPLATE_UNTOUCHED` 后写 ≥ 500 字 AI 协作记录",
    "m8c": "完成 `docs/retrospective.md`：删除 `TEMPLATE_UNTOUCHED` 后写 ≥ 500 字复盘",
}


# team-05 / team-09 历史上把 m4_5 / m7_plus 写成 m4.5 / m7+，这里做 fallback。
KEY_ALIASES = {
    "m4_5": ["m4.5", "m4_5"],
    "m7_plus": ["m7+", "m7plus", "m7_plus"],
}


def _result_for(results: dict, key: str) -> dict | None:
    if key in results:
        return results[key]
    for alias in KEY_ALIASES.get(key, []):
        if alias in results:
            return results[alias]
    return None


def _icon_for(r: dict | None) -> str:
    if r is None:
        return ICON_PENDING
    return ICON[bool(r.get("passed"))]


def _note_for(r: dict | None) -> str:
    if r is None:
        return "尚未运行（push 任意 commit 触发）"
    msg = (r.get("message") or "").strip()
    # message 里的反引号在 GitHub markdown 表格中需要保留，但 | 必须转义
    return msg.replace("|", "\\|") if msg else ("通过" if r.get("passed") else "未通过")


def render_status_table(results: dict) -> str:
    headers = "| Code | 名称 | 截止 | 必须 | 状态 | 说明 |"
    sep =     "|------|------|------|------|------|------|"
    lines = [headers, sep]
    for m in MILESTONES:
        r = _result_for(results, m["key"])
        row = f"| **{m['label']}** | {m['name']} | {m['due']} | {m['required']} | {_icon_for(r)} | {_note_for(r)} |"
        lines.append(row)
    return "\n".join(lines)


def determine_next_step(results: dict) -> str:
    for m in MILESTONES:
        r = _result_for(results, m["key"])
        if r is None or not r.get("passed"):
            hint = NEXT_HINTS.get(m["key"], f"完成 {m['label']}: {m['name']}")
            return hint
    return "🎉 所有 milestone 通过！等候 Panel Review 结果。"


def update_readme(readme: Path, results: dict) -> bool:
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(r"<!-- BEE-STATUS-START -->.*?<!-- BEE-STATUS-END -->", re.DOTALL)

    table = render_status_table(results)
    next_step = determine_next_step(results)
    block = f"""<!-- BEE-STATUS-START -->
# Team · 进度仪表盘

> 由 `.github/workflows/milestone-check.yml` 在每次 push 后自动更新。详细规则见 `BeeFintech 比赛进度系统 spec v3`。

## 📊 进度

{table}

> 图例：✅ 通过 / ❌ 未通过 / ⏳ 尚未运行 · 「必须 🔴」= 不通过将影响硬规则评分

## 🎯 下一步

{next_step}

<!-- BEE-STATUS-END -->"""

    new_text = pattern.sub(block, text)
    if new_text == text:
        return False
    readme.write_text(new_text, encoding="utf-8")
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", type=Path, required=True)
    ap.add_argument("--readme", type=Path, default=Path("README.md"))
    args = ap.parse_args()

    results = json.loads(args.states.read_text(encoding="utf-8"))
    changed = update_readme(args.readme, results)
    print(f"README 已更新：{changed}")
