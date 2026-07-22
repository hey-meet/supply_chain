from backend.services.cache_service import get_cached_or_compute

def test_cache_hit():
    val1 = get_cached_or_compute("item_101", lambda: {"stock": 500})
    val2 = get_cached_or_compute("item_101", lambda: {"stock": 999})
    assert val1["stock"] == 500
    assert val2["stock"] == 500
