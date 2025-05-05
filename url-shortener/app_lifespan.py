from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.api_v1.short_urls.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    # действия  до запуска приложения
    storage.init_storage_from_state()
    # ставим функцию на паузу
    yield
    # выполняем завершение работы
