"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from ocarina.ports.ilogger import ILogger

    from pages.corsicamon.main import CorsicamonPage


def open_corsicamon_main_page(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Open the Igoristan's Corsicamon main page."""
    return p.open()


def verify_corsicamon_main_page(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Verify we are on the Igoristan's Corsicamon main page."""
    return p.verify()


def click_back_to_igoristan_link(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Click on the 'back to Igoristan' link."""
    return p.click_back_to_igoristan_link()


def enter_fresh_corsicamon_id(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Enter fresh Corsicamon ID."""
    return p.enter_fresh_corsicamon_id()


def enter_fresh_corsicamon_id_with_retries(
    *,
    retries: int,
    logger: ILogger,
) -> Callable[[CorsicamonPage], CorsicamonPage]:
    """Enter fresh Corsicamon ID (n retries)."""

    def unwrapped(p: CorsicamonPage) -> CorsicamonPage:
        return p.enter_fresh_corsicamon_id_with_retries(retries=retries, logger=logger)

    return unwrapped


def enter_invalid_corsicamon_id(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Enter invalid Corsicamon ID."""
    return p.enter_invalid_corsicamon_id()


def enter_already_in_draw_corsicamon_id(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Enter already in draw id, then check the presence of an error message."""
    return p.enter_already_in_draw_corsicamon_id()


def make_a_new_draw(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Make a new draw."""
    return p.make_a_new_draw()


def make_a_new_draw_with_retries(
    *,
    retries: int,
    logger: ILogger,
) -> Callable[[CorsicamonPage], CorsicamonPage]:
    """Make a new draw (n retries)."""

    def unwrapped(p: CorsicamonPage) -> CorsicamonPage:
        return p.make_a_new_draw_with_retries(retries=retries, logger=logger)

    return unwrapped


def verify_enter_id_field_is_empty(
    p: CorsicamonPage,
) -> CorsicamonPage:
    """Verify the 'Enter ID' field is empty."""
    return p.verify_enter_id_field_empty()
