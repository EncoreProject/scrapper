import re
from typing import List, Set
from urllib.request import urlopen

from bs4 import BeautifulSoup

from src.domain.entity import CardEntity
from src.repo.interface import ScrapperInterface


class WeissSchwarzYuyuteiScrapper(ScrapperInterface):
    _URL = "https://yuyu-tei.jp/game_ws/sell/sell_price.php?ver={}"
    CARD_REGEXP = re.compile('[^a-zA-Z0-9/-]')
    RARITY_REGEXP = re.compile('[a-zA-Z]+$')

    def get_cards(self, web_code: str) -> List[CardEntity]:
        cards_ids = self._get_cards_codes(web_code=web_code)
        return self._generate_cards(cards_ids=cards_ids)

    def _generate_cards(self, *, cards_ids: Set[str]) -> List[CardEntity]:
        self._get_cards_rarity(cards_ids=cards_ids)
        return

    def _get_cards_rarity(self, *, cards_ids: Set[str]):
        cards_rarity = {}
        for card_id in cards_ids:
            code = self.RARITY_REGEXP.sub('', card_id)
            rarity = self.RARITY_REGEXP.findall('FS/S34-076R')[0]
            if code in cards_rarity:
                cards_rarity[code].append()
            else:
                cards_rarity[code] = []

    def _get_cards_codes(self, *, web_code: str) -> Set[str]:
        html = urlopen(self._URL.format(web_code))
        bs = BeautifulSoup(html, 'html.parser')
        return {self.CARD_REGEXP.sub('', element.text) for element in bs.find_all(class_="id")}


if __name__ == '__main__':
    a = WeissSchwarzYuyuteiScrapper().get_cards('fsubw')
