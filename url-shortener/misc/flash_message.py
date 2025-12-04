"""The module is responsible for flash message on pages working with Short URL"""

__all__ = (
    "create_flash_message",
    "get_flashed_message",
)

from typing import Literal, TypedDict

from fastapi.requests import Request

from core.const import FLASHED_MESSAGES_KEY

type MessageCategory = Literal["success", "warning", "danger", "info"]


class Message(TypedDict):
    message: str
    category: MessageCategory


def create_flash_message(
    request: Request,
    message: str,
    category: MessageCategory = "info",
) -> None:
    if FLASHED_MESSAGES_KEY not in request.session:
        request.session[FLASHED_MESSAGES_KEY] = []
    request.session[FLASHED_MESSAGES_KEY].append(
        Message(
            message=message,
            category=category,
        ),
    )


def get_flashed_message(request: Request) -> list[Message]:
    messages: list[Message] = request.session.pop(FLASHED_MESSAGES_KEY, [])
    return messages
