import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to initialize Supabase client: {str(e)}")

# Bucket names
AVATAR_BUCKET = "avatars"
PRESCRIPTION_BUCKET = "prescriptions"

# Initialize buckets if they don't exist
def init_buckets():
    try:
        # Check if buckets exist, create them if they don't
        buckets = supabase.storage.list_buckets()
        bucket_names = [bucket["name"] for bucket in buckets]
        
        if AVATAR_BUCKET not in bucket_names:
            supabase.storage.create_bucket(AVATAR_BUCKET, public=False)
        
        if PRESCRIPTION_BUCKET not in bucket_names:
            supabase.storage.create_bucket(PRESCRIPTION_BUCKET, public=False)
            
    except Exception as e:
        print(f"Error initializing buckets: {str(e)}")
        # Continue execution even if bucket creation fails
        # The application will attempt to use the buckets later

# Call this function when the app starts
init_buckets()