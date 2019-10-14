"""Yuyutei Scrapper"""
import re
from typing import Dict
from urllib.request import urlopen

from bs4 import BeautifulSoup

from src.domain.entity import CardEntity
from src.domain.enum import LanguageEnum, CardRarityEnum
from src.domain.value_object import CardRarityInfoValueObject
from src.repo.scrapper.common_scrapper import CommonScrapper
from src.repo.scrapper.interface import ScrapperInterface


class WeissSchwarzYuyuteiScrapper(ScrapperInterface, CommonScrapper):
    """Yuyutei Scrapper object"""
    _URL_MAIN = 'https://yuyu-tei.jp'
    _URL = "https://yuyu-tei.jp/game_ws/sell/sell_price.php?ver={}"
    _CARD_CLEAN_ID = re.compile('[^A-Z0-9/-]')

    def get_cards(self, *, web_code):
        html = urlopen(self._URL.format(web_code))
        b_s = BeautifulSoup(html, 'html.parser')

        card_dict: Dict[str, CardEntity] = {}

        for element in b_s.find_all(class_="id"):
            card_clean_id = self._CARD_CLEAN_ID.sub('', element.text)
            card_common_id = self._CARD_COMMON_ID_REGEXP.search(card_clean_id).group()
            rarity = CardRarityEnum(element.parent.parent.parent.parent.find_all('em')[0].text)

            card_rarity = CardRarityInfoValueObject(
                language=LanguageEnum.JP,
                rarity=rarity,
                extra=self._get_extra_rarity(rarity=rarity,
                                             card_id=card_clean_id),
                img=self._URL_MAIN + element.parent.parent.find_all('img')[0].attrs['src'],
            )

            if card_common_id in card_dict:
                card_dict[card_common_id].rarity.append(card_rarity)
            else:
                card_entity = CardEntity(
                    card_number={LanguageEnum.JP: card_common_id},
                    rarity=[card_rarity],
                )
                card_dict[card_common_id] = card_entity

        return set(card_dict.values())
