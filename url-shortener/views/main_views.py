from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from templating import templates

if TYPE_CHECKING:
    from datetime import date

router = APIRouter()


@router.get(
    path="/",
    name="home",
)
def home_page(
    request: Request,
) -> HTMLResponse:
    context: dict[str, date | list[str]] = {}
    features: list[str] = [
        "Create short URLs",
        "Track all redirects",
        "Real-time statistics",
        "Shared management",
    ]
    context.update(
        features=features,
    )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )


@router.get(
    path="/about/",
    name="about",
)
def about_pages(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )
