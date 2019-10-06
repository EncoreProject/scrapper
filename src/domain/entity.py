from dataclasses import dataclass
from typing import Tuple, Dict, Optional

from src.domain.enum import CardTypeEnum, CardTriggerEnum, CardSideEnum, CardColorEnum, LanguageEnum
from src.domain.value_object import CardRarityInfoValueObject, CardTextValueObject


@dataclass
class ExpansionEntity:
    """Expansion Entity."""
    id: int
    name: str


@dataclass
class CardEntity:
    """Card Entity."""
    card_number: Dict[LanguageEnum, str]
    id: Optional[int] = None
    expansion: Optional[ExpansionEntity] = None
    type: Optional[CardTypeEnum] = None
    level: Optional[int] = None
    power: Optional[int] = None
    trigger: Optional[Tuple[CardTriggerEnum]] = None
    rarity: Optional[Tuple[CardRarityInfoValueObject]] = None
    side: Optional[CardSideEnum] = None
    color: Optional[CardColorEnum] = None
    cost: Optional[int] = None
    soul: Optional[int] = None
    special_attribute: Optional[Tuple[str]] = None
    text: Optional[Dict[LanguageEnum, CardTextValueObject]] = None

    def get_jap_code(self):
        if LanguageEnum.JP in self.card_number:
            return self.card_number[LanguageEnum.JP]

        card_number = list(self.card_number.values())[0]
        index = card_number.find("-") + 1

        jap_card_number = card_number[0:index] + card_number[index+1:]
        return jap_card_number

    def __hash__(self):
        return hash(self.get_jap_code())
