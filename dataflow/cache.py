class MemoryCache:
    """
    In memory cache with redis interface.

    Use this for running tests without having to start up the redis server.
    """
    def __init__(self):
        self.cache = {}
    def exists(self, key):
        return key in self.cache
    def keys(self):
        return self.cache.keys()
    def set(self, key, value):
        self.cache[key] = value
    def rpush(self, key, value):
        self.cache.setdefault(key,[]).append(value)
    def lrange(self, key, low, high):
        return self.cache[key][low:high]

def memory_cache():
    return MemoryCache()

class CacheManager:
    def __init__(self):
        self._cache = None
        self._redis_host = None
    def use_redis(self, host="localhost"):
        if self._cache is not None:
            raise RuntimeError("redis host must be specified before cache is used")
        self._redis_host = host
    @property
    def cache(self):
        if self._cache is None:
            if self._redis_host is not None:
                import redis
                self._cache = redis.Redis(self._redis_host)
            else:
                self._cache = MemoryCache()
        return self._cache

CACHE_MANAGER = CacheManager()


