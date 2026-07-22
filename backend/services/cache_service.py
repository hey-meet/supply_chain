# Week 3 Day 4: High-Performance Response Caching Layer
import time

_CACHE = {}
CACHE_TTL = 30  # seconds

def get_cached_or_compute(key: str, compute_func):
    now = time.time()
    if key in _CACHE:
        val, timestamp = _CACHE[key]
        if now - timestamp < CACHE_TTL:
            return val
    computed = compute_func()
    _CACHE[key] = (computed, now)
    return computed
