from fastapi import HTTPException
from starlette import status

from app.logs.logger import logger
from app.repositories.chats import ChatRepository


class DeleteChatUseCase:
    """
    UseCase для удаления чата вместе со всеми сообщениями.

    Attributes:
        repo (ChatRepository): Репозиторий для работы с чатами.

    Methods:
        execute(id: int) -> None:
            Удаляет чат по ID. Логирует процесс и выбрасывает HTTPException при ошибках.
    """
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def execute(self, id: int) -> HTTPException:
        """
        Удаляет чат по указанному ID.

        Args:
            id (int): ID чата для удаления.

        Returns:
            HTTPException

        Raises:
            HTTPException 404: Если чат с указанным ID не найден.
            HTTPException 500: Если произошла ошибка при удалении чата.
        """
        logger.info(f"Попытка удалить чат с id={id}")
        chat = await self.repo.get_chat(id)
        if not chat:
            logger.warning(f"Чат с id={id} не найден")
            raise HTTPException(status_code=404, detail="Chat not found")
        try:
            await self.repo.delete_chat(chat)
            logger.info(f"Чат с id={id} успешно удалён")

        except Exception as e:
            logger.warning(f"Чат с id={id} не найден")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Could not delete chat: {str(e)}")
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
