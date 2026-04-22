"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.donkey_sausage_detector.ids_bypassed import IDSBypassedPage


def verify_ids_bypassed_page(
    p: IDSBypassedPage,
) -> IDSBypassedPage:
    """Verify we are on the Igoristan's IDS bypassed page."""
    return p.verify()


def click_back_to_igoristan_link(
    p: IDSBypassedPage,
) -> IDSBypassedPage:
    """Click on the back to Igoristan link."""
    return p.click_back_to_igoristan_link()
