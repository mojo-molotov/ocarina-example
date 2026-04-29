"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.homepage import Homepage


def open_homepage(p: Homepage) -> Homepage:
    """Open the Igoristan's homepage."""
    return p.open()


def verify_homepage(p: Homepage) -> Homepage:
    """Verify we are on the Igoristan's homepage."""
    return p.verify()
