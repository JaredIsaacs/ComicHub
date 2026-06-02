from dataclasses import dataclass

@dataclass
class Comic():
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