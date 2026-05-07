"""Layer-1 里程碑硬规则校验。

每个函数返回 MilestoneStatus(passed, message, details)。
被 .github/workflows/milestone-check.yml 在每次 push 到 main 时调用。
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import yaml


@dataclass
class MilestoneStatus:
    passed: bool
    message: str
    details: dict | None = None


def check_m1_team_yml(path: Path) -> MilestoneStatus:
    """M1：team.yml 字段齐全 + members ≥ 2 个不同办公室。"""
    if not path.exists():
        return MilestoneStatus(False, "team.yml 不存在")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return MilestoneStatus(False, f"team.yml 解析失败: {e}")

    if not data.get("team_name"):
        return MilestoneStatus(False, "team_name 不能为空")
    if not data.get("pioneer_lead"):
        return MilestoneStatus(False, "pioneer_lead 不能为空")

    members = data.get("members") or []
    if len(members) < 3:
        return MilestoneStatus(False, f"队员至少 3 人（当前 {len(members)} 人）")

    for i, m in enumerate(members, 1):
        for field in ("name", "office", "github_username"):
            if not m.get(field):
                return MilestoneStatus(False, f"成员 #{i} 缺少 {field}")

    offices = {m["office"] for m in members}
    if len(offices) < 2:
        return MilestoneStatus(
            False,
            f"至少 2 个不同办公室（当前: {', '.join(offices)}）",
        )

    return MilestoneStatus(
        True,
        f"M1 通过：{len(members)} 人，{len(offices)} 个不同办公室",
        {"members_count": len(members), "offices": list(offices)},
    )


REQUIRED_DESIGN_SECTIONS = [
    "目标",
    "页面架构",
    "核心功能",
    "Tech Stack",
    "移动端适配",
]


def check_m3_design_md(path: Path) -> MilestoneStatus:
    """M3：design.md 含 marker + 5 个必填章节。"""
    if not path.exists():
        return MilestoneStatus(False, "design.md 不存在")

    text = path.read_text(encoding="utf-8")

    if "<!-- generated-by: superpowers-brainstorming -->" not in text:
        return MilestoneStatus(
            False,
            "design.md 缺少 marker `<!-- generated-by: superpowers-brainstorming -->`（必须用 superpower 技能生成）",
        )

    missing = []
    for section in REQUIRED_DESIGN_SECTIONS:
        pattern = re.compile(r"^#{1,3}\s*\d*\.?\s*" + re.escape(section), re.MULTILINE)
        if not pattern.search(text):
            missing.append(section)

    if missing:
        return MilestoneStatus(
            False,
            f"design.md 缺少必填章节: {', '.join(missing)}",
        )

    return MilestoneStatus(True, "M3 通过：5 必填章节齐全 + marker 存在")


def check_m4_plan_md(path: Path) -> MilestoneStatus:
    """M4：plan.md 含 marker + ≥ 4 个 Phase。"""
    if not path.exists():
        return MilestoneStatus(False, "plan.md 不存在")

    text = path.read_text(encoding="utf-8")

    if "<!-- generated-by: superpowers-writing-plans -->" not in text:
        return MilestoneStatus(
            False,
            "plan.md 缺少 marker `<!-- generated-by: superpowers-writing-plans -->`",
        )

    phase_pattern = re.compile(r"^#{1,3}\s*Phase\s+\d+", re.MULTILINE | re.IGNORECASE)
    phases = phase_pattern.findall(text)
    if len(phases) < 4:
        return MilestoneStatus(
            False,
            f"plan.md 至少 4 个 Phase（当前 {len(phases)}）",
        )

    return MilestoneStatus(True, f"M4 通过：{len(phases)} 个 Phase")


def check_m7_branches(repo_dir: Path) -> MilestoneStatus:
    """M7+：≥ 2 个分支，含 main 且至少 1 个非 main 分支有 commit。"""
    try:
        result = subprocess.run(
            ["git", "branch", "-r"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        branches = [
            b.strip().replace("origin/", "")
            for b in result.stdout.splitlines()
            if "HEAD" not in b
        ]
        non_main = [b for b in branches if b != "main"]
        if len(branches) < 2 or not non_main:
            return MilestoneStatus(
                False,
                f"至少需要 2 个分支（含 main + 1 个 feature/dev 分支），当前: {branches}",
            )
        return MilestoneStatus(True, f"M7+ 通过：分支 {branches}")
    except subprocess.CalledProcessError as e:
        return MilestoneStatus(False, f"git branch 命令失败: {e}")


def check_doc_min_length(path: Path, min_chars: int, label: str) -> MilestoneStatus:
    """通用文档字数校验（M8a/b/c）。"""
    if not path.exists():
        return MilestoneStatus(False, f"{label} 不存在: {path}")
    content = path.read_text(encoding="utf-8").strip()
    if len(content) < min_chars:
        return MilestoneStatus(
            False,
            f"{label} 字数不足（当前 {len(content)}，要求 ≥ {min_chars}）",
        )
    return MilestoneStatus(True, f"{label} 通过：{len(content)} 字符")


if __name__ == "__main__":
    import argparse, json, sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--milestone", required=True, choices=["m1", "m3", "m4", "m7", "m8a", "m8b", "m8c", "all"])
    args = ap.parse_args()

    repo = args.repo
    results = {}

    if args.milestone in ("m1", "all"):
        results["m1"] = check_m1_team_yml(repo / "team.yml")
    if args.milestone in ("m3", "all"):
        results["m3"] = check_m3_design_md(repo / "docs" / "design.md")
    if args.milestone in ("m4", "all"):
        results["m4"] = check_m4_plan_md(repo / "docs" / "plan.md")
    if args.milestone in ("m7", "all"):
        results["m7"] = check_m7_branches(repo)
    if args.milestone in ("m8a", "all"):
        results["m8a"] = check_doc_min_length(repo / "docs" / "test.md", 300, "M8a 测试文档")
    if args.milestone in ("m8b", "all"):
        results["m8b"] = check_doc_min_length(repo / "docs" / "ai-collab-log.md", 500, "M8b AI 协作记录")
    if args.milestone in ("m8c", "all"):
        results["m8c"] = check_doc_min_length(repo / "docs" / "retrospective.md", 500, "M8c 复盘文档")

    out = {
        k: {"passed": v.passed, "message": v.message, "details": v.details}
        for k, v in results.items()
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if any(not v.passed for v in results.values()):
        sys.exit(1)
