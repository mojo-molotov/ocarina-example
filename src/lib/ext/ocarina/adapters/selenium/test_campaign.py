"""Test campaign adapter."""

from typing import TYPE_CHECKING, final

from ocarina.dsl.testing.oc_test_campaign import TestCampaign as OriginalTestCampaign
from selenium.webdriver.remote.webdriver import WebDriver

from lib.ext.ocarina.adapters.agnostic.cli_getters import get_max_workers

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing.oc_test_suite import TestSuite


@final
class TestCampaign(OriginalTestCampaign[WebDriver]):
    """TestCampaign adapter."""

    def __init__(
        self,
        *,
        name: str,
        suites: Sequence[TestSuite[WebDriver]],
        max_workers: int | None = None,
        saturate_workers: bool | None = None,
    ) -> None:
        """Initialize the campaign."""
        if max_workers is None:
            max_workers = get_max_workers()

        super().__init__(
            name=name,
            suites=suites,
            max_workers=max_workers,
            saturate_workers=saturate_workers,
        )
