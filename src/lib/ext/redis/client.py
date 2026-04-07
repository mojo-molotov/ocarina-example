"""Redis client Singleton."""

from threading import Lock

import redis as _redis
from ocarina.opinionated.loggers.create_matching_logger import create_matching_logger

from constants.sys.redis_keys import REDIS_ENV_KILLSWITCH
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters

_init_lock = Lock()
_redis_client: _redis.StrictRedis | None = None
_initialized = False


def _log_redis_unavailable_msg() -> None:
    create_matching_logger("terminal").warning("Redis unavailable!")


def _log_redis_killswitch_msg() -> None:
    create_matching_logger("terminal").warning("Redis killswitch triggered!")


def get_redis_client() -> _redis.StrictRedis | None:
    """Redis client Singleton."""
    global _redis_client, _initialized  # noqa: PLW0603

    if _initialized:
        return _redis_client

    with _init_lock:
        if _initialized:
            return _redis_client

        try:
            redis_url = create_env_getters().get_value("redis_url")
            if redis_url == REDIS_ENV_KILLSWITCH:
                _log_redis_killswitch_msg()
                return None
            client = _redis.StrictRedis.from_url(redis_url)
            client.ping()
            _redis_client = client
        except Exception:  # noqa: BLE001
            _log_redis_unavailable_msg()
        finally:
            _initialized = True

    return _redis_client


def warmup_redis_client() -> None:
    """Warmup Redis client."""
    get_redis_client()
