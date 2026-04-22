"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.donkey_sausage_detector.base import DonkeySausageEaterDetectorPage
    from pages.donkey_sausage_detector.bsod import BSODPage
    from pages.donkey_sausage_detector.ids_bypassed import IDSBypassedPage


def open_dsed_page(
    p: DonkeySausageEaterDetectorPage,
) -> DonkeySausageEaterDetectorPage:
    """Open the DSED page."""
    return p.open()


def verify_ids_bypassed_page(
    p: IDSBypassedPage,
) -> IDSBypassedPage:
    """Verify we are on the Igoristan's IDS bypassed page."""
    return p.verify()


def verify_bsod_page(
    p: BSODPage,
) -> BSODPage:
    """Verify we are on the Igoristan's DSED BSOD page."""
    return p.verify()
