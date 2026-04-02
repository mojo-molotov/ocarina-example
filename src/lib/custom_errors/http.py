"""HTTP errors."""

from typing import final


@final
class HttpErrorPageReachedError(Exception):
    """Raised when error page is reached."""
