import redis
import json
from config.app_config import config


class CacheRepository:
    def __init__(self, host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key, value):        
        # Serialize complex data types
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        self.redis.set(key, value, ex=config.CACHE_TTL)

    def get(self, key):
        value = self.redis.get(key)
        if value is None:
            return None
            
        # Try to deserialize JSON
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def delete(self, key):
        return self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)

    def delete_pattern(self, pattern):
        keys = self.redis.keys(pattern)
        if keys:
            return self.redis.delete(*keys)
        return 0
    
cache_repository = CacheRepository()