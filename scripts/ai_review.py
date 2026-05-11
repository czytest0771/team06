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

请阅读以下文件内容并给出 100-200 字的建设性反馈：

```
{file_content}
```

反馈格式：
【整体】1-2 句总体评价
【建议】2-3 个具体可行的改进点
【评估】1-5 分可行性评分 + 一句话总结

要求：
- 中文输出
- 不要溢美，专注问题
- 提醒官方核心要求：移动端适配 / 浏览器兼容 / 调用指定 API
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
        max_tokens=600,
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
