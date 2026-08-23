#!/usr/bin/env python3
"""Collect recent public Instagram posts for the competitor monitor.

This intentionally uses Instaloader without credentials. A failed or blocked
profile is recorded as unverified; it is never converted into "no updates".
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import instaloader


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RUNS = DATA / "instagram_runs"
UPDATES = DATA / "updates.jsonl"

ACCOUNTS = {
    "Spigen": {"market": "Global", "username": "spigen"},
    "BURGA": {"market": "Global", "username": "burgaofficial"},
    "RHINOSHIELD": {"market": "Global", "username": "rhinoshield"},
    "OtterBox": {"market": "Global", "username": "otterbox"},
}


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def post_url(post: instaloader.Post) -> str:
    kind = "reel" if post.is_video else "p"
    return f"https://www.instagram.com/{kind}/{post.shortcode}/"


def existing_keys() -> set[str]:
    keys: set[str] = set()
    if not UPDATES.exists():
        return keys
    for line in UPDATES.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("url"):
            keys.add(item["url"])
        if item.get("dedupe_key"):
            keys.add(item["dedupe_key"])
    return keys


def collect_brand(loader: instaloader.Instaloader, brand: str, config: dict, since: datetime) -> dict:
    username = config["username"]
    result = {
        "brand": brand,
        "market": config["market"],
        "username": username,
        "profile_url": f"https://www.instagram.com/{username}/",
        "checked_at": iso(datetime.now(timezone.utc)),
        "status": "不可验证",
        "reason": "",
        "posts": [],
    }
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        for post in profile.get_posts():
            published = post.date_utc.replace(tzinfo=timezone.utc)
            if published < since:
                break
            result["posts"].append(
                {
                    "brand": brand,
                    "market": config["market"],
                    "platform": "Instagram",
                    "account": username,
                    "published_at": iso(published),
                    "title": (post.caption or "").strip()[:240],
                    "content_type": "Reel" if post.is_video else ("Carousel" if post.typename == "GraphSidecar" else "Post"),
                    "url": post_url(post),
                    "shortcode": post.shortcode,
                    "likes": post.likes,
                    "comments": post.comments,
                    "evidence_level": "官方社媒",
                }
            )
            if len(result["posts"]) >= 30:
                break
        result["status"] = "已验证" if result["posts"] else "已访问但过去24小时未取得帖子"
    except Exception as exc:  # Instaloader errors vary with IG responses.
        result["reason"] = f"公开页面不可验证：{type(exc).__name__}"
    return result


def main() -> int:
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=24)
    today = now.date().isoformat()
    RUNS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    UPDATES.touch()

    loader = instaloader.Instaloader(
        sleep=False,
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        max_connection_attempts=1,
        request_timeout=30,
        fatal_status_codes=[429],
        quiet=True,
    )

    results = [collect_brand(loader, brand, config, since) for brand, config in ACCOUNTS.items()]
    run = {
        "run_date": today,
        "window_start": iso(since),
        "window_end": iso(now),
        "mode": "public_without_login",
        "brands": results,
        "verified_posts": sum(len(item["posts"]) for item in results),
        "unverified_brands": sum(item["status"] == "不可验证" for item in results),
    }
    (RUNS / f"{today}.json").write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")

    seen = existing_keys()
    added = 0
    with UPDATES.open("a", encoding="utf-8") as handle:
        for result in results:
            for post in result["posts"]:
                if post["url"] in seen:
                    continue
                caption = post["title"] or "（未取得正文）"
                item = {
                    **post,
                    "action_type": "Instagram公开更新",
                    "iphone18_relevance": "待分析",
                    "summary": f"Instagram {post['content_type']}：{caption}",
                    "signal": "待日报分析：记录品牌当天的内容主题、产品卖点、促销、联名或用户互动信号。",
                    "dedupe_key": post["url"],
                    "added_on": today,
                }
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
                seen.add(post["url"])
                added += 1

    run["new_updates_appended"] = added
    (RUNS / f"{today}.json").write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"date": today, "new_updates_appended": added, "verified_posts": run["verified_posts"], "unverified_brands": run["unverified_brands"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
