from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logs.logger import logger
from app.api.chats import router as chats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла FastAPI.

    Используется для:
    - Логирования запуска и завершения сервера
    - Создания таблиц в базе данных при старте

    Args:
        app (FastAPI): Экземпляр FastAPI приложения.
    """
    try:
        logger.info("Запуск сервера")
        yield
        logger.info("Выключение сервера")
    except ConnectionRefusedError as e:
        logger.warning(f"Не удалось подключиться к БД: {e}")


app = FastAPI(lifespan=lifespan)
app.include_router(chats_router)
