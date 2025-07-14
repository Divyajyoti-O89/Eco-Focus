from supabase import create_client
import streamlit as st

@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def save_report(data: dict):
    supabase = get_supabase_client()
    try:
        print(f"Attempting to save: {data}")  # Console log
        response = supabase.table("impact_logs").insert(data).execute()
        print("Save successful:", response)  # Console log
        return response
    except Exception as e:
        print(f"Supabase Error: {e}")  # Console log
        st.error(f"Failed to save: {e}")  # UI display
        return None


def fetch_user_logs(nickname: str):
    supabase = get_supabase_client()
    try:
        response = supabase.table("impact_logs").select("*").eq("nickname", nickname).order("timestamp", desc=True).limit(5).execute()
        return response.data
    except Exception as e:
        print("Supabase Fetch Error:", e)
        return []
