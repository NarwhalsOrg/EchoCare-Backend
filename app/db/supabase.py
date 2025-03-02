from supabase import create_client, Client
from app.core.config import settings
from functools import lru_cache

@lru_cache()
def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance.
    Uses LRU cache to avoid creating multiple instances.
    """
    try:
        supabase: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_KEY
        )
        return supabase
    except Exception as e:
        raise Exception(f"Failed to initialize Supabase client: {str(e)}")

def get_supabase_storage():
    """Get the Supabase storage client for file operations"""
    supabase = get_supabase_client()
    return supabase.storage