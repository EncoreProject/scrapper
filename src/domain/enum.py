"""Enum"""
from enum import Enum


class CardTypeEnum(Enum):
    """Card type."""
    CHARACTER = "Character"
    EVENT = "Event"
    CLIMAX = "Climax"


class CardColorEnum(Enum):
    """Card Color."""
    BLUE = "Blue"
    YELLOW = "Yellow"
    RED = "Red"
    GREEN = "Green"
    PURPLE = "Purple"


class CardSideEnum(Enum):
    """Card Side."""
    WEISS = "Weiss"
    SCHWARZ = "Schwarz"


class CardTriggerEnum(Enum):
    """Card Trigger."""
    SOUL = "Soul"
    GATE = "Gate"
    DRAW = "Draw"
    COMEBACK = "Comeback"
    SHOT = "Shot"
    RETURN = "Return"
    POOL = "Pool"
    TREASURE = "Treasure"
    STANDBY = "Standby"


class CardRarityEnum(Enum):
    """Card Rarity."""
    SP = "SP"
    RRR = "RRR"
    SR = "SR"
    RR = "RR"
    R = "R"
    U = "U"
    C = "C"
    CR = "CR"
    CC = "CC"
    TD = "TD"
    PR = "PR"


class CardExtraRarityEnum(Enum):
    """Card Extra Rarity. For cases when a card has the same rarity but different code."""
    S = "S"


class LanguageEnum(Enum):
    """Language Enum."""
    EN = "en"
    JP = "jp"
    CH = "ch"
