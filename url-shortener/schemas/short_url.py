__all__ = (
    "ShortUrl",
    "ShortUrlCreate",
    "ShortUrlPartialUpdate",
    "ShortUrlRead",
    "ShortUrlUpdate",
)

from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import AnyHttpUrl, BaseModel

from core.const import MAX_LENGTH_DESCRIPTION

Description = Annotated[str, MaxLen(MAX_LENGTH_DESCRIPTION)]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Description = ""


class ShortUrl(ShortUrlBase):
    """Модель сокращенной ссылки"""

    slug: Annotated[str, MinLen(2), MaxLen(20)]
    description: str
    visits: int = 42


class ShortUrlCreate(ShortUrlBase):
    """Модель для создания сокращенной ссылки"""

    # noinspection PyTypeHints
    slug: Annotated[str, MinLen(2), MaxLen(20)]
    description: Description = ""


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления информации о сокращенной ссылке
    """


class ShortUrlPartialUpdate(BaseModel):
    target_url: AnyHttpUrl | None = None
    description: Description | None = None


class ShortUrlRead(ShortUrlBase):
    """
    Модель для чтения данных по короткой ссылке
    """

    slug: str
    description: str
