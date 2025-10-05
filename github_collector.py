import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github(query="leak", limit=5):
    """
    Fetch GitHub repositories using GitHub REST API
    """
    try:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'osint-pipeline/1.0'
        }
        
        # Add authorization if token is available
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
        # Search repositories
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": max(1, min(50, limit))
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        if response.status_code != 200:
            # Common causes: missing/invalid token, missing User-Agent, rate limiting (403/429)
            print(f"GitHub API Error: HTTP {response.status_code}")
            return []
        
        data = response.json()
        results = []
        
        # Extract repositories from the response
        for repo in data.get('items', [])[:limit]:
            results.append({
                "platform": "github",
                "user": repo['owner']['login'],
                "timestamp": repo['created_at'],
                "text": f"{repo['name']}: {repo['description']}" if repo['description'] else repo['name'],
                "url": repo['html_url']
            })
            
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {e}")
        return []