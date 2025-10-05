import requests


def fetch_hackernews(query="ai", limit=10):
    """
    Fetch Hacker News stories via the public Algolia API (no key required).
    """
    try:
        url = "https://hn.algolia.com/api/v1/search"
        params = {
            "query": query,
            "tags": "story",
            "hitsPerPage": limit,
            "page": 0,
        }
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            return []

        data = response.json()
        results = []
        for hit in data.get("hits", [])[:limit]:
            results.append({
                "platform": "hackernews",
                "user": hit.get("author") or "N/A",
                "timestamp": hit.get("created_at") or "N/A",
                "text": hit.get("title") or "",
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID','')}",
            })

        return results

    except requests.exceptions.RequestException:
        return []


