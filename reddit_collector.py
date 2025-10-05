import os
import praw
import requests
from dotenv import load_dotenv

load_dotenv()
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")

# Initialize Reddit client if credentials are available
reddit = None
if REDDIT_ID and REDDIT_SECRET:
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="osint_pipeline/1.0"
        )
    except Exception:
        reddit = None


def _fetch_reddit_via_json(subreddit: str, limit: int):
    """Public, no-auth fallback using Reddit JSON endpoint."""
    try:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
        params = {"limit": max(1, min(50, limit))}
        headers = {"User-Agent": "osint-pipeline/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        results = []
        for child in data.get("data", {}).get("children", [])[:limit]:
            post = child.get("data", {})
            results.append({
                "platform": "reddit",
                "user": str(post.get("author", "N/A")),
                "timestamp": str(post.get("created_utc", "N/A")),
                "text": f"{post.get('title','')} {post.get('selftext','')}",
                "url": f"https://reddit.com{post.get('permalink','')}"
            })
        return results
    except requests.exceptions.RequestException:
        return []


def fetch_reddit(subreddit="technology", limit=20):
    # Prefer official API if configured
    if reddit is not None:
        try:
            results = []
            for post in reddit.subreddit(subreddit).hot(limit=limit):
                results.append({
                    "platform": "reddit",
                    "user": str(post.author),
                    "timestamp": str(post.created_utc),
                    "text": (post.title or "") + " " + (post.selftext or ""),
                    "url": f"https://reddit.com{post.permalink}"
                })
            if results:
                return results
        except Exception:
            pass

    # Fallback to public JSON
    return _fetch_reddit_via_json(subreddit, limit)

