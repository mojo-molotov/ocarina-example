"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.random_loaders import RandomLoadersPage


def open_random_loaders_page(p: RandomLoadersPage) -> RandomLoadersPage:
    """Open the Igoristan's Random Loaders page."""
    return p.open()


def verify_random_loaders_page(p: RandomLoadersPage) -> RandomLoadersPage:
    """Verify we are on the Igoristan's Random Loaders page."""
    return p.verify()


def verify_full_load(p: RandomLoadersPage) -> RandomLoadersPage:
    """Verify full load."""
    return p.verify_full_load()


def click_back_to_igoristan_link(p: RandomLoadersPage) -> RandomLoadersPage:
    """Click back to Igoristan's Random Loaders page."""
    return p.click_back_to_igoristan_link()
