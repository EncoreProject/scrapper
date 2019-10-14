"""Common Scrapper"""
import re
from typing import Optional

from src.domain.enum import CardExtraRarityEnum, CardRarityEnum


class CommonScrapper:
    """Common scrapper object"""
    _CARD_COMMON_ID_REGEXP = re.compile('^[A-Z]+/[A-Z]+[0-9]+-[A-Z]*[0-9]+')
    _CARD_EXTRA_RARITY = re.compile('[A-Z]+$')

    def _get_extra_rarity(self, *, rarity, card_id) -> Optional[CardExtraRarityEnum]:
        if rarity == CardRarityEnum.PR:
            search_extra = self._CARD_EXTRA_RARITY.search(card_id)
            if search_extra:
                return CardExtraRarityEnum(search_extra.group())
        return None
