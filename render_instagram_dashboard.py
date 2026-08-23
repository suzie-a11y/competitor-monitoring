#!/usr/bin/env python3
"""Render the latest Instagram run into the static dashboard."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "data" / "instagram_runs"
DASHBOARD = ROOT / "dashboard.html"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def newest_run() -> tuple[Path, dict] | tuple[None, None]:
    files = sorted(RUNS.glob("*.json"))
    if not files:
        return None, None
    path = files[-1]
    return path, json.loads(path.read_text(encoding="utf-8"))


def render(run: dict) -> str:
    rows: list[str] = []
    for brand in run.get("brands", []):
        posts = brand.get("posts", [])
        if posts:
            content = "<br>".join(
                f'<a class="source" href="{esc(post["url"])}" target="_blank" rel="noopener">'
                f'{esc(post.get("published_at", ""))[:16]} · {esc(post.get("content_type", "Post"))} · 打开原帖 →</a>'
                f'<br><span class="note">{esc(post.get("title") or "（未取得正文）")}</span>'
                for post in posts
            )
            signal = "已取得原帖，可进入日报分析内容主题和释放信号"
            status_class = "ok"
            status = "已验证"
        else:
            content = f'<a class="source" href="{esc(brand["profile_url"])}" target="_blank" rel="noopener">打开账号主页 →</a>'
            signal = esc(brand.get("reason") or "不能据此判断没有更新")
            status_class = "unverified"
            status = esc(brand.get("status") or "不可验证")
        rows.append(
            f'<tr><td><b>{esc(brand["brand"])}</b><br><span class="market">{esc(brand["market"])}</span></td>'
            f'<td><a class="source" href="{esc(brand["profile_url"])}" target="_blank" rel="noopener">@{esc(brand["username"])}</a></td>'
            f'<td class="status {status_class}">{status}<br>{content}</td>'
            f'<td>{signal}</td></tr>'
        )
    date = esc(run.get("run_date", ""))
    verified = esc(run.get("verified_posts", 0))
    return f'''<section class="panel"><h2>Instagram 每日更新 · {date}</h2>
    <table><thead><tr><th>品牌 / 区域</th><th>账号</th><th>过去 24 小时帖子</th><th>状态 / 信号</th></tr></thead>
    <tbody>{"".join(rows)}</tbody></table>
    <p class="note">本轮取得可验证 Instagram 原帖 {verified} 条。账号主页仅用于账号确认；已验证内容使用 /p/ 或 /reel/ 原帖链接。</p></section>'''


def main() -> int:
    _, run = newest_run()
    if not run or not DASHBOARD.exists():
        return 0
    content = DASHBOARD.read_text(encoding="utf-8")
    section = render(run)
    pattern = r'<section class="panel"><h2>Instagram 每日更新.*?</section>'
    updated, count = re.subn(pattern, section, content, count=1, flags=re.DOTALL)
    if count == 0:
        raise SystemExit("Instagram dashboard section not found")
    DASHBOARD.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    main()
