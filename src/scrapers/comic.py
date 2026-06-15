"""Data class used to hold data from scraped websites.

This is basically the data template all scrapers need to be able to return.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scrapers.scraper import Scraper

@dataclass
class Comic():
    """Data template all scrapers must be able to return."""

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


    def get_details(self) -> Comic:
        """Returns comic details using the scraper that originally fetched this comic."""

        return self.scraper.get_comic(self.slug)
