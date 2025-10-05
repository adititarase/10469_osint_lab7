import os
from dotenv import load_dotenv

load_dotenv()
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
MASTODON_API_BASE_URL = os.getenv("MASTODON_API_BASE_URL", "https://mastodon.social")

# Initialize Mastodon client only if credentials are available
mastodon = None
if MASTODON_ACCESS_TOKEN:
    try:
        from mastodon import Mastodon 
        mastodon = Mastodon( 
            access_token=MASTODON_ACCESS_TOKEN, 
            api_base_url=MASTODON_API_BASE_URL 
        )
    except Exception as e:
        mastodon = None

def fetch_mastodon(hashtag="osint", limit=10): 
    if not mastodon:
        return []
    
    try:
        results = [] 
        posts = mastodon.timeline_hashtag(hashtag, limit=limit)  
        for p in posts: 
            results.append({ 
                "platform": "mastodon", 
                "user": p["account"]["username"], 
                "timestamp": str(p["created_at"]), 
                "text": p["content"],
                "url": p["url"] 
            }) 
        return results
    except Exception as e:
        return [] 
