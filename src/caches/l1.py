"""L1 caches."""

from dogpile.cache import make_region

in_memory_cache_with_300s_ttl = make_region().configure(
    "dogpile.cache.memory", expiration_time=300
)
