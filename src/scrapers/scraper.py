"""Abstract class all Scraper classes should be built on."""

from abc import ABC, abstractmethod
import importlib

from requests import Session

from src.scrapers.comic import Comic

class Scraper(ABC):
    """Base class for all scrapers.
    
    If this is being used to scrape, something went majorly wrong.
    """

    def __init__(self, base_url):
        self.base_url = "https://" + base_url

        self.name = "Base Scraper"
        self.session = Session()


    @staticmethod
    def get_scraper(class_name: str, base_url: str) -> Scraper:
        """Static method used to dynamically allow the retrieval of a scraper class that
        derives from the base Scraper class.
        
        Requires:
            * class_name: str - this needs to be the name of the class under the scrapers folder, 
            as well as the name of the class in the config.json file. After an initial scrape this
            field can also be found in the database under the Source table.
            * base_url: str - the base_url of a source site. Can be found in the config file.
            
        Returns:
            * Scraper - the requested for class based on the Scraper class."""

        module = importlib.import_module(f"src.scrapers.{class_name}")
        scraper_class = getattr(module, class_name)

        return scraper_class(base_url)


    @abstractmethod
    def get_all_comics(self) -> list[Comic]:
        """Method used that returns a list of all comics from a selected source.
        
        Requires:
            * Nothing

        Returns:
            * list[Comic]
        """


    @abstractmethod
    def get_comic(self, slug: str) -> Comic:
        """Method that returns a specific comic provided a slug/id/name.
        
        Requires:
            * slug/id/name: str - This can be any of the speicified fields.

        Returns:
            Comic
        """
