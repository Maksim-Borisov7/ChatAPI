from fastapi import HTTPException
from starlette import status

from app.database.models import ChatModels
from app.logs.logger import logger
from app.repositories.chats import ChatRepository
from app.schemas.chats import ChatSchemas


class CreateChatUseCase:
    """
    UseCase для создания  чата.

    Attributes:
        repo (ChatRepository): Репозиторий для работы с чатами в базе данных.

    Methods:
        execute(data: ChatSchemas) -> ChatModels:
            Создает чат с указанным заголовком.
            Логирует процесс и выбрасывает HTTPException при ошибках.
    """

    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def execute(self, data: ChatSchemas) -> ChatModels:
        """
        Создает новый чат с указанным заголовком.

        Args:
            data (ChatSchemas): Pydantic-схема с заголовком чата.

        Returns:
            ChatModels: Объект созданного чата.

        Raises:
            HTTPException 500: Если возникла ошибка при создании чата.
        """
        logger.info(f"Попытка создать чат с title='{data.title}'")
        try:
            chat = await self.repo.create_chat(data.title)
            logger.info(f"Чат '{data.title}' успешно создан с id={chat.id}")
            return chat
        except Exception as e:
            logger.error(f"Ошибка при создании чата '{data.title}': {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not create chat: {str(e)}"
            )

