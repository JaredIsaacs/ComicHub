"""Abstract class all Scraper classes should be built on."""

from abc import ABC, abstractmethod
from pkgutil import walk_packages
import importlib

from requests import Session
import src.scrapers

from src.scrapers.comic import Comic

class Scraper(ABC):
    """Base class for all scrapers.

    If this is being used to scrape, something went majorly wrong.
    """

    _class_registry = {}

    def __init__(self, base_url):
        self.base_url = "https://" + base_url

        self.name = "Base Scraper"
        self.session = Session()


    def __init_subclass__(cls):
        super().__init_subclass__()

        Scraper._class_registry[cls.__name__] = cls


    @staticmethod
    def initialize_registry():
        """Static method used to initialize scrapers into the base classes registry.

        Call this method before get_scraper()
        """

        if len(Scraper._class_registry) > 0:
            print("Registry already populated. Skipping scraper initialization.")
            return

        for _, module_name, _ in walk_packages(
            src.scrapers.__path__,
            src.scrapers.__name__ + "."
        ):
            importlib.import_module(module_name)


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

        if class_name not in Scraper._class_registry:
            raise ValueError(f"Class name, {class_name}, not in class registry.")

        return Scraper._class_registry[class_name](base_url)


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
