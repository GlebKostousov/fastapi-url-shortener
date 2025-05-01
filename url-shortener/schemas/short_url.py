from pydantic import BaseModel, AnyHttpUrl
from typing import Annotated
from annotated_types import Len, MaxLen

Description = Annotated[str, MaxLen(200)]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Description = ""


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str


class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания сокращенной ссылки
    """

    # noinspection PyTypeHints
    slug: Annotated[str, MaxLen(200)]


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления информации о сокращенной ссылке
    """

    description: Description


class ShortUrlPartialUpdate(ShortUrlBase):
    target_url: AnyHttpUrl | None = None
    description: Description | None = None
