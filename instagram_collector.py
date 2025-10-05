import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Official Meta Graph API credentials
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")  # long-lived access token
IG_USER_ID = os.getenv("IG_USER_ID")            # Instagram Business/Creator user id
INSTAGRAM_DEBUG = os.getenv("INSTAGRAM_DEBUG", "false").lower() in ("1", "true", "yes")


def fetch_instagram(hashtag="gaming", limit=5):
    """
    Fetch Instagram posts using the official Meta Graph API via hashtag search.
    Requirements:
      - Instagram Business/Creator account connected to a Facebook Page
      - Permissions: instagram_basic, pages_show_list, instagram_manage_insights, instagram_manage_comments
      - Environment variables: INSTAGRAM_TOKEN, IG_USER_ID
    """
    if not INSTAGRAM_TOKEN or not IG_USER_ID:
        return []

    try:
        # 1) Resolve hashtag id
        search_url = "https://graph.facebook.com/v19.0/ig_hashtag_search"
        search_params = {
            "user_id": IG_USER_ID,
            "q": hashtag,
            "access_token": INSTAGRAM_TOKEN,
        }
        search_resp = requests.get(search_url, params=search_params, timeout=20)
        if INSTAGRAM_DEBUG:
            try:
                print("[IG] hashtag_search status:", search_resp.status_code, search_resp.text[:400])
            except Exception:
                pass
        if search_resp.status_code != 200:
            return []
        search_data = search_resp.json()
        hashtag_id = None
        if isinstance(search_data, dict):
            data_list = search_data.get("data", [])
            if data_list:
                hashtag_id = data_list[0].get("id")
        if not hashtag_id:
            return []

        # 2) Fetch recent media for the hashtag
        media_url = f"https://graph.facebook.com/v19.0/{hashtag_id}/recent_media"
        media_params = {
            "user_id": IG_USER_ID,
            "fields": "id,caption,permalink,timestamp,media_type,media_url,like_count,comments_count,children{media_url,media_type}",
            "limit": limit,
            "access_token": INSTAGRAM_TOKEN,
        }
        media_resp = requests.get(media_url, params=media_params, timeout=20)
        if INSTAGRAM_DEBUG:
            try:
                print("[IG] recent_media status:", media_resp.status_code, media_resp.text[:400])
            except Exception:
                pass

        media_data = None
        if media_resp.status_code == 200:
            tmp = media_resp.json()
            if isinstance(tmp, dict) and tmp.get("data"):
                media_data = tmp

        # Fallback to top_media if recent_media failed or empty
        if media_data is None:
            top_url = f"https://graph.facebook.com/v19.0/{hashtag_id}/top_media"
            top_resp = requests.get(top_url, params=media_params, timeout=20)
            if INSTAGRAM_DEBUG:
                try:
                    print("[IG] top_media status:", top_resp.status_code, top_resp.text[:400])
                except Exception:
                    pass
            if top_resp.status_code != 200:
                return []
            media_data = top_resp.json()

        results = []
        for item in media_data.get("data", [])[:limit]:
            results.append({
                "platform": "instagram",
                "user": "N/A",  # Graph API does not return author username here
                "timestamp": item.get("timestamp"),
                "text": item.get("caption", ""),
                "url": item.get("permalink", ""),
            })

        return results

    except requests.exceptions.RequestException:
        return []