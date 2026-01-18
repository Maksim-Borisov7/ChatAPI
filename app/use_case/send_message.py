from fastapi import HTTPException
from starlette import status

from app.database.models import MessageModels
from app.logs.logger import logger
from app.repositories.chats import ChatRepository
from app.repositories.messages import MessageRepository


class SendMessageUseCase:
    """
      UseCase для отправки сообщения в чат.

      Attributes:
          chat_repo (ChatRepository): Репозиторий для работы с чатами.
          message_repo (MessageRepository): Репозиторий для работы с сообщениями.

      Methods:
          execute(data: MessageSchemas) -> MessageModels:
              Отправляет сообщение в чат и возвращает созданное сообщение.
      """
    def __init__(self, chat_repo: ChatRepository, message_repo: MessageRepository):
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    async def execute(self, chat_id: int, text: str) -> MessageModels:
        logger.info(f"Попытка отправки сообщения в чат id={chat_id}")
        chat = await self.chat_repo.get_chat(chat_id)
        if not chat:
            logger.warning(f"Чат с id={chat_id} не найден. Сообщение не отправлено.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat with id={chat_id} not found"
            )
        try:
            message = await self.message_repo.send_message(chat_id, text)
            logger.info(f"Сообщение успешно отправлено в чат id={chat_id}, message_id={message.id}")
            return message
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в чат id={chat_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not send message to chat id={chat_id}: {str(e)}"
            )



