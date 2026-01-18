from typing import Annotated

from fastapi import APIRouter, Depends, status
from app.dependencies.repositories import (
    get_create_chat_use_case,
    get_send_message_use_case,
    get_chat_use_case,
    get_delete_chat_use_case,
)
from app.schemas.chats import ChatSchemas, ChatWithMessagesSchema
from app.schemas.messages import MessageSchemas
from app.schemas.responses import ChatResponseSchema, MessageResponseSchema, ChatWithMessagesResponseSchema
from app.use_case.create_chat import CreateChatUseCase
from app.use_case.delete_chat import DeleteChatUseCase
from app.use_case.get_chat import GetChatUseCase
from app.use_case.send_message import SendMessageUseCase

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_chat(
    data: ChatSchemas,
    use_case: CreateChatUseCase = Depends(get_create_chat_use_case)
):
    """
    Создать новый чат.

    Args:
        data (ChatSchemas): Схема Pydantic с заголовком чата.
        use_case (CreateChatUseCase): UseCase для создания чата.

    Returns:
        ChatResponseSchema: Созданный чат с ID, заголовком и временем создания.

    Raises:
        HTTPException 500: Если не удалось создать чат.
    """
    return await use_case.execute(data)


@router.post("/{id}/messages/", response_model=MessageResponseSchema, status_code=status.HTTP_201_CREATED)
async def send_message_in_chat(
    id: int,
    data: MessageSchemas,
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
):
    """
    Отправить сообщение в существующий чат.

    Args:
        id (int): ID чата, в который отправляется сообщение.
        data (MessageSchemas): Схема Pydantic с текстом сообщения.
        use_case (SendMessageUseCase): UseCase для отправки сообщения.

    Returns:
        MessageResponseSchema: Созданное сообщение с ID, текстом, chat_id и временем создания.

    Raises:
        HTTPException 404: Если чат с указанным chat_id не существует.
        HTTPException 500: Если сообщение не удалось сохранить.
    """
    return await use_case.execute(id, data.text)


@router.get("/{id}", response_model=ChatWithMessagesResponseSchema)
async def get_chat_with_messages(
    id: int,
    data: Annotated[ChatWithMessagesSchema,Depends()],
    use_case: GetChatUseCase = Depends(get_chat_use_case),
) -> ChatWithMessagesResponseSchema:
    """
    Получить чат и последние N сообщений.

    Args:
        id (int): ID чата.
        limit (int): Количество сообщений для возврата (по умолчанию 20, максимум 100).
        use_case (GetChatUseCase): UseCase для получения чата и сообщений.

    Returns:
        ChatWithMessagesResponseSchema: Чат и список сообщений, отсортированных по created_at.

    Raises:
        HTTPException 404: Если чат с указанным ID не найден.
        HTTPException 500: Если возникла ошибка при получении сообщений.
    """
    chat, messages = await use_case.execute(id, data.limit)
    return ChatWithMessagesResponseSchema(
        id=chat.id,
        title=chat.title,
        created_at=chat.created_at,
        messages=messages
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_and_messages(
    id: int,
    use_case: DeleteChatUseCase = Depends(get_delete_chat_use_case),
):
    """
    Удалить чат вместе со всеми его сообщениями.

    Args:
        id (int): ID чата для удаления.
        use_case (DeleteChatUseCase): UseCase для удаления чата.

    Returns:
        None: Возвращает 204 No Content при успешном удалении.

    Raises:
        HTTPException 404: Если чат с указанным ID не найден.
        HTTPException 500: Если удаление не удалось.
    """
    return await use_case.execute(id)
