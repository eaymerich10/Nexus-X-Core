import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def supabase_post(endpoint: str, data: dict):
    response = requests.post(f"{SUPABASE_URL}/rest/v1/{endpoint}", json=data, headers=HEADERS)
    return response

def supabase_get(endpoint: str, params: dict = None):
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{endpoint}?select=*", headers=HEADERS, params=params)
    return response

def supabase_delete(endpoint: str, filter_query: str):
    response = requests.delete(f"{SUPABASE_URL}/rest/v1/{endpoint}?{filter_query}", headers=HEADERS)
    return response
