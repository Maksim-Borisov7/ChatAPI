from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.messages import MessageRepository
from app.use_case.create_chat import CreateChatUseCase
from app.repositories.chats import ChatRepository
from app.database.db import db
from app.use_case.get_chat import GetChatUseCase
from app.use_case.send_message import SendMessageUseCase
from app.use_case.delete_chat import DeleteChatUseCase


async def get_chat_repo(
    session: AsyncSession = Depends(db.get_session),
) -> ChatRepository:
    """Репозиторий для работы с чатами."""
    return ChatRepository(session)


async def get_message_repo(
    session: AsyncSession = Depends(db.get_session),
) -> MessageRepository:
    """Репозиторий для работы с сообщениями."""
    return MessageRepository(session)


async def get_create_chat_use_case(
    repo: ChatRepository = Depends(get_chat_repo),
) -> CreateChatUseCase:
    """UseCase для создания чата."""
    return CreateChatUseCase(repo)


async def get_send_message_use_case(
    chat_repo: ChatRepository = Depends(get_chat_repo),
    message_repo: MessageRepository = Depends(get_message_repo),
) -> SendMessageUseCase:
    """UseCase для отправки сообщения в чат."""
    return SendMessageUseCase(chat_repo, message_repo)


async def get_chat_use_case(
    chat_repo: ChatRepository = Depends(get_chat_repo),
    message_repo: MessageRepository = Depends(get_message_repo),
) -> GetChatUseCase:
    """UseCase для получения чата и последних сообщений."""
    return GetChatUseCase(chat_repo, message_repo)


async def get_delete_chat_use_case(
    repo: ChatRepository = Depends(get_chat_repo),
) -> DeleteChatUseCase:
    """UseCase для удаления чата вместе с сообщениями."""
    return DeleteChatUseCase(repo)