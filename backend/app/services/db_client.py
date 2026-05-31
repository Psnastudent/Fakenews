import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://vhknnhducrjpgjfvxsqf.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_9k2LJBarcfJrZJBnlDx0_A_4_3HqtM3")

# Initialize the Supabase client
# Ensure you set the environment variables in your .env file
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"[!] Supabase initialization failed. Please check your credentials: {e}")
    supabase = None

def save_analysis_result(user_id: str, file_name: str, file_type: str, prediction: str, confidence: int):
    """
    Saves an analysis record to the Supabase database.
    """
    if not supabase:
        print("[!] DB not connected. Skipping save.")
        return None
        
    try:
        data, count = supabase.table('Analysis').insert({
            "user_id": user_id,
            "file_name": file_name,
            "type": file_type,
            "prediction": prediction,
            "confidence": confidence
        }).execute()
        return data
    except Exception as e:
        print(f"[!] Supabase insert failed: {e}")
        return None
