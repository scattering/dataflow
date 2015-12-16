import warnings

def lrucache(size):
    try:
        import pylru
        return pylru.lrucache(size)
    except ImportError:
        warnings.warn("pylru not available; using simple cache with no size limit")
        return {}


class MemoryCache:
    """
    In memory cache with redis interface.

    Use this for running tests without having to start up the redis server.
    """
    def __init__(self, size=1000):
        self.cache = lrucache(size)
    def exists(self, key):
        return key in self.cache
    def keys(self):
        return self.cache.keys()
    def delete(self, *key):
        for k in key:
            del self.cache[k]
    def set(self, key, value):
        self.cache[key] = value
    def get(self, key):
        """Note: doesn't provide default value for missing key like dict.get"""
        return self.cache[key]
    __delitem__ = delete
    __setitem__ = set
    __getitem__ = get
    def rpush(self, key, value):
        if key not in self.cache:
            self.cache[key] = [value]
        else:
            self.cache[key].append(value)
    def lrange(self, key, low, high):
        return self.cache[key][low:(high+1 if high != -1 else None)]


def memory_cache():
    return MemoryCache()


# port 6379 is the default port value for the python redis connection
def redis_connect(host="localhost", port=6379, **kwargs):
    """
    Open a redis connection.

    If host is localhost, then try starting the redis server.

    If redis is unavailable, then return a simple dict cache.
    """
    import redis  # lazy import so that redis need not be available

    # ensure redis is running, at least if we are not on a windows box
    if host == "localhost" and not sys.platform=='win32':
        os.system("nohup redis-server --maxmemory 4gb --maxmemory-policy --port %d allkeys-lru > /dev/null 2>&1 &"
                  % port)

    cache = redis.Redis(host=host, port=port, **kwargs)

    try:
        cache.info()
    except redis.ConnectionError as exc:
        warnings.warn("""\
Redis connection failed with:
    %s
Falling back to in-memory cache."""%str(exc))
        cache = memory_cache()

    return cache

class CacheManager:
    def __init__(self):
        self._cache = None
        self._redis_kwargs = None
    def use_redis(self, **kwargs):
        if self._cache is not None:
            raise RuntimeError("call use_redis() before cache is first used")
        self._redis_kwargs = kwargs
    def get_cache(self):
        if self._cache is None:
            if self._redis_kwargs is not None:
                self._cache = redis_connect(**self._redis_kwargs)
            else:
                self._cache = memory_cache()
        return self._cache

# Singleton cache manager if you only need one cache
CACHE_MANAGER = CacheManager()

# direct access to singleton methods
use_redis = CACHE_MANAGER.use_redis
get_cache = CACHE_MANAGER.get_cache

