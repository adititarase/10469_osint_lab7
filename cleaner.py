from langdetect import detect, DetectorFactory
import re 

# Set seed for consistent results
DetectorFactory.seed = 0

def clean_text(text): 
    if text is None:
        return ""
    text = re.sub(r"http\S+", "", text)  # remove URLs 
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # remove symbols  
    text = re.sub(r"\s+", " ", text)  # replace multiple spaces with single space
    return text.strip()

def filter_english(records):
    """
    Filter records to only include English content with comprehensive error handling
    """
    if records is None:
        return []
    
    results = []
    
    for r in records:
        # Skip if record doesn't have a text field or text is None
        if "text" not in r or r["text"] is None:
            continue
            
        text = r["text"]
        platform = (r.get("platform") or r.get("Platform") or "").lower()
        
        # Convert to string if it's not already
        if not isinstance(text, str):
            try:
                text = str(text)
            except:
                continue
                
        # Skip empty strings
        if not text.strip():
            continue
            
        # For short snippets or certain platforms, don't over-filter
        if len(text) < 30 or platform in {"github", "hackernews", "quora"}:
            results.append(r)
            continue

        try:
            lang = detect(text)
            if lang == "en":
                results.append(r)
        except Exception:
            # If detection fails, keep the record instead of dropping it
            results.append(r)
            
    return results