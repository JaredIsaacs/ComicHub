from abc import ABC, abstractmethod

from requests import Session

from src.scrapers.Comic import Comic

class Scraper(ABC):
    def __init__(self, base_url):
        self.base_url = "https://" + base_url

        self.name = "Base Scraper"
        self.session = Session()

    @abstractmethod
    def get_all_comics(self) -> list[Comic]:
        pass
    
    @abstractmethod
    def get_comic(self, title: str) -> Comic:
        pass