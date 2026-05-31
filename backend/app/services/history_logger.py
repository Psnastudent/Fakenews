import json
import os
from datetime import datetime
import uuid

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")

def _load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_history(data):
    # Ensure directory exists
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_check(check_type: str, content: str, verdict: str):
    """
    Log an analysis check to history.
    """
    history = _load_history()
    
    # Truncate content for display
    display_content = content
    if len(display_content) > 100:
        display_content = display_content[:97] + "..."
        
    entry = {
        "id": str(uuid.uuid4()),
        "type": check_type,
        "content": display_content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "verdict": "FAKE" if verdict.lower() == "fake" else "REAL"
    }
    
    # Insert at beginning
    history.insert(0, entry)
    
    # Keep only last 100
    if len(history) > 100:
        history = history[:100]
        
    _save_history(history)
    return entry

def get_history(limit: int = 50):
    """
    Retrieve history.
    """
    history = _load_history()
    return history[:limit]
