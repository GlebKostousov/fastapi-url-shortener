class ShortUrlBaseError(Exception):
    """Base exception for short url CRUD actions"""


class ShortUrlAlreadyExistsError(ShortUrlBaseError):
    """Raised when short url already exists"""

    def __init__(self, slug: str) -> None:
        self.slug = slug
