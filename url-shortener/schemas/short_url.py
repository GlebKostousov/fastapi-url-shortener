from pydantic import BaseModel, AnyHttpUrl
from typing import Annotated
from annotated_types import MaxLen, MinLen

Description = Annotated[str, MaxLen(200)]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Description


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: Annotated[str, MinLen(2), MaxLen(20)]
    description: str
    visits: int = 42


class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания сокращенной ссылки
    """

    # noinspection PyTypeHints
    slug: Annotated[str, MaxLen(200)]
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
