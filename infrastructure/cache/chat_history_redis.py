from langchain_redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import os


def get_redis(session_id: str) -> BaseChatMessageHistory | None:
    redis_url = os.getenv("REDIS_URL","")
    if redis_url == "":
        return None
    try:
        time_hour = 3600
        return RedisChatMessageHistory(session_id, redis_url=redis_url, ttl=time_hour)
    except Exception:
        return None