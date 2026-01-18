from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей SQLAlchemy.

    Используется как корневой класс декларативных моделей.
    Все модели приложения должны наследоваться от данного класса.
    """
    pass


class ChatModels(Base):
    """
    ORM-модель таблицы `chat`.

    Описывает чат в системе.

    Атрибуты:
       id (int): Уникальный идентификатор чата.
       title (str): Название чата. Не может быть пустым.
       created_at (datetime): Дата и время создания чата.
       messages (list[MessageModels]): Связанные сообщения чата.

    Связи:
       Один чат может иметь много сообщений.
       При удалении чата все связанные сообщения удаляются каскадно.
   """
    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now())
    messages: Mapped[list["MessageModels"]] = relationship(
        "MessageModels",
        back_populates="chats",
        cascade="all, delete-orphan"
    )


class MessageModels(Base):
    """
    ORM-модель таблицы `message`.

    Описывает сообщение, принадлежащее конкретному чату.

    Атрибуты:
        id (int): Уникальный идентификатор сообщения.
        chat_id (int): Идентификатор чата, к которому относится сообщение.
        text (str): Текст сообщения. Не может быть пустым.
        created_at (datetime): Дата и время создания сообщения.
        chats (ChatModels): Связанный объект чата.

    Связи:
        Каждое сообщение принадлежит одному чату.
    """
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    chats: Mapped["ChatModels"] = relationship(
        "ChatModels",
        back_populates="messages"
    )

