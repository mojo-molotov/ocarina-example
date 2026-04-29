"""L1 caches."""

from dogpile.cache import make_region

in_memory_cache_with_30m_ttl = make_region().configure(
    "dogpile.cache.memory", expiration_time=30 * 60
)
