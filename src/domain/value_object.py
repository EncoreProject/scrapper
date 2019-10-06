from dataclasses import dataclass

from src.domain.enum import LanguageEnum, CardRarityEnum, CardExtraRarityEnum


@dataclass
class CardRarityInfoValueObject:
    language: LanguageEnum
    rarity: CardRarityEnum
    is_extra: CardExtraRarityEnum
    img: str


@dataclass
class CardTextValueObject:
    card_name: str
    text: str
    flavor_text: str
