"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.donkey_sausage_detector.bsod import BSODPage


def verify_bsod_page(
    p: BSODPage,
) -> BSODPage:
    """Verify we are on the Igoristan's DSED BSOD page."""
    return p.verify()
