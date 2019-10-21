"""JKTCG Scrapper"""
import re
from dataclasses import dataclass
from typing import List, Set, Dict, Optional

from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup, Comment, Tag

from src.domain.entity import CardEntity
from src.domain.enum import LanguageEnum, CardRarityEnum
from src.domain.value_object import CardRarityInfoValueObject
from src.repo.scrapper.common_scrapper import CommonScrapper
from src.repo.scrapper.interface import ScrapperInterface


@dataclass
class TagListByRarity:
    """Stores a list of BeautifulSoup tags containing cards of the specified rarity"""
    rarity: CardRarityEnum
    tag_list: List[Tag]


class JKTCGScrapper(ScrapperInterface, CommonScrapper):
    """JKTCG Scrapper object"""
    _URL = "http://jktcg.com/WS_EN/"
    RARITY_DICT = {"SP": CardRarityEnum.SP,
                   "RRR": CardRarityEnum.RRR,
                   "SR": CardRarityEnum.SR,
                   "RR": CardRarityEnum.RR,
                   "R": CardRarityEnum.R,
                   "UC": CardRarityEnum.U,  # On JKTCG the uncommon code is UC
                   "C": CardRarityEnum.C,
                   "CR": CardRarityEnum.CR,
                   "CC": CardRarityEnum.CC,
                   "TD": CardRarityEnum.TD,
                   "PR": CardRarityEnum.PR}

    @staticmethod
    def _tags_between(start: Tag, end: Optional[Tag]) -> List[Tag]:
        """
        Returns a list of the tags between start and end.
        :param start: The starting Tag. The first considered tag is the next sibling from start.
        :param end: The ending tag. The last considered tag is the previous sibling from end. If end is None, the
                    function will return a list of Tag from start until the end of the document.
        :return: A list of Tag between start and end.
        """
        cur = start.next_sibling
        tag_list = []
        while cur and cur != end:
            if cur.name is not None:
                tag_list.append(cur)
            cur = cur.next_sibling
        return tag_list

    @staticmethod
    def _split_and_strip_all(text: str) -> str:
        """
        Split the words of a text and joins them after stripping each word.
        :param text: The original text.
        :return: The text after stripping each word.
        """
        split_text = text.split()

        new_text = ""
        for text_i in split_text:
            new_text += text_i.strip()
        return new_text

    @staticmethod
    def _get_rarity_code_from_title(rarity_title: str) -> str:
        """
        Given a title containing a card rarity, extracts its rarity and returns it.
        :param rarity_title: The title of a JKTCG's booster page which contains a card's rarity.
        :return: The card rarity in rarity_title.
        """
        rarity_word = rarity_title.split()[0]
        if rarity_word[-1:] == "-":
            correct_rarity_len = len(rarity_word) - 1
            return rarity_word[:correct_rarity_len]
        return rarity_word

    @staticmethod
    def _clean_beautiful_soup_document(soup: BeautifulSoup) -> BeautifulSoup:
        """ Cleans the html document of comments, br and empty lines inside td.
        :param soup: An initialized document.
        :return: The document wihout comments, br or empty lines inside td.
        """
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        for tag in soup.find_all('br'):
            tag.extract()

        for tag in soup.find_all('td'):
            for content in tag.contents:
                if str(content).strip() == '':
                    content.extract()
        return soup

    def _get_tags_by_rarity(self, soup: BeautifulSoup) -> List[TagListByRarity]:
        """
        Get the tags containing cards by its rarity from an initialized BeautifulSoup document.
        :param soup: The initialized BeautifulSoup document.
        :return: A list of tags by rarity.
        """
        rarity_nodes = soup.find_all('h1')
        rarity_nodes.pop(0)  # Removes expansion title

        # Stores all the tags containing cards (which are tables) by its rarity.
        cards_by_rarity = []
        for i, current_node in enumerate(rarity_nodes, 0):
            if i == len(rarity_nodes) - 1:
                card_tag_list = self._tags_between(current_node, None)
            else:
                next_node = rarity_nodes[i + 1]
                card_tag_list = self._tags_between(current_node, next_node)
            rarity_code = self._get_rarity_code_from_title(rarity_nodes[i].contents[0].strip())
            rarity = self.RARITY_DICT[rarity_code]
            tag_list_by_rarity = TagListByRarity(rarity=rarity, tag_list=card_tag_list)
            cards_by_rarity.append(tag_list_by_rarity)
        return cards_by_rarity

    def _get_common_id(self, card_number: str) -> Optional[str]:
        """
        Tries to extract the common part of the card_number.
        :param card_number: The card_number got from JKTCG.
        :return: The card_number without its rarity or None if it has a wrong format.
        """
        result = re.findall(self._CARD_COMMON_ID_REGEXP, card_number)
        if len(result) == 0:
            return None
        return result[0]

    def get_card_dict_from_tags(self, tags_by_rarity_list: List[TagListByRarity], full_url: str) \
            -> Dict[str, CardEntity]:
        """
        Obtain a card dictionary from a list of tags by rarity
        :param tags_by_rarity_list: the list of tags by rarity.
        :param full_url: the full url to the current expansion.
        :return: A dictionary of CardEntity by card_number. card_number can be None if it doesn't match CARD_NUMBER_RE.
        """
        card_dict = {}
        for tags_by_rarity in tags_by_rarity_list:
            # For JKTCG a html table is a "row"
            for table in tags_by_rarity.tag_list:
                item_values = table.find_all('td')
                item_values = [node for node in item_values if node.contents[0].strip() != '']

                for node in item_values:
                    card_number = self._get_common_id(str(node.contents[0]).strip())

                    # Gets card's image src to construct a CardRarityInfoValueObject
                    img_node = node.find('img')
                    if img_node is None:
                        img_src = None
                    else:
                        img_src = self._split_and_strip_all(img_node['src'])
                    img_src = urljoin(full_url, img_src)
                    rarity_info = CardRarityInfoValueObject(
                        language=LanguageEnum.EN,
                        rarity=tags_by_rarity.rarity,
                        extra=None,
                        img=img_src)

                    # Adds the new rarity info if the card exists or it creates a new one with full info if not.
                    if card_number in card_dict:
                        card_dict[card_number].rarity.append(rarity_info)
                    else:
                        card_text = node.contents[6].string.strip()

                        card = CardEntity(
                            card_number={LanguageEnum.EN: card_number},
                            rarity=[rarity_info],
                            text={LanguageEnum.EN: card_text})
                        card_dict[card_number] = card
        return card_dict

    def get_cards(self, *, web_code: str) -> Set[CardEntity]:
        """
        Scrap the given url and returns a set of the found cards.
        :param web_code: The expansion code in JKTCG. It can be located in its url: "http://jktcg.com/web_code/"
        :return: A set of CardEntity of the found cards.
        """
        full_url = self._URL + web_code + "/" + web_code + ".html"
        response = requests.get(full_url)
        html = response.content

        soup = BeautifulSoup(html, "html5lib")
        soup = self._clean_beautiful_soup_document(soup)

        tags_by_rarity = self._get_tags_by_rarity(soup=soup)

        card_dict = self.get_card_dict_from_tags(tags_by_rarity_list=tags_by_rarity, full_url=full_url)
        return set(card_dict.values())
