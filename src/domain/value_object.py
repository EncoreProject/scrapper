from dataclasses import dataclass
from typing import Optional

from src.domain.enum import LanguageEnum, CardRarityEnum, CardExtraRarityEnum


@dataclass
class CardRarityInfoValueObject:
    language: LanguageEnum
    rarity: CardRarityEnum
    extra: Optional[CardExtraRarityEnum]
    img: str



@dataclass
class CardTextValueObject:
    card_name: str
    text: str
    flavor_text: str
