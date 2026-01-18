from typing import Tuple, List

from fastapi import HTTPException
from starlette import status

from app.database.models import ChatModels, MessageModels
from app.logs.logger import logger
from app.repositories.chats import ChatRepository
from app.schemas.chats import ChatWithMessagesSchema
from app.repositories.messages import MessageRepository


class GetChatUseCase:
    """
    UseCase для получения чата и последних сообщений.

    Attributes:
        chat_repo (ChatRepository): Репозиторий для работы с чатами.
        message_repo (MessageRepository): Репозиторий для работы с сообщениями.

    Methods:
        execute(data: ChatWithMessagesSchema) -> tuple[ChatModels, list[MessageModels]]:
            Возвращает чат и список последних сообщений.
    """
    def __init__(self, chat_repo: ChatRepository, message_repo: MessageRepository):
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    async def execute(self, data: ChatWithMessagesSchema) -> tuple[ChatModels, list[MessageModels]]:
        """
        Получить чат и последние N сообщений.

        Args:
            data (ChatWithMessagesSchema): Схема с ID чата и параметром limit
                (количество сообщений для выборки, по умолчанию 20, максимум 100).

        Returns:
            tuple: (ChatModels, list[MessageModels])
                Чат и список сообщений, отсортированных по created_at.

        Raises:
            HTTPException 404: Если чат с указанным ID не найден.
            HTTPException 500: Если произошла ошибка при получении сообщений.
        """
        logger.info(f"Запрос на получение чата id={data.id} с последними {data.limit} сообщениями")

        chat = await self.chat_repo.get_chat(data.id)
        if not chat:
            logger.warning(f"Чат с id={data.id} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat with id={data.id} not found"
            )

        try:
            messages = await self.message_repo.get_last_messages(data.id, data.limit)
            logger.info(f"Получено {len(messages)} сообщений для чата id={data.id}")
        except Exception as e:
            logger.error(f"Ошибка при получении сообщений для чата id={data.id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not get messages for chat id={data.id}: {str(e)}"
            )

        return chat, messages




