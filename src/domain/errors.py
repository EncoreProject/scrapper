"""Errors Module"""

from enum import Enum


class CardError(Enum):
    """Descriptions about possible errors in a CardEntity."""
    CARD_NUMBER_NONE = "Card number is None"
    CARD_NUMBER_VALUE_NONE = "Card number value is None {}"
