from pydantic import BaseModel, Field, field_validator


class ChatSchemas(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    @field_validator("title")
    @staticmethod
    def validate_title(v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
        return v


class ChatWithMessagesSchema(BaseModel):
    id: int
    limit: int = Field(20, ge=20, le=100)
