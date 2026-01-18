from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class ChatResponseSchema(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponseSchema(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatWithMessagesResponseSchema(ChatResponseSchema):
    messages: List[MessageResponseSchema]
