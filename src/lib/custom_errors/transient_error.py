"""Transient error."""

from typing import final


@final
class TransientError(Exception):
    """General purpose transient error."""
