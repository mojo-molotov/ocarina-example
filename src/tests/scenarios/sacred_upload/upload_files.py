"""Test that random loaders page can be rendered."""

from random import randint
from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.sacred_upload import (
    add_images,
    click_on_amen_btn,
    click_on_delete_img_btn,
    click_on_sin_btn,
    click_on_upload_btn,
    open_sacred_upload_page,
    verify_dropzone_is_empty,
    verify_sacred_upload_page,
)
from lib.ext.ocarina.adapters.selenium.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_and_take_screenshot,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.sacred_upload.sacred_upload import SacredUploadPage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def upload_some_files(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[SacredUploadPage]]:
    """Verify that uploading files works properly."""
    on_sacred_upload_page = SacredUploadPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_and_take_screenshot = create_log_success_and_take_screenshot(
        logger=logger, driver=driver
    )
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    images_amount = randint(1, 10)  # noqa: S311

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
            act(on_sacred_upload_page, add_images(images_amount=images_amount))
            .failure(
                just_log_error("Failed to add images to the sacred upload form...")
            )
            .success(
                log_success_and_take_screenshot(
                    "Added images to the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, click_on_upload_btn)
            .failure(just_log_error("Failed to click on upload button..."))
            .success(log_success_and_take_screenshot("Clicked on the upload button!")),
            act(on_sacred_upload_page, click_on_amen_btn)
            .failure(just_log_error("Failed to click on the upload confirm button..."))
            .success(
                log_success_and_take_screenshot("Clicked on the upload confirm button!")
            ),
            act(on_sacred_upload_page, verify_dropzone_is_empty)
            .failure(just_log_error("The dropzone is not empty..."))
            .success(log_success_and_take_screenshot("The dropzone is empty!")),
        ),
    ]


