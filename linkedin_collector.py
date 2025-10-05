import os
from dotenv import load_dotenv

load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def fetch_linkedin(keyword="cybersecurity", limit=10):  
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        return []
    
    try:
        from linkedin_api import Linkedin 
        api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
        results = [] 
        people = api.search_people(keyword=keyword, limit=limit)  
        for p in people: 
            results.append({ 
                "platform": "linkedin", 
                "user": p.get("public_id", ""), 
                "timestamp": "N/A", 
                "text": p.get("headline", ""), 
                "url": f"https://linkedin.com/in/{p.get('public_id','')}"  
            }) 
        return results
    except Exception as e:
        return []
