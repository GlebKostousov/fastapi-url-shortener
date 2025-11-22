import datetime
from datetime import date

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter()


@router.get(
    path="/",
    include_in_schema=False,
)
def read_root(
    request: Request,
) -> HTMLResponse:
    context: dict[str, date | list[str]] = {}
    features: list[str] = [
        "Create short URLs",
        "Track all redirects",
        "Real-time statistics",
        "Shared management",
    ]
    today = datetime.datetime.now(tz=datetime.UTC).date()
    context.update(
        today=today,
        features=features,
    )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )
