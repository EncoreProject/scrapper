"""Interface"""
from abc import ABCMeta, abstractmethod
from typing import Set

from src.domain.entity import CardEntity


class ScrapperInterface(metaclass=ABCMeta):
    """Scrapper interface object"""
    @abstractmethod
    def get_cards(self, *, web_code: str) -> Set[CardEntity]:
        """Get cards from scrapper."""
