# ruff: noqa: ARG001

import datetime
from datetime import date

from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR
from misc.flash_message import get_flashed_message


def inject_current_date_and_dt(request: Request) -> dict[str, date]:
    return {"today": datetime.datetime.now(tz=datetime.UTC).date()}


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[
        inject_current_date_and_dt,
    ],
)
templates.env.globals[get_flashed_message.__name__] = get_flashed_message
