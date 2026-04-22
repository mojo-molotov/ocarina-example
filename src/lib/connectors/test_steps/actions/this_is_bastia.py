"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.madness.this_is_bastia import ThisIsBastiaPage


def verify_this_is_bastia_page(
    p: ThisIsBastiaPage,
) -> ThisIsBastiaPage:
    """Verify we are on the Igoristan's madness THIS IS BASTIA page."""
    return p.verify()


def click_invader_detector_btn(
    p: ThisIsBastiaPage,
) -> ThisIsBastiaPage:
    """Click on invader detector btn."""
    return p.click_invader_detector_btn()
