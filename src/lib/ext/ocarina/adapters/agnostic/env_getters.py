"""Env getters, intended to be quickly changed if required."""

import os
from types import MappingProxyType
from typing import TYPE_CHECKING, Literal

from ocarina.opinionated.infra.env import EnvGetters

if TYPE_CHECKING:
    from ocarina.custom_types.effect import Effects

type _CredsKeys = Literal["dashboard"]
type _ValuesKeys = Literal["igor_api_key", "redis_url"]


def _load_env() -> None:
    from dotenv import load_dotenv  # noqa: PLC0415

    load_dotenv()


_DEFAULT_EFFECTS = (_load_env,)


class _EnvGetters(EnvGetters[_CredsKeys, _ValuesKeys]):
    def __init__(self, *, effects: Effects) -> None:
        for effect in effects:
            effect()

        super().__init__(
            credentials={
                "dashboard": MappingProxyType(
                    {
                        "login": os.environ["DASH_USERNAME"],
                        "password": os.environ["DASH_PASSWORD"],
                    }
                ),
            },
            values={
                "igor_api_key": os.environ["IGOR_API_KEY"],
                "redis_url": os.environ["REDIS_URL"],
            },
        )


def create_env_getters(*, effects: Effects | None = None) -> _EnvGetters:
    """Create a fresh EnvGetter instance."""
    if effects is None:
        effects = _DEFAULT_EFFECTS
    return _EnvGetters(effects=effects)
