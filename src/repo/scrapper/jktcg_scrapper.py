"""JKTCG scrapper"""
from src.repo.scrapper.interface import ScrapperInterface


class JKTCGScrapper(ScrapperInterface):
    """JKTCG scrapper object"""
    def get_cards(self, *, web_code: str):
        pass
