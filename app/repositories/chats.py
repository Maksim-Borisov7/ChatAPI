from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import ChatModels


class ChatRepository:
    """
    Репозиторий для работы с чатами.

    Отвечает за CRUD-операции над моделью ChatModels:
    - создание чата,
    - получение чата по id,
    - удаление чата.
    """

    model = ChatModels

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.
        """
        self.session = session

    async def create_chat(self, title: str) -> ChatModels:
        """
        Создать новый чат.

        Args:
            title (str): Заголовок чата.

        Returns:
            ChatModels: Созданный объект чата с заполненным id и created_at.
        """
        chat = self.model(title=title)
        self.session.add(chat)
        await self.session.commit()
        return chat

    async def get_chat(self, chat_id: int) -> ChatModels | None:
        """
        Получить чат по идентификатору.

        Args:
            chat_id (int): ID чата.

        Returns:
            ChatModels | None: Найденный чат или None, если не найден.
        """
        query = select(self.model).where(self.model.id == chat_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_chat(self, chat: ChatModels) -> None:
        """
        Удалить чат.

        Args:
            chat (ChatModels): Объект чата для удаления.

        Returns:
            None
        """
        await self.session.delete(chat)
        await self.session.commit()
