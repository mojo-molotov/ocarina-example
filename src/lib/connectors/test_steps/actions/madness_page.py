"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.madness.base import MadnessPage
    from pages.madness.cors import CorsPage
    from pages.madness.this_is_bastia import ThisIsBastiaPage


def open_madness_page(
    p: MadnessPage,
) -> MadnessPage:
    """Open the madness page."""
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
