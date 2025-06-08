from app.config.db import redis_client

def get_recent_actions(limit: int = 10):
    return redis_client.lrange("global:recent_actions", 0, limit - 1)