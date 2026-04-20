"""Test that random error page can be loaded (flaky)."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.dsl.testing_with_railway.match_page import when
from ocarina.opinionated.dsl.drive_page import drive_page
from ocarina.opinionated.loggers.create_matching_logger import create_matching_logger

from lib.connectors.test_steps.actions.madness_page import (
    open_madness_page,
    verify_cors_page,
    verify_this_is_bastia_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.agnostic.match_page import match_page
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.madness.base import MadnessPage
from pages.madness.cors import CorsPage
from pages.madness.matchers import MadnessPageMatchers
from pages.madness.this_is_bastia import ThisIsBastiaPage

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def madness_page_render(driver: WebDriver, logger: ILogger):
    """Verify that random madness page reaches its first render."""
    on_madness_page = MadnessPage(driver=driver)
    on_cors_page = CorsPage(driver=driver)
    on_this_is_bastia_page = ThisIsBastiaPage(driver=driver)
    check_that_madness = MadnessPageMatchers(driver=driver)

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

    return [
        drive_page(
            act(on_madness_page, open_madness_page)
            .failure(just_log_error("Failed to open the madness page..."))
            .success(just_log_success("Opened the madness page!")),
        ),
        match_page(
            branches=[
                when(
                    check_that_madness.is_cors_page,
                    name="is_cors_page",
                    then=[
                        drive_page(
                            act(on_cors_page, verify_cors_page)
                            .failure(log_error_with_current_url("Test KO - CORS"))
                            .success(
                                log_success_with_current_url_and_take_screenshot(
                                    "Test OK - CORS"
                                )
                            )
                        )
                    ],
                ),
                when(
                    check_that_madness.is_bastia_page,
                    name="is_bastia_page",
                    then=[
                        drive_page(
                            act(on_this_is_bastia_page, verify_this_is_bastia_page)
                            .failure(
                                log_error_with_current_url("Test KO - THIS IS BASTIA")
                            )
                            .success(
                                log_success_with_current_url_and_take_screenshot(
                                    "Test OK - THIS IS BASTIA"
                                )
                            )
                        )
                    ],
                ),
            ],
            logger=create_matching_logger("terminal"),
        ),
    ]


test_madness_page_render = create_selenium_test(
    name="Madness page render",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=madness_page_render(driver, logger),
    ),
)
