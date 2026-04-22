"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.donkey_sausage_detector.base import DonkeySausageEaterDetectorPage


def open_dsed_page(
    p: DonkeySausageEaterDetectorPage,
) -> DonkeySausageEaterDetectorPage:
    """Open the DSED page."""
    return p.open()
