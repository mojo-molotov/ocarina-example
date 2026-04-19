"""Act function."""

from contextlib import suppress
from typing import TYPE_CHECKING

from ocarina.dsl.testing_with_railway.constructors.create_act import create_act
from ocarina.opinionated.infra.act_counter import ActCounter
from ocarina.railway.result import Fail

from lib.custom_errors.http import HttpErrorPageReachedError
from lib.ext.ocarina.regex.error_page import ERROR_PAGE_REGEX

if TYPE_CHECKING:
    from collections.abc import Callable

    from ocarina.custom_types.tpom import TPOM
    from ocarina.dsl.testing_with_railway.internals.action_chain import ActionStart


def act(pom: TPOM, action: Callable[[TPOM], TPOM]) -> ActionStart[TPOM]:
    """Act on a page."""

    def failure_hook(pom: TPOM, exc: Exception) -> Fail:
        with suppress(Exception):
            title = pom.get_current_title()
            is_http_error_page = title and ERROR_PAGE_REGEX.match(title.strip())
            if is_http_error_page:
                http_error = HttpErrorPageReachedError(f"HTTP error page: {title}")
                http_error.__cause__ = exc
                return Fail(error=http_error)
        return Fail(error=exc)

    return create_act(
        pom,
        action,
        on_failure=failure_hook,
        on_run_effect=lambda: ActCounter().incr_act_call_count(),
    )
