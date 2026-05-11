"""Layer-1 里程碑硬规则校验。

每个函数返回 MilestoneStatus(passed, message, details)。
被 .github/workflows/milestone-check.yml 在每次 push 到 main 时调用。
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import re
import subprocess
import yaml


# 已知模板 hash 黑名单：team 文件 SHA256 命中即视为"未实际编辑"。
# 包含 v1 旧模板（已下发到 10 team repo）+ v2 新骨架模板。
TEMPLATE_HASH_BLACKLIST = {
    "docs/test.md": {
        "d1b41af478830ca7152044d05cea28665129fcc93fd8c93575ee56401e09dbf4",  # v1
        "9dc9577fb2ffb8b45dbb86c70877ffba1bd8170880883261ea68cb34862063df",  # v2
    },
    "docs/ai-collab-log.md": {
        "cdbe6cde0000cb73131d5baf90418e280fe3a0ff8fc1f3c7864a2f2c209a2db2",  # v1
        "9e71da33dc1c7899d6eabffcf28bd8e84132a38d599bb0ff1bdb24fa86ad9fd9",  # v2
    },
    "docs/retrospective.md": {
        "aa2dbea5b30f38dcdb28f4d7ec640e0772c298fdd752d28a7863f11105117a50",  # v1
        "4a3e3a136dc54cdbcaf3d7da65b8154d4725a21c07a848d13dd6bbace916531a",  # v2
    },
}

TEMPLATE_SENTINEL = "TEMPLATE_UNTOUCHED"


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


def check_m2_brainstorm_md(path: Path) -> MilestoneStatus:
    """M2：brainstorm.md 至少 8 个 Q&A 段落（`## Q1:` ~ `## Q8:` 起步）。"""
    if not path.exists():
        return MilestoneStatus(False, "brainstorm.md 不存在")
    text = path.read_text(encoding="utf-8")
    questions = re.findall(r"^#{1,3}\s*Q\d+\s*[:：]", text, re.MULTILINE)
    if len(questions) < 8:
        return MilestoneStatus(
            False,
            f"brainstorm.md 至少 8 个 Q&A（当前 {len(questions)} 个）",
        )
    return MilestoneStatus(True, f"M2 通过：{len(questions)} 个 Q&A")


def check_m4_5_ui_mock(path: Path) -> MilestoneStatus:
    """M4.5：docs/ui-mock/ 下 ≥ 1 个非空设计稿文件（排除 .gitkeep）。"""
    if not path.exists():
        return MilestoneStatus(False, "docs/ui-mock/ 不存在")
    files = [
        p for p in path.iterdir()
        if p.is_file() and p.name != ".gitkeep" and p.stat().st_size > 0
    ]
    if not files:
        return MilestoneStatus(False, "docs/ui-mock/ 下没有非空设计稿文件")
    return MilestoneStatus(
        True,
        f"M4.5 通过：{len(files)} 个设计稿文件",
        {"files": sorted(p.name for p in files)},
    )


SRC_CODE_EXTS = {".html", ".htm", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
SRC_DEPLOY_FILES = ["vercel.json", "netlify.toml", "CNAME", "wrangler.toml", "static.json"]


def _list_src_code(repo_dir: Path) -> list[Path]:
    src = repo_dir / "src"
    if not src.exists() or not src.is_dir():
        return []
    return [p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in SRC_CODE_EXTS]


def _has_deploy_config(repo_dir: Path) -> bool:
    for name in SRC_DEPLOY_FILES:
        if (repo_dir / name).exists():
            return True
    wf_dir = repo_dir / ".github" / "workflows"
    if wf_dir.exists():
        for p in wf_dir.glob("*.yml"):
            text = p.read_text(encoding="utf-8", errors="ignore").lower()
            if "pages" in text or "deploy" in text or "vercel" in text or "netlify" in text:
                return True
    return False


def check_m5_homepage_skeleton(repo_dir: Path) -> MilestoneStatus:
    """M5：src/ 含首页源码 + 部署配置 + 源码中出现 team_name（防 hello world）。"""
    code_files = _list_src_code(repo_dir)
    if not code_files:
        return MilestoneStatus(False, f"src/ 下未找到源码文件（支持: {', '.join(sorted(SRC_CODE_EXTS))}）")

    if not _has_deploy_config(repo_dir):
        return MilestoneStatus(
            False,
            f"未找到部署配置（{', '.join(SRC_DEPLOY_FILES)} 之一，或 .github/workflows 下含 pages/deploy 工作流）",
        )

    team_yml = repo_dir / "team.yml"
    if not team_yml.exists():
        return MilestoneStatus(False, "team.yml 不存在，无法校验首页是否含队名指纹")
    try:
        team_name = (yaml.safe_load(team_yml.read_text(encoding="utf-8")) or {}).get("team_name", "").strip()
    except yaml.YAMLError as e:
        return MilestoneStatus(False, f"team.yml 解析失败: {e}")
    if not team_name:
        return MilestoneStatus(False, "team.yml 缺 team_name，无法校验首页指纹")

    for p in code_files:
        if team_name in p.read_text(encoding="utf-8", errors="ignore"):
            return MilestoneStatus(
                True,
                f"M5 通过：{len(code_files)} 个源码文件，部署配置 OK，首页含队名「{team_name}」",
            )
    return MilestoneStatus(
        False,
        f"src/ 源码中未出现队名「{team_name}」——首页应包含队名（避免空 Hello World）",
    )


def check_m6_core_features(repo_dir: Path) -> MilestoneStatus:
    """M6（宽松）：src/ 任意源码含 <form> + API 调用关键字（fetch/axios/XMLHttpRequest）。"""
    code_files = _list_src_code(repo_dir)
    if not code_files:
        return MilestoneStatus(False, "src/ 下未找到源码文件")

    api_pattern = re.compile(r"\bfetch\s*\(|axios\.|XMLHttpRequest", re.IGNORECASE)
    has_form = False
    has_api = False
    for p in code_files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        if not has_form and re.search(r"<form\b", text, re.IGNORECASE):
            has_form = True
        if not has_api and api_pattern.search(text):
            has_api = True
        if has_form and has_api:
            break

    missing = []
    if not has_form:
        missing.append("<form> 标签（预约表单）")
    if not has_api:
        missing.append("API 调用（fetch / axios / XMLHttpRequest）")
    if missing:
        return MilestoneStatus(False, f"M6 src/ 缺少: {', '.join(missing)}")
    return MilestoneStatus(True, "M6 通过：src/ 含预约表单 + API 调用")


DEPLOY_URL_PATTERN = re.compile(
    r"https?://[\w.-]+\.(?:github\.io|vercel\.app|netlify\.app|pages\.dev|page\.gd|cloudflare\.io|workers\.dev|render\.com|fly\.dev|surge\.sh|web\.app|firebaseapp\.com|gh-pages\.io|com|cn|app|net|io|org|xyz|dev|me|site|tech)(?:/\S*)?",
    re.IGNORECASE,
)


def check_m7_deployment(repo_dir: Path) -> MilestoneStatus:
    """M7：README 含部署 URL + src/ 含 <meta name=viewport>（移动端适配基础）。"""
    readme = repo_dir / "README.md"
    if not readme.exists():
        return MilestoneStatus(False, "README.md 不存在")
    readme_text = readme.read_text(encoding="utf-8")

    url_match = DEPLOY_URL_PATTERN.search(readme_text)
    if not url_match:
        return MilestoneStatus(
            False,
            "README 未包含部署 URL（GitHub Pages / Vercel / Netlify / 自有域名等）",
        )

    code_files = _list_src_code(repo_dir)
    if not code_files:
        return MilestoneStatus(False, "src/ 下未找到源码文件，无法校验移动端适配")
    viewport_pattern = re.compile(r"""<meta\s+name\s*=\s*["']viewport["']""", re.IGNORECASE)
    for p in code_files:
        if viewport_pattern.search(p.read_text(encoding="utf-8", errors="ignore")):
            return MilestoneStatus(
                True,
                f"M7 通过：部署 URL `{url_match.group(0)}`，含 viewport meta",
                {"deployment_url": url_match.group(0)},
            )
    return MilestoneStatus(False, '源码中未发现 <meta name="viewport"> 标签（移动端适配）')


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


def check_doc_min_length(
    path: Path, min_chars: int, label: str, rel_path: str | None = None
) -> MilestoneStatus:
    """通用文档字数校验（M8a/b/c）。

    判定顺序（任一失败即 fail）：
    1. 文件存在
    2. 不含 TEMPLATE_UNTOUCHED sentinel（防止只删字段不删标记）
    3. SHA256 不命中模板 hash 黑名单（防止整篇照抄模板）
    4. 字数 ≥ min_chars
    """
    if not path.exists():
        return MilestoneStatus(False, f"{label} 不存在: {path}")

    raw = path.read_text(encoding="utf-8")

    if TEMPLATE_SENTINEL in raw:
        return MilestoneStatus(
            False,
            f"{label} 仍是模板（请删除顶部 `<!-- {TEMPLATE_SENTINEL} ... -->` 标记后再提交）",
        )

    if rel_path and rel_path in TEMPLATE_HASH_BLACKLIST:
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if digest in TEMPLATE_HASH_BLACKLIST[rel_path]:
            return MilestoneStatus(
                False,
                f"{label} 与原始模板完全一致（未实际编辑）",
            )

    content = raw.strip()
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
    ap.add_argument(
        "--milestone",
        required=True,
        choices=["m1", "m2", "m3", "m4", "m4_5", "m5", "m6", "m7", "m7_plus", "m8a", "m8b", "m8c", "all"],
    )
    args = ap.parse_args()

    repo = args.repo
    results = {}

    if args.milestone in ("m1", "all"):
        results["m1"] = check_m1_team_yml(repo / "team.yml")
    if args.milestone in ("m2", "all"):
        results["m2"] = check_m2_brainstorm_md(repo / "docs" / "brainstorm.md")
    if args.milestone in ("m3", "all"):
        results["m3"] = check_m3_design_md(repo / "docs" / "design.md")
    if args.milestone in ("m4", "all"):
        results["m4"] = check_m4_plan_md(repo / "docs" / "plan.md")
    if args.milestone in ("m4_5", "all"):
        results["m4_5"] = check_m4_5_ui_mock(repo / "docs" / "ui-mock")
    if args.milestone in ("m5", "all"):
        results["m5"] = check_m5_homepage_skeleton(repo)
    if args.milestone in ("m6", "all"):
        results["m6"] = check_m6_core_features(repo)
    if args.milestone in ("m7", "all"):
        results["m7"] = check_m7_deployment(repo)
    if args.milestone in ("m7_plus", "all"):
        results["m7_plus"] = check_m7_branches(repo)
    if args.milestone in ("m8a", "all"):
        results["m8a"] = check_doc_min_length(repo / "docs" / "test.md", 300, "M8a 测试文档", "docs/test.md")
    if args.milestone in ("m8b", "all"):
        results["m8b"] = check_doc_min_length(repo / "docs" / "ai-collab-log.md", 500, "M8b AI 协作记录", "docs/ai-collab-log.md")
    if args.milestone in ("m8c", "all"):
        results["m8c"] = check_doc_min_length(repo / "docs" / "retrospective.md", 500, "M8c 复盘文档", "docs/retrospective.md")

    out = {
        k: {"passed": v.passed, "message": v.message, "details": v.details}
        for k, v in results.items()
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if any(not v.passed for v in results.values()):
        sys.exit(1)
