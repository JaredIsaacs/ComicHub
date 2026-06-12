from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scrapers.Scraper import Scraper

@dataclass
class Comic():
    scraper: Scraper

    # Required fields
    name: str
    cover_image_url: str
    slug: str

    # Optional fields
    chapter_count: float = 0.0
    status: str | None = None

    # Fields for Metadata class.
    """ tags: list[str] | None = None
    description: str | None = None
    rating: float = 0.0
    review_count: int = 0
     """
    

    def get_details(self):
        return self.scraper.get_comic(self.slug)