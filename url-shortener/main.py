import logging

from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from api.redirect_views import router as redirect_views
from core.config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

app = FastAPI(title="URL Shortener")
app.include_router(main_router)

app.include_router(redirect_views)
app.include_router(api_router)
