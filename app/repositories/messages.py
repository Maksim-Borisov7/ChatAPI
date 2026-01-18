from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import MessageModels


class MessageRepository:
    """
    Репозиторий для работы с сообщениями.
    """

    model = MessageModels

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session = session

    async def send_message(self, chat_id: int, text: str) -> MessageModels:
        """
        Создать и сохранить сообщение в чате.

        Args:
            chat_id (int): ID чата.
            text (str): Текст сообщения.

        Returns:
            MessageModels: Созданное сообщение.
        """
        message = self.model(chat_id=chat_id, text=text)
        self.session.add(message)
        await self.session.commit()
        return message

    async def get_last_messages(self, chat_id: int, limit: int) -> list[MessageModels]:
        """
        Получить последние сообщения чата.

        Args:
            chat_id (int): ID чата.
            limit (int): Максимальное количество сообщений.

        Returns:
            list[MessageModels]: Список сообщений, отсортированных по убыванию created_at.
        """
        query = (
            select(self.model)
            .where(self.model.chat_id == chat_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
        )
        res = await self.session.execute(query)
        return list(res.scalars().all())
