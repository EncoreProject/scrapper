from abc import ABCMeta, abstractmethod
from typing import Set

from src.domain.entity import CardEntity


class ScrapperInterface(ABCMeta):

    @abstractmethod
    def get_cards(self, url: str) -> Set[CardEntity]:
        """Get cards from scrapper."""
