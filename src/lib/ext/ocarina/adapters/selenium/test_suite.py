"""Test suite adapter."""

from typing import TYPE_CHECKING, final

from ocarina.dsl.testing.oc_test_suite import TestSuite as OriginalTestSuite
from ocarina.opinionated.infra.act_counter import ActCounter
from ocarina.opinionated.loggers.create_matching_logger import create_matching_logger
from selenium.webdriver.remote.webdriver import WebDriver

from constants.sys.transient_errors import transient_errors
from lib.ext.ocarina.adapters.selenium.cli_getters import get_logger_mode
from lib.ext.ocarina.adapters.selenium.screenshotter import take_screenshot_unstrict

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool
    from ocarina.custom_types.thunk import Thunk
    from ocarina.dsl.testing.oc_test import Test
    from ocarina.ports.ilogger import ILogger


@final
class TestSuite(OriginalTestSuite[WebDriver]):
    """TestSuite adapter."""

    def __init__(  # noqa: PLR0913
        self,
        *,
        name: str,
        tests: Sequence[Test[WebDriver]],
        drivers_pool: SeleniumWebDriversPool,
        create_logger: Thunk[ILogger] | None = None,
        copy_indicator: str = "+",
        put_space_after_copy_indicator: bool = False,
        autoscreen_on_fail: bool = True,
        saturate_workers: bool | None = None,
    ) -> None:
        """Initialize the TestSuite."""
        if create_logger is None:

            def _create_logger():  # noqa: ANN202
                return create_matching_logger(get_logger_mode())

            create_logger = _create_logger

        super().__init__(
            name=name,
            tests=tests,
            max_retries_per_test=8,
            create_logger=create_logger,
            drivers_pool=drivers_pool,
            copy_indicator=copy_indicator,
            put_space_after_copy_indicator=put_space_after_copy_indicator,
            autoscreen_on_fail=autoscreen_on_fail,
            act_counter=ActCounter(),
            take_screenshot=take_screenshot_unstrict,
            transient_errors=transient_errors,
            saturate_workers=saturate_workers,
        )
