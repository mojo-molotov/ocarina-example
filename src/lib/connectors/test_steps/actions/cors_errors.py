"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.madness.cors import CorsPage


def verify_cors_page(
    p: CorsPage,
) -> CorsPage:
    """Verify we are on the Igoristan's madness CORS page."""
    return p.verify()


def click_use_api_anyway_btn(
    p: CorsPage,
) -> CorsPage:
    """Click on use API anyway btn."""
    return p.click_use_api_anyway_btn()
