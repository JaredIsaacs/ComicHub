from dataclasses import dataclass

@dataclass
class Comic():
    # Required fields
    name: str
    cover_image_url: str
    chapter_count: float

    # Optional Fields
    tags: list[str] | None = None
    description: str | None = None
    rating: float = 0.0
    review_count: int = 0