import os 
from dotenv import load_dotenv 

load_dotenv() 
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

# Initialize Telegram client only if credentials are available
client = None
if TELEGRAM_API_ID and TELEGRAM_API_HASH:
    try:
        from telethon import TelegramClient 
        api_id = int(TELEGRAM_API_ID)
        client = TelegramClient("osint_session", api_id, TELEGRAM_API_HASH)
    except Exception as e:
        client = None

async def fetch_telegram(channel="osint_channel", limit=20):  
    if not client:
        return []
    
    try:
        results = [] 
        async for msg in client.iter_messages(channel, limit=limit):
            results.append({ 
                "platform": "telegram", 
                "user": str(msg.sender_id), 
                "timestamp": str(msg.date), 
                "text": msg.text, 
                "url": f"https://t.me/{channel}/{msg.id}"  
            })
        return results
    except Exception as e:
        return [] 
         
