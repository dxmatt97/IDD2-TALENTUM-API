from datetime import datetime
from app.config.db import redis_client

def log_recent_action(action_description: str):
    key = "global:recent_actions"
    redis_client.lpush(key, f"{datetime.utcnow().isoformat()}: {action_description}")
    redis_client.ltrim(key, 0, 9)
