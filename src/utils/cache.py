from cachetools import TTLCache
from threading import RLock
from typing import Any

class TTLCacheWrapper:
    """Thread-safe TTL cache wrapper used by the app."""
    
    def __init__(self, maxsize: int = 1024, ttl: int = 30):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = RLock()

    def get(self, key: str):
        with self._lock:
            return self._cache.get(key)

    def set(self, key: str, value: Any):
        with self._lock:
            self._cache[key] = value

    def clear(self):
        with self._lock:
            self._cache.clear()
