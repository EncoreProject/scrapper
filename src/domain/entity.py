import logging
from dataclasses import dataclass
from typing import Tuple, Dict, Optional, List, Union

from src.domain.enum import CardTypeEnum, CardTriggerEnum, CardSideEnum, CardColorEnum, LanguageEnum
from src.domain.errors import CardTestError
from src.domain.value_object import CardRarityInfoValueObject, CardTextValueObject

LOGGER = logging.getLogger('basic_logger')


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
    rarity: Optional[List[CardRarityInfoValueObject]] = None
    side: Optional[CardSideEnum] = None
    color: Optional[CardColorEnum] = None
    cost: Optional[int] = None
    soul: Optional[int] = None
    special_attribute: Optional[Tuple[str]] = None
    text: Optional[Dict[LanguageEnum, CardTextValueObject]] = None

    def _check_card_number(self):
        if self.card_number is None:
            LOGGER.error("Card number is None")
            return

        for language, card_number in self.card_number.items():
            if card_number is None:
                LOGGER.error(f"Card number value is None in language {language.value}")
            # else:

        # for card_number in self.card_number.values():
        #    if card_number is None:
        #        LOGGER

    def _check_id(self) -> List[CardTestError]:
        pass

    def _check_expansion(self) -> List[CardTestError]:
        pass

    def _check_type(self) -> List[CardTestError]:
        pass

    def _check_level(self) -> List[CardTestError]:
        pass

    def _check_power(self) -> List[CardTestError]:
        pass

    def _check_trigger(self) -> List[CardTestError]:
        pass

    def _check_rarity(self) -> List[CardTestError]:
        pass

    def _check_side(self) -> List[CardTestError]:
        pass

    def _check_color(self) -> List[CardTestError]:
        pass

    def _check_cost(self) -> List[CardTestError]:
        pass

    def _check_soul(self) -> List[CardTestError]:
        pass

    def _check_special_attribute(self) -> List[CardTestError]:
        pass

    def _check_text(self) -> List[CardTestError]:
        pass

    def check(self):
        error_list = []

        return error_list

    def get_jap_code(self):
        if LanguageEnum.JP in self.card_number:
            return self.card_number[LanguageEnum.JP]

        card_number = list(self.card_number.values())[0]
        index = card_number.find("-") + 1

        jap_card_number = card_number[0:index] + card_number[index+1:]
        return jap_card_number

    def __hash__(self):
        return hash(self.get_jap_code())

    def __eq__(self, other):
        return self.get_jap_code() == other.get_jap_code()
