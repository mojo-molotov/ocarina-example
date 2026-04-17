"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.madness.cors import CorsPage
    from pages.madness.this_is_bastia import ThisIsBastiaPage


def open_cors_page_url(
    p: CorsPage,
) -> CorsPage:
    """Open the madness page URL (typed to be called from CorsPage)."""
    return p.open()


def open_this_is_bastia_page_url(
    p: ThisIsBastiaPage,
) -> ThisIsBastiaPage:
    """Open the madness page URL (typed to be called from ThisIsBastiaPage)."""
    return p.open()


def verify_cors_page(
    p: CorsPage,
) -> CorsPage:
    """Verify we are on the Igoristan's madness CORS page."""
    return p.verify()


def verify_this_is_bastia_page(
    p: ThisIsBastiaPage,
) -> ThisIsBastiaPage:
    """Verify we are on the Igoristan's madness THIS IS BASTIA page."""
    return p.verify()
