"""Redis client Singleton."""

from threading import Lock

import redis as _redis

from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters

_init_lock = Lock()
_redis_client: _redis.StrictRedis | None = None


def get_redis_client() -> _redis.StrictRedis:
    """Redis client Singleton."""
    global _redis_client  # noqa: PLW0603

    if _redis_client is not None:
        return _redis_client

    with _init_lock:
        if _redis_client is not None:
            return _redis_client

        redis_url = create_env_getters().get_value("redis_url")
        client = _redis.StrictRedis.from_url(redis_url)
        client.ping()
        _redis_client = client

    return _redis_client


def warmup_redis_client() -> None:
    """Warmup Redis client."""
    get_redis_client()
