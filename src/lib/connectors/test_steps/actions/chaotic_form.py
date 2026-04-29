"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from ocarina.ports.ilogger import ILogger

    from pages.chaotic_form import ChaoticFormPage


def open_chaotic_form_page(p: ChaoticFormPage) -> ChaoticFormPage:
    """Open the Igoristan's chaotic form page."""
    return p.open()


def verify_chaotic_form_page(p: ChaoticFormPage) -> ChaoticFormPage:
    """Verify we are on the Igoristan's chaotic form page."""
    return p.verify()


def fill_chaotic_form_and_send_it_with_retries(  # noqa: PLR0913
    *,
    retries: int,
    logger: ILogger,
    bible_verse: str,
    corsican_city: str,
    inspiring_apostle_index: int,
    cinto_height: float,
    personal_revelation: str,
) -> Callable[[ChaoticFormPage], ChaoticFormPage]:
    """Fill every field and submit the form (n retries)."""

    def unwrapped(p: ChaoticFormPage) -> ChaoticFormPage:
        return p.fill_form_and_send_it_with_retries(
            retries=retries,
            logger=logger,
            bible_verse=bible_verse,
            corsican_city=corsican_city,
            inspiring_apostle_index=inspiring_apostle_index,
            cinto_height=cinto_height,
            personal_revelation=personal_revelation,
        )

    return unwrapped
