"""
reddit_reader.py — personal, read-only Reddit digest for learning technical terms.

Once a day, reads top and new posts (plus top-level comments) from a few
public subreddits and saves them to a local Markdown file. The file is then
reviewed privately with an AI assistant to explain unfamiliar jargon.

Read-only: no posting, commenting, voting, or messaging.
Low volume: well under 100 API requests per day.
Data stays on the owner's computer; it is not shared, sold, or used for AI training.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import praw
from dotenv import load_dotenv

SUBREDDITS = ["ClaudeAI", "ClaudeCode", "learnprogramming", "ExperiencedDevs"]
POSTS_PER_LISTING = 5      # top-of-day and newest, per subreddit
COMMENTS_PER_POST = 5      # top-level comments only
OUTPUT_DIR = Path(__file__).parent / "digests"


def make_client() -> praw.Reddit:
    load_dotenv()
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET",
                "REDDIT_USERNAME", "REDDIT_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        sys.exit(f"Missing settings in .env: {', '.join(missing)}")

    username = os.environ["REDDIT_USERNAME"]
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=username,
        password=os.environ["REDDIT_PASSWORD"],
        # Reddit's required User-Agent format: <platform>:<app id>:<version> (by /u/<username>)
        user_agent=f"python:personal-term-reader:0.1.0 (by /u/{username})",
    )
    reddit.read_only = True
    return reddit


def format_post(post) -> str:
    created = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
    lines = [
        f"### {post.title}",
        f"r/{post.subreddit.display_name} · {post.score} points · "
        f"{post.num_comments} comments · {created:%Y-%m-%d}",
        f"https://www.reddit.com{post.permalink}",
        "",
    ]
    if post.selftext:
        lines += [post.selftext.strip(), ""]

    post.comment_sort = "top"
    post.comments.replace_more(limit=0)  # skip "load more" stubs; no extra requests
    top_comments = [c for c in post.comments if getattr(c, "body", None)][:COMMENTS_PER_POST]
    if top_comments:
        lines.append("**Top comments:**")
        for c in top_comments:
            body = c.body.strip().replace("\n", " ")
            lines.append(f"- ({c.score} pts) {body}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    reddit = make_client()
    today = datetime.now()
    sections = [f"# Reddit digest — {today:%A, %B %d, %Y}", ""]
    seen = set()

    for name in SUBREDDITS:
        sub = reddit.subreddit(name)
        sections.append(f"## r/{name}\n")
        posts = list(sub.top(time_filter="day", limit=POSTS_PER_LISTING))
        posts += list(sub.new(limit=POSTS_PER_LISTING))
        for post in posts:
            if post.id in seen or post.stickied:
                continue
            seen.add(post.id)
            sections.append(format_post(post))

    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / f"reddit-digest-{today:%Y-%m-%d}.md"
    out.write_text("\n".join(sections), encoding="utf-8")
    print(f"Saved {len(seen)} posts to {out}")


if __name__ == "__main__":
    main()
