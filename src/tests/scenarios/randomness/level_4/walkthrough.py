"""Walkthrough, traversing random pages."""

from typing import TYPE_CHECKING, Any

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.dsl.testing_with_railway.match_page import when
from ocarina.opinionated.dsl.drive_page import drive_page
from ocarina.opinionated.loggers.create_matching_logger import create_matching_logger

from lib.connectors.test_steps.actions.bsod import verify_bsod_page
from lib.connectors.test_steps.actions.cors_errors import (
    click_use_api_anyway_btn,
    verify_cors_page,
)
from lib.connectors.test_steps.actions.corsicamon_enter_api_key import (
    click_back_to_igoristan_link as click_back_to_igoristan_link_on_corsicamon_enter_api_key_page,  # noqa: E501
)
from lib.connectors.test_steps.actions.corsicamon_enter_api_key import (
    verify_corsicamon_enter_api_key_page,
)
from lib.connectors.test_steps.actions.homepage import verify_homepage
from lib.connectors.test_steps.actions.ids_bypassed import (
    click_back_to_igoristan_link as click_back_to_igoristan_link_on_ids_bypassed_page,
)
from lib.connectors.test_steps.actions.ids_bypassed import verify_ids_bypassed_page
from lib.connectors.test_steps.actions.madness import (
    open_madness_page,
)
from lib.connectors.test_steps.actions.this_is_bastia import (
    click_invader_detector_btn,
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
from pages.corsicamon.enter_api_key import CorsicamonEnterApiKeyPage
from pages.donkey_sausage_detector.bsod import BSODPage
from pages.donkey_sausage_detector.ids_bypassed import IDSBypassedPage
from pages.donkey_sausage_detector.matchers import DSEDPageMatchers
from pages.homepage import Homepage
from pages.madness.base import MadnessPage
from pages.madness.cors import CorsPage
from pages.madness.matchers import MadnessPageMatchers
from pages.madness.this_is_bastia import ThisIsBastiaPage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def traverse_random_pages(driver: WebDriver, logger: ILogger):
    """Woo-oo!"""  # noqa: D400
    on_madness_page = MadnessPage(driver=driver)

    on_cors_page = CorsPage(driver=driver)
    on_corsicamon_enter_api_key_page = CorsicamonEnterApiKeyPage(driver=driver)

    on_this_is_bastia_page = ThisIsBastiaPage(driver=driver)
    on_bsod_page = BSODPage(driver=driver)
    on_ids_bypassed_page = IDSBypassedPage(driver=driver)
    on_homepage = Homepage(driver=driver)

    check_that_madness = MadnessPageMatchers(driver=driver)
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

    open_madness_random_page = drive_page(
        act(on_madness_page, open_madness_page)
        .failure(just_log_error("Failed to open the madness page..."))
        .success(just_log_success("Opened the madness page!")),
    )

    go_from_cors_page_to_homepage: Sequence[ChainRunner[Any]] = [
        drive_page(
            act(on_cors_page, verify_cors_page)
            .failure(log_error_with_current_url("Failed to verify the CORS page..."))
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the CORS page!"
                )
            ),
            act(on_cors_page, click_use_api_anyway_btn)
            .failure(
                just_log_error("Failed to click on the 'Use API anyway' button...")
            )
            .success(just_log_success("Clicked on the 'Use API anyway' button!")),
        ),
        drive_page(
            act(
                on_corsicamon_enter_api_key_page,
                verify_corsicamon_enter_api_key_page,
            )
            .failure(
                log_error_with_current_url(
                    "Failed to verify the Corsicamon enter API key page..."
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the Corsicamon enter API key page!"
                )
            ),
            act(
                on_corsicamon_enter_api_key_page,
                click_back_to_igoristan_link_on_corsicamon_enter_api_key_page,
            )
            .failure(
                log_error_with_current_url(
                    "Failed to click on the 'go back to Igoristan' link..."
                )
            )
            .success(just_log_success("Clicked on the 'go back to Igoristan' link...")),
        ),
        drive_page(
            act(
                on_homepage,
                verify_homepage,
            )
            .failure(log_error_with_current_url("Failed to verify the homepage..."))
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the homepage!"
                )
            )
        ),
    ]

    go_from_ids_bypassed_page_to_homepage: Sequence[ChainRunner[Any]] = [
        drive_page(
            act(
                on_ids_bypassed_page,
                verify_ids_bypassed_page,
            )
            .failure(
                log_error_with_current_url("Failed to verify the IDS bypassed page...")
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the IDS bypassed page!"
                )
            ),
            act(
                on_ids_bypassed_page,
                click_back_to_igoristan_link_on_ids_bypassed_page,
            )
            .failure(
                log_error_with_current_url(
                    "Failed to click on the 'go back to Igoristan' link..."
                )
            )
            .success(just_log_success("Clicked on the 'go back to Igoristan' link!")),
        ),
        drive_page(
            act(
                on_homepage,
                verify_homepage,
            )
            .failure(log_error_with_current_url("Failed to verify the homepage..."))
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the homepage!"
                )
            )
        ),
    ]

    go_from_this_is_bastia_page_to_random_dsed_page = drive_page(
        act(on_this_is_bastia_page, verify_this_is_bastia_page)
        .failure(
            log_error_with_current_url("Failed to verify the This is Bastia page...")
        )
        .success(
            log_success_with_current_url_and_take_screenshot(
                "Verified the This is Bastia page!"
            )
        ),
        act(on_this_is_bastia_page, click_invader_detector_btn)
        .failure(just_log_error("Failed to click on the 'Invader Detector' button..."))
        .success(just_log_success("Clicked on the 'Invader Detector' button!")),
    )

    bsod_dead_end = drive_page(
        act(on_bsod_page, verify_bsod_page)
        .failure(log_error_with_current_url("Failed to verify the BSOD page..."))
        .success(
            log_success_with_current_url_and_take_screenshot("Verified the BSOD page!")
        )
    )

    return [
        open_madness_random_page,
        match_page(
            branches=[
                when(
                    check_that_madness.is_cors_page,
                    name="is_cors_page",
                    then=go_from_cors_page_to_homepage,
                ),
                when(
                    check_that_madness.is_bastia_page,
                    name="is_bastia_page",
                    then=[
                        go_from_this_is_bastia_page_to_random_dsed_page,
                        match_page(
                            branches=[
                                when(
                                    check_that_dsed_result.is_bsod_page,
                                    name="is_bsod_page",
                                    then=[bsod_dead_end],
                                ),
                                when(
                                    check_that_dsed_result.is_ids_bypassed_page,
                                    name="is_ids_bypassed_page",
                                    then=go_from_ids_bypassed_page_to_homepage,
                                ),
                            ],
                            logger=create_matching_logger("terminal"),
                        ),
                    ],
                ),
            ],
            logger=create_matching_logger("terminal"),
        ),
    ]


test_traverse_random_pages = create_selenium_test(
    name="Traverse random pages",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=traverse_random_pages(driver, logger),
    ),
)
