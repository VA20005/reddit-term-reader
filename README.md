# reddit-term-reader
# Personal Reddit Term Reader

A small, **read-only** Python script for personal learning.

I'm a physician learning software engineering and AI tools. Posts in communities like r/ClaudeAI are full of jargon I don't yet know. Once a day this script saves the top and newest posts (with their top comments) from a few public subreddits to a local Markdown file, which I then review privately with an AI assistant that explains the unfamiliar terms.

## What it does / doesn't do

- ✅ Reads public posts and top-level comments from: r/ClaudeAI, r/ClaudeCode, r/learnprogramming, r/ExperiencedDevs
- ✅ Runs once a day on my own computer, under 100 API requests/day
- ✅ Uses the official Reddit Data API via PRAW (app type: script) with a proper User-Agent
- ❌ No posting, commenting, voting, or messaging (`read_only = True`)
- ❌ No collection of user profiles or personal data
- ❌ Data is not shared, sold, published, or used to train AI models
- ❌ No commercial use

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill in your Reddit app credentials
python reddit_reader.py
```

Output is saved to `digests/reddit-digest-YYYY-MM-DD.md`.

## Compliance

Built to follow Reddit's Data API Terms and Responsible Builder Policy. Credentials are kept in a local `.env` file that is never committed.
