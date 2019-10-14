"""Value object"""
from dataclasses import dataclass
from typing import Optional

from src.domain.enum import LanguageEnum, CardRarityEnum, CardExtraRarityEnum


@dataclass
class CardRarityInfoValueObject:
    """Card rarity info value object"""
    language: LanguageEnum
    rarity: CardRarityEnum
    extra: Optional[CardExtraRarityEnum]
    img: str


@dataclass
class CardTextValueObject:
    """Card text value object"""
    card_name: str
    text: str
    flavor_text: str
