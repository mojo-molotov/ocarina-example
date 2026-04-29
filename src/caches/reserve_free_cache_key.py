"""Donkey-sausage eaters can't triforce."""

import uuid
from threading import Lock
from typing import TYPE_CHECKING, Final

from dogpile.cache.api import NO_VALUE

if TYPE_CHECKING:
    from dogpile.cache import CacheRegion

_RESERVED_VALUE: Final[str] = "__RESERVED__"
_lock = Lock()


def reserve_free_cache_key(region: CacheRegion) -> str:
    """Generate and reserve a fresh cache key."""
    while True:
        key_candidate = str(uuid.uuid4())

        with _lock:
            if region.get(key_candidate) == NO_VALUE:
                region.set(key_candidate, _RESERVED_VALUE)
                return key_candidate