def upload_some_files_passing_by_delete_img_button(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[SacredUploadPage]]:
    """Verify that uploading files works properly."""
    on_sacred_upload_page = SacredUploadPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_and_take_screenshot = create_log_success_and_take_screenshot(
        logger=logger, driver=driver
    )
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
            act(on_sacred_upload_page, add_images(images_amount=1))
            .failure(just_log_error("Failed to add image to the sacred upload form..."))
            .success(
                log_success_and_take_screenshot(
                    "Added image to the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                click_on_delete_img_btn(idx=1),
            )
            .failure(
                just_log_error(
                    "Failed to delete the 1st image of the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Deleted the 1st image of the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, verify_dropzone_is_empty)
            .failure(just_log_error("The dropzone is not empty..."))
            .success(log_success_and_take_screenshot("The dropzone is empty!")),
            act(
                on_sacred_upload_page,
                add_images(images_amount=2),
            )
            .failure(
                just_log_error("Failed to add 2 images to the sacred upload form...")
            )
            .success(
                log_success_and_take_screenshot(
                    "Added 2 images to the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                click_on_delete_img_btn(idx=2),
            )
            .failure(
                just_log_error(
                    "Failed to delete the 2nd image of the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Deleted the 2nd image of the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                click_on_delete_img_btn(idx=1),
            )
            .failure(
                just_log_error(
                    "Failed to delete the 1st image of the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Deleted the 1st image of the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, verify_dropzone_is_empty)
            .failure(just_log_error("The dropzone is not empty..."))
            .success(log_success_and_take_screenshot("The dropzone is empty!")),
            act(
                on_sacred_upload_page,
                add_images(images_amount=3),
            )
            .failure(
                just_log_error("Failed to add 3 images to the sacred upload form...")
            )
            .success(
                log_success_and_take_screenshot(
                    "Added 3 images to the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                click_on_delete_img_btn(idx=3),
            )
            .failure(
                just_log_error(
                    "Failed to delete the 3rd image of the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Deleted the 3rd image of the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                click_on_delete_img_btn(idx=2),
            )
            .failure(
                just_log_error(
                    "Failed to delete the 2nd image of the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Deleted the 2nd image of the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                click_on_delete_img_btn(idx=1),
            )
            .failure(
                just_log_error(
                    "Failed to delete the 1st image of the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Deleted the 1st image of the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, verify_dropzone_is_empty)
            .failure(just_log_error("The dropzone is not empty..."))
            .success(log_success_and_take_screenshot("The dropzone is empty!")),
            act(
                on_sacred_upload_page,
                add_images(images_amount=4),
            )
            .failure(
                just_log_error("Failed to add 4 images to the sacred upload form...")
            )
            .success(
                log_success_and_take_screenshot(
                    "Added 4 images to the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, click_on_upload_btn)
            .failure(just_log_error("Failed to click on upload button..."))
            .success(log_success_and_take_screenshot("Clicked on the upload button!")),
            act(on_sacred_upload_page, click_on_amen_btn)
            .failure(just_log_error("Failed to click on the upload confirm button..."))
            .success(
                log_success_and_take_screenshot("Clicked on the upload confirm button!")
            ),
            act(on_sacred_upload_page, verify_dropzone_is_empty)
            .failure(just_log_error("The dropzone is not empty..."))
            .success(log_success_and_take_screenshot("The dropzone is empty!")),
        ),
    ]


def upload_some_files_passing_by_sin_button(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[SacredUploadPage]]:
    """Verify that uploading files works properly."""
    on_sacred_upload_page = SacredUploadPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_and_take_screenshot = create_log_success_and_take_screenshot(
        logger=logger, driver=driver
    )
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
            act(on_sacred_upload_page, add_images(images_amount=1))
            .failure(just_log_error("Failed to add image to the sacred upload form..."))
            .success(
                log_success_and_take_screenshot(
                    "Added image to the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, click_on_upload_btn)
            .failure(just_log_error("Failed to click on upload button..."))
            .success(log_success_and_take_screenshot("Clicked on the upload button!")),
            act(on_sacred_upload_page, click_on_sin_btn)
            .failure(just_log_error("Failed to click on the upload cancel button..."))
            .success(
                log_success_and_take_screenshot("Clicked on the upload cancel button!")
            ),
            act(
                on_sacred_upload_page,
                add_images(images_amount=1, forced_expected_img_amount=2),
            )
            .failure(just_log_error("Failed to add image to the sacred upload form..."))
            .success(
                log_success_and_take_screenshot(
                    "Added image to the sacred upload form!"
                )
            ),
            act(on_sacred_upload_page, click_on_upload_btn)
            .failure(just_log_error("Failed to click on upload button..."))
            .success(log_success_and_take_screenshot("Clicked on the upload button!")),
            act(on_sacred_upload_page, click_on_amen_btn)
            .failure(just_log_error("Failed to click on the upload confirm button..."))
            .success(
                log_success_and_take_screenshot("Clicked on the upload confirm button!")
            ),
            act(on_sacred_upload_page, verify_dropzone_is_empty)
            .failure(just_log_error("The dropzone is not empty..."))
            .success(log_success_and_take_screenshot("The dropzone is empty!")),
        ),
    ]


def try_to_upload_too_much_files_immediately(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[SacredUploadPage]]:
    """Verify putting a lot of images in one-shot = 0 image registered."""
    on_sacred_upload_page = SacredUploadPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_and_take_screenshot = create_log_success_and_take_screenshot(
        logger=logger, driver=driver
    )
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
            act(on_sacred_upload_page, add_images(images_amount=900, failing=True))
            .failure(
                just_log_error(
                    "Failed to add (too much) images to the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Added (too much) images to the sacred upload form!"
                )
            ),
        ),
    ]


def try_to_upload_too_much_files_after_first_insertion(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[SacredUploadPage]]:
    """Verify putting a lot of images in two-shots = n first-shot images registered."""
    on_sacred_upload_page = SacredUploadPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_and_take_screenshot = create_log_success_and_take_screenshot(
        logger=logger, driver=driver
    )
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
            act(on_sacred_upload_page, add_images(images_amount=1))
            .failure(
                just_log_error("Failed to add images to the sacred upload form...")
            )
            .success(
                log_success_and_take_screenshot(
                    "Added images to the sacred upload form!"
                )
            ),
            act(
                on_sacred_upload_page,
                add_images(
                    images_amount=900, failing=True, forced_expected_img_amount=1
                ),
            )
            .failure(
                just_log_error(
                    "Failed to add (too much) images to the sacred upload form..."
                )
            )
            .success(
                log_success_and_take_screenshot(
                    "Added (too much) images to the sacred upload form!"
                )
            ),
        ),
    ]


test_sacred_upload_form_with_some_files = create_selenium_test(
    name="Upload some files",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=upload_some_files(driver, logger)
    ),
)

test_sacred_upload_form_with_some_files_passing_by_sin_btn = create_selenium_test(
    name="Upload some files, also playing with the upload cancel button",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=upload_some_files_passing_by_sin_button(driver, logger)
    ),
)

test_sacred_upload_form_with_some_files_passing_by_del_btn = create_selenium_test(
    name="Upload some files, also playing with the delete image buttons",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=upload_some_files_passing_by_delete_img_button(driver, logger)
    ),
)

test_sacred_upload_try_with_too_much_files_immediately = create_selenium_test(
    name="Try to put too much files in the dropzone",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=try_to_upload_too_much_files_immediately(driver, logger)
    ),
)

test_sacred_upload_try_with_too_much_files_after_first_insertion = create_selenium_test(
    name="Put 1 file in the dropzone, then try to drop too much files",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=try_to_upload_too_much_files_after_first_insertion(driver, logger)
    ),
)
