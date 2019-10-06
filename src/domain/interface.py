from abc import ABCMeta, abstractmethod
from typing import Set

from src.domain.entity import CardEntity


class CardRepositoryInterface(ABCMeta):
    """Card repository that get cards."""

    @abstractmethod
    def get_cards(self) -> Set[CardEntity]:
        """Method that get cards that are configured in config.yaml."""


