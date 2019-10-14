"""Entities Module"""
import logging
import re
from dataclasses import dataclass
from typing import Tuple, Dict, Optional, List

from src.domain.enum import CardTypeEnum, CardTriggerEnum, CardSideEnum, CardColorEnum, LanguageEnum
from src.domain.errors import CardError
from src.domain.value_object import CardRarityInfoValueObject, CardTextValueObject

LOGGER = logging.getLogger('basic_logger')


@dataclass
class ExpansionEntity:
    """Expansion Entity."""
    expansion_id: int
    name: str


@dataclass  # pylint: disable=too-many-instance-attributes
class CardEntity:
    """Card Entity."""
    _REGEXP_GENERIC_CODE = re.compile('^[A-Z]+/[A-Z]+[0-9]+-[0-9]+$')  # pylint: disable=invalid-name

    card_number: Dict[LanguageEnum, str]
    card_id: Optional[int] = None
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
                LOGGER.error("Card number value is None in language %s", language.value)
            # else:

        # for card_number in self.card_number.values():
        #    if card_number is None:
        #        LOGGER

    def _check_id(self) -> List[CardError]:
        pass

    def _check_expansion(self) -> List[CardError]:
        pass

    def _check_type(self) -> List[CardError]:
        pass

    def _check_level(self) -> List[CardError]:
        pass

    def _check_power(self) -> List[CardError]:
        pass

    def _check_trigger(self) -> List[CardError]:
        pass

    def _check_rarity(self) -> List[CardError]:
        pass

    def _check_side(self) -> List[CardError]:
        pass

    def _check_color(self) -> List[CardError]:
        pass

    def _check_cost(self) -> List[CardError]:
        pass

    def _check_soul(self) -> List[CardError]:
        pass

    def _check_special_attribute(self) -> List[CardError]:
        pass

    def _check_text(self) -> List[CardError]:
        pass

    def check(self):
        """Check all possible errors in current CardEntity."""
        # error_list = []
        # self._check_id()

    def get_generic_code(self):
        """get """
        card_number = list(self.card_number.values())[0]
        if self._REGEXP_GENERIC_CODE.match(card_number):
            return card_number

        index = card_number.find("-") + 1
        jap_card_number = card_number[0:index] + card_number[index + 1:]
        return jap_card_number

    def __hash__(self):
        return hash(self.get_generic_code())

    def __eq__(self, other):
        return self.get_generic_code() == other.get_generic_code()
