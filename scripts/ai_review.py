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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--milestone", required=True, choices=["m3", "m4"])
    ap.add_argument("--team-id", required=True)
    ap.add_argument("--repo-dir", type=Path, default=Path("."))
    args = ap.parse_args()

    file_map = {
        "m3": args.repo_dir / "docs" / "design.md",
        "m4": args.repo_dir / "docs" / "plan.md",
    }
    fp = file_map[args.milestone]
    if not fp.exists():
        print(f"❌ {fp} 不存在")
        sys.exit(1)

    if not check_budget(args.repo_dir, args.milestone):
        print(f"⚠️ {args.milestone} 配额已用完；跳过。")
        sys.exit(0)

    feedback = review(args.milestone, args.team_id, fp)
    print(f"## 🤖 Bee AI Review · {args.milestone.upper()} · {args.team_id}\n\n{feedback}")
