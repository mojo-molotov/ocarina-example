"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from pages.sacred_upload.sacred_upload import SacredUploadPage


def open_sacred_upload_page(p: SacredUploadPage) -> SacredUploadPage:
    """Open the Igoristan's sacred upload page."""
    return p.open()


def verify_sacred_upload_page(p: SacredUploadPage) -> SacredUploadPage:
    """Verify we are on the Igoristan's sacred upload page."""
    return p.verify()


def add_images(
    *,
    images_amount: int,
) -> Callable[[SacredUploadPage], SacredUploadPage]:
    """Append images to the sacred upload page's form."""

    def unwrapped(p: SacredUploadPage) -> SacredUploadPage:
        return p.add_images(images_amount=images_amount)

    return unwrapped


def click_on_upload_btn(p: SacredUploadPage) -> SacredUploadPage:
    """Click on upload button."""
    return p.click_on_upload_btn()


def click_on_amen_btn(p: SacredUploadPage) -> SacredUploadPage:
    """Click on amen button."""
    return p.click_on_amen_btn()


def verify_dropzone_is_empty(p: SacredUploadPage) -> SacredUploadPage:
    """Verify dropzone is empty."""
    return p.verify_dropzone_is_empty()
