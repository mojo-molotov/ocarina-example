"""Test that random loaders page can be rendered."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.sacred_upload import (
    click_back_to_igoristan_link,
    open_sacred_upload_page,
    verify_sacred_upload_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.sacred_upload.sacred_upload import SacredUploadPage
from tests.scenarios.homepage.verify_homepage import verify_homepage

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def just_go_back_to_igoristan(driver: WebDriver, logger: ILogger):
    """Verify that random loaders page reaches its first render."""
    on_sacred_upload_page = SacredUploadPage(driver=driver)

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
            act(on_sacred_upload_page, open_sacred_upload_page)
            .failure(just_log_error("Failed to open the sacred upload page..."))
            .success(just_log_success("Opened the sacred upload page!")),
            act(on_sacred_upload_page, verify_sacred_upload_page)
            .failure(
                log_error_with_current_url(
                    "Failed to verify the sacred upload page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the sacred upload page!"
                )
            ),
            act(on_sacred_upload_page, click_back_to_igoristan_link)
            .failure(
                just_log_error(
                    "Failed to click on the 'Back to Igoristan' link...",
                )
            )
            .success(just_log_success("Clicked the 'Back to Igoristan' link!")),
        ),
    ]


test_sacred_upload_just_go_back_to_igoristan = create_selenium_test(
    name="Use the go back to Igoristan button",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=just_go_back_to_igoristan(driver, logger)
    ),
    post_test_scenarios_fragments=[verify_homepage],
)
