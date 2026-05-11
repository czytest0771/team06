"""Layer-2 AI Review：DeepSeek v4-pro 读 docs 并发反馈。

DeepSeek API 是 OpenAI 兼容协议，用 openai SDK + 自定义 base_url。
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

PROMPT_TEMPLATE = """你是 BeeFintech Vibe Coding 比赛的 AI Reviewer。
当前评审 Milestone: {milestone}
当前评审 Team: {team_id}

请阅读以下文件内容并给出建设性反馈：

```
{file_content}
```

**输出格式（三段都必须有，缺一不可）：**

【整体】1-2 句总体评价（≤ 80 字）

【建议】列 2-3 个具体可行的改进点（每点 ≤ 60 字，标号 1./2./3.）

【评估】必须以 `X/5 分` 起头给出 1-5 分整数或半分（如 `3/5 分` 或 `3.5/5 分`），后接一句话总结，不超过 30 字。
⚠️ 严格遵守此格式，否则输出无效。示例：`3.5/5 分。整体方向可行，但浏览器兼容与 API 集成需补强。`

**评分标准（参考）：**
- 1/5 = 几乎未完成 milestone 要求
- 2/5 = 完成基础但缺关键内容
- 3/5 = 中规中矩，核心要求基本覆盖
- 4/5 = 完整且对比赛核心点（移动端 / 浏览器兼容 / 指定 API）有具体方案
- 5/5 = 完整 + 创新 + 全部硬性要求都已落地

**其他要求：**
- 中文输出
- 不要溢美，专注问题
- 必须提及官方核心要求：移动端适配 / 浏览器兼容 / 调用指定 API
- 若发现严重缺漏，明确指出
"""


def review(milestone: str, team_id: str, file_path: Path) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    content = file_path.read_text(encoding="utf-8")
    if len(content) > 20000:
        content = content[:20000] + "\n\n[...truncated...]"
    msg = client.chat.completions.create(
        model="deepseek-v4-pro",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": PROMPT_TEMPLATE.format(
                milestone=milestone, team_id=team_id, file_content=content
            ),
        }],
    )
    return msg.choices[0].message.content


def check_budget(repo_dir: Path, milestone: str) -> bool:
    """每个 (team, milestone) 最多 1 次 AI review。"""
    state_file = repo_dir / ".bee-state" / "ai-review-state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state = {}
    if state_file.exists():
        state = json.loads(state_file.read_text())
    used = state.get(milestone, 0)
    if used >= 1:
        return False
    state[milestone] = used + 1
    state_file.write_text(json.dumps(state, indent=2))
    return True


MILESTONE_FILE_MAP = {
    "m3":  ("docs/design.md",          "设计文档"),
    "m4":  ("docs/plan.md",            "实施计划"),
    "m8a": ("docs/test.md",            "测试文档"),
    "m8b": ("docs/ai-collab-log.md",   "AI 协作记录"),
    "m8c": ("docs/retrospective.md",   "复盘文档"),
}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--milestone", required=True, choices=sorted(MILESTONE_FILE_MAP.keys()))
    ap.add_argument("--team-id", required=True)
    ap.add_argument("--repo-dir", type=Path, default=Path("."))
    ap.add_argument(
        "--skip-budget",
        action="store_true",
        help="跳过配额检查（管理员侧 workflow_dispatch 用，不消耗 team 自己的 /review 名额）",
    )
    args = ap.parse_args()

    rel_path, _doc_label = MILESTONE_FILE_MAP[args.milestone]
    fp = args.repo_dir / rel_path
    if not fp.exists():
        print(f"❌ {fp} 不存在")
        sys.exit(1)

    if not args.skip_budget:
        if not check_budget(args.repo_dir, args.milestone):
            print(f"⚠️ {args.milestone} 配额已用完；跳过。")
            sys.exit(0)

    feedback = review(args.milestone, args.team_id, fp)
    tag = " · [admin dispatch]" if args.skip_budget else ""
    print(f"## 🤖 Bee AI Review · {args.milestone.upper()} · {args.team_id}{tag}\n\n{feedback}")
