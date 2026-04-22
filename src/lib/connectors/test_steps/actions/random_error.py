"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.random_error import RandomErrorPage


def open_random_error_page(p: RandomErrorPage) -> RandomErrorPage:
    """Open the Igoristan's random error page."""
    return p.open()


def verify_random_error_page(p: RandomErrorPage) -> RandomErrorPage:
    """Verify we are on the Igoristan's random error page."""
    return p.verify()
