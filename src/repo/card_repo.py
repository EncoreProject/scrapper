"""Card repository."""

from src.domain.interface import CardRepositoryInterface


class CardRepo(CardRepositoryInterface):
    """Card repo object"""
    def get_cards(self):
        pass
