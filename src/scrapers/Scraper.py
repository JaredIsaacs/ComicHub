from abc import ABC, abstractmethod
import importlib

from requests import Session

from src.scrapers.comic import Comic

class Scraper(ABC):
    def __init__(self, base_url):
        self.base_url = "https://" + base_url

        self.name = "Base Scraper"
        self.session = Session()


    @staticmethod
    def get_scraper(class_name: str, base_url: str) -> Scraper:
        module = importlib.import_module(f"src.scrapers.{class_name}")
        scraper_class = getattr(module, class_name)

        return scraper_class(base_url)


    @abstractmethod
    def get_all_comics(self) -> list[Comic]:
        pass
    
    @abstractmethod
    def get_comic(self, slug: str) -> Comic:
        pass