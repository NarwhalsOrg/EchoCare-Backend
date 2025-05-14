import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_EXPIRE_SECONDS = 1800  # 30 minutes

# Create the Redis client (decode_responses=True for string values)
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def save_session(session_id: str, data: dict):
    """
    Save user/session data to Redis with expiry.
    """
    r.setex(f"session:{session_id}", SESSION_EXPIRE_SECONDS, json.dumps(data))

def get_session(session_id: str):
    """
    Retrieve user/session data from Redis.
    """
    val = r.get(f"session:{session_id}")
    if val is not None:
        return json.loads(val)
    return None

def delete_session(session_id: str):
    """
    Delete session data from Redis.
    """
    r.delete(f"session:{session_id}")

def refresh_session(session_id: str):
    """
    Refresh expiry time for session.
    """
    r.expire(f"session:{session_id}", SESSION_EXPIRE_SECONDS)
