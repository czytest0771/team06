"""根据 milestone-results.json 更新 README.md 中的 BEE-STATUS 区块。"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ICON = {True: "✅", False: "❌"}
ICON_PENDING = "⏳"

MILESTONE_ORDER = ["m1", "m2", "m3", "m4", "m4_5", "m_peer1", "m5", "m6", "m7", "m7+", "m8a", "m8b", "m8c"]

GUIDES = {
    "m1": "完成 `team.yml` 填写（队名 / 队长 / 成员 / 办公室）",
    "m3": "完成 `docs/design.md`：5 必填章节 + 顶部 marker（必须用 superpower 技能生成）",
    "m4": "完成 `docs/plan.md`：≥ 4 个 Phase + 顶部 marker",
    "m5": "完成 Phase 1：首页骨架（src/）",
    "m6": "完成 Phase 2：核心功能（含预约表单调指定 API）",
    "m7": "完成 Phase 3+4：内容页 + polish + 部署 URL（写到 README）",
    "m7+": "确保 GitHub 至少 2 个分支（main + feature/dev），都有提交",
    "m8a": "完成 `docs/test.md`（≥ 300 字）",
    "m8b": "完成 `docs/ai-collab-log.md`（≥ 500 字）",
    "m8c": "完成 `docs/retrospective.md`（≥ 500 字）",
}


def render_status_table(results: dict) -> str:
    cells = []
    for m in MILESTONE_ORDER:
        r = results.get(m.replace("_", "."))
        if r is None:
            cells.append(ICON_PENDING)
        else:
            cells.append(ICON[r["passed"]])
    headers = "| " + " | ".join(m.upper().replace("_", ".") for m in MILESTONE_ORDER) + " |"
    sep = "|" + "|".join(["----"] * len(MILESTONE_ORDER)) + "|"
    row = "| " + " | ".join(cells) + " |"
    return f"{headers}\n{sep}\n{row}"


def determine_next_step(results: dict) -> str:
    for m in MILESTONE_ORDER:
        key = m.replace("_", ".")
        r = results.get(key)
        if r is None or not r["passed"]:
            if m in GUIDES:
                return GUIDES[m]
            continue
    return "🎉 所有 milestone 通过！等候 Panel Review 结果。"


def update_readme(readme: Path, results: dict) -> bool:
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(r"<!-- BEE-STATUS-START -->.*?<!-- BEE-STATUS-END -->", re.DOTALL)

    table = render_status_table(results)
    next_step = determine_next_step(results)
    block = f"""<!-- BEE-STATUS-START -->
# Team · 进度仪表盘

## 📊 进度

{table}

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
