# app/database/redis_client.py
import redis
import json
import logging
from typing import Any, Optional


class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        self.logger = logging.getLogger(__name__)

    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
        return None

    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """设置缓存数据"""
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            self.logger.error(f"Cache delete error: {e}")
            return False

    def exists(self, key: str) -> bool:
        """检查缓存键是否存在"""
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            self.logger.error(f"Cache exists check error: {e}")
            return False


# 全局缓存实例
cache = RedisCache()
