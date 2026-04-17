"""Conditional branching operator for adaptive pages.

Provides match_page() and when() as a DSL extension for handling pages
that can be in multiple states (A/B tests, optional banners, random modals,
maintenance pages, etc.).

Semantics:
    - Evaluates each when() condition in order (first match wins)
    - Executes the matching branch's ChainRunners sequentially
    - If no condition matches: Fail (on failure rail, short-circuits downstream)
    - If a branch's ChainRunner fails: Fail (same short-circuit behaviour)
    - Returns a ChainRunner[Any] — integrates naturally in a scenario's list

Railway behaviour:
    match_page is a ChainRunner like drive_page.
    It composes in a scenario list and participates in the same
    short-circuit logic: if a previous ChainRunner has failed,
    match_page is never executed (caller is responsible for that,
    as with all ChainRunners in Ocarina).

Example:
    >>> def scenario(driver: WebDriver, logger: ILogger) -> Sequence[ChainRunner[Any]]:
    ...     page = SomePage(driver=driver)
    ...
    ...     return [
    ...         drive_page(
    ...             act(page, open_page)
    ...                 .failure(log_error("Failed to open..."))
    ...                 .success(log_success("Opened!")),
    ...         ),
    ...         match_page(
    ...             when(
    ...                 lambda: page.has_cookie_banner(),
    ...                 then=[
    ...                     drive_page(
    ...                         act(page, dismiss_banner)
    ...                             .failure(log_error("Failed to dismiss..."))
    ...                             .success(log_success("Banner dismissed!")),
    ...                     ),
    ...                 ],
    ...             ),
    ...             when(
    ...                 lambda: not page.has_cookie_banner(),
    ...                 then=[
    ...                     drive_page(
    ...                         act(page, verify_page)
    ...                             .failure(log_error("Failed to verify..."))
    ...                             .success(log_success("Page verified!")),
    ...                     ),
    ...                 ],
    ...             ),
    ...         ),
    ...         drive_page(
    ...             act(page, do_next_thing)
    ...                 .failure(log_error("Failed..."))
    ...                 .success(log_success("Done!")),
    ...         ),
    ...     ]

"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, final

from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
from ocarina.dsl.testing_with_railway.internals.action_chain import ActionChain
from ocarina.railway.result import Fail, Ok

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.custom_types.thunk import Thunk


class NoMatchingBranchError(Exception):
    """Raised when no when() condition matched in a match_page() call."""


@dataclass
@final
class _When:
    """A conditional branch: a guard and the ChainRunners to execute if it matches.

    Not meant to be instantiated directly — use the when() constructor.

    Attributes:
        condition: A thunk returning True if this branch should execute.
        runners: ChainRunners to execute sequentially if condition is True.

    """

    condition: Thunk[bool]
    runners: Sequence[ChainRunner[Any]]


def when(
    condition: Thunk[bool],
    *,
    then: Sequence[ChainRunner[Any]],
) -> _When:
    """Declare a conditional branch for match_page().

    Args:
        condition: A thunk (() -> bool) evaluated to decide if this branch runs.
                   Should not raise — exceptions are treated as False.
        then: ChainRunners to execute sequentially if condition returns True.
              Accepts drive_page() calls or any other ChainRunner.

    Returns:
        A When branch descriptor consumed by match_page().

    Example:
        >>> when(
        ...     lambda: page.has_cookie_banner(),
        ...     then=[
        ...         drive_page(
        ...             act(page, dismiss_banner)
        ...                 .failure(log_error("Failed..."))
        ...                 .success(log_success("Dismissed!")),
        ...         ),
        ...     ],
        ... )

    """
    return _When(condition=condition, runners=then)


def _run_branch(runners: Sequence[ChainRunner[Any]]) -> ActionChain[Any]:
    """Execute a branch's ChainRunners sequentially, short-circuiting on failure.

    Args:
        runners: ChainRunners to execute in order.

    Returns:
        The final ActionChain — either the first failed one, or the last ok one.

    """
    last: ActionChain[Any] | None = None

    for runner in runners:
        chain = runner.run()
        last = chain
        if chain.has_failed():
            return chain

    if last is None:
        return ActionChain(has_failed=False, result=Ok(value=None))

    return last


def match_page(*branches: _When) -> ChainRunner[Any]:
    """Conditional branching operator for adaptive pages.

    Evaluates each when() condition in declaration order.
    The first branch whose condition returns True is executed.
    If no branch matches, the ChainRunner fails with NoMatchingBranchError.

    Args:
        *branches: When instances declared with when(). Evaluated in order.

    Returns:
        ChainRunner[Any] — composes naturally in a scenario's ChainRunner list.

    Raises (via Fail on the railway):
        NoMatchingBranchError: If no when() condition returned True.

    Example:
        >>> match_page(
        ...     when(lambda: page.is_in_state_a(), then=[drive_page(...)]),
        ...     when(lambda: page.is_in_state_b(), then=[drive_page(...)]),
        ... )

    """

    def thunk() -> ActionChain[Any]:
        for branch in branches:
            try:
                matched = branch.condition()
            except Exception:  # noqa: BLE001
                matched = False

            if matched:
                return _run_branch(branch.runners)

        return ActionChain(
            has_failed=True,
            result=Fail(
                error=NoMatchingBranchError(
                    f"No when() branch matched out of {len(branches)} candidate(s)."
                )
            ),
        )

    return ChainRunner(thunk=thunk)
