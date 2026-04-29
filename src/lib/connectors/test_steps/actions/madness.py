"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.madness.base import MadnessPage


def open_madness_page(
    p: MadnessPage,
) -> MadnessPage:
    """Open the madness page."""
    return p.open()
