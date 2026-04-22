"""Test that random dsed page can be loaded (NOT flaky)."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.dsl.testing_with_railway.match_page import when
from ocarina.opinionated.dsl.drive_page import drive_page
from ocarina.opinionated.loggers.create_matching_logger import create_matching_logger

from lib.connectors.test_steps.actions.bsod import verify_bsod_page
from lib.connectors.test_steps.actions.dsed import (
    open_dsed_page,
)
from lib.connectors.test_steps.actions.ids_bypassed import verify_ids_bypassed_page
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.agnostic.match_page import match_page
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.donkey_sausage_detector.base import DonkeySausageEaterDetectorPage
from pages.donkey_sausage_detector.bsod import BSODPage
from pages.donkey_sausage_detector.ids_bypassed import IDSBypassedPage
from pages.donkey_sausage_detector.matchers import DSEDPageMatchers

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def dsed_page_render(driver: WebDriver, logger: ILogger):
    """Verify that random DSED page reaches its first render."""
    on_dsed_page = DonkeySausageEaterDetectorPage(driver=driver)
    on_ids_bypassed_page = IDSBypassedPage(driver=driver)
    on_bsod_page = BSODPage(driver=driver)
    check_that_dsed_result = DSEDPageMatchers(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    open_random_page = drive_page(
        act(on_dsed_page, open_dsed_page)
        .failure(just_log_error("Failed to open the DSED page..."))
        .success(just_log_success("Opened the DSED page!")),
    )

    control_bsod_page = drive_page(
        act(on_bsod_page, verify_bsod_page)
        .failure(log_error_with_current_url("Test KO - BSOD"))
        .success(log_success_with_current_url_and_take_screenshot("Test OK - BSOD"))
    )

    control_ids_bypassed_page = drive_page(
        act(on_ids_bypassed_page, verify_ids_bypassed_page)
        .failure(
            log_error_with_current_url(
                "Test KO - IDS (not) Bypassed // UNKNOWN OUTCOME"
            )
        )
        .success(
            log_success_with_current_url_and_take_screenshot("Test OK - IDS Bypassed")
        )
    )

    return [
        open_random_page,
        match_page(
            branches=[
                when(
                    check_that_dsed_result.is_bsod_page,
                    name="is_bsod_page",
                    then=[control_bsod_page],
                ),
                when(
                    check_that_dsed_result.is_ids_bypassed_page,
                    name="is_ids_bypassed_page",
                    then=[control_ids_bypassed_page],
                ),
            ],
            logger=create_matching_logger("terminal"),
        ),
    ]


test_dsed_page_render = create_selenium_test(
    name="DSED page render",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dsed_page_render(driver, logger),
    ),
)
