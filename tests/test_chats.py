import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_chat_and_send_message():
    """
    Проверяет создание чата и отправку сообщения и работу API
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        chat_resp = await client.post("/chats/", json={"title": "Тестовый чат"})
        assert chat_resp.status_code == 201
        chat_data = chat_resp.json()
        assert "id" in chat_data
        assert chat_data["title"] == "Тестовый чат"
        chat_id = chat_data["id"]

        message_resp = await client.post(f"/chats/{chat_id}/messages/", json={"id": chat_id, "text": "Привет"})
        assert message_resp.status_code == 201
        msg_data = message_resp.json()
        assert msg_data["chat_id"] == chat_id
        assert msg_data["text"] == "Привет"
        assert "id" in msg_data

        get_resp = await client.get(f"/chats/{chat_id}?limit=20")
        assert get_resp.status_code == 200
        chat_with_messages = get_resp.json()
        assert chat_with_messages["id"] == chat_id
        assert chat_with_messages["title"] == "Тестовый чат"
        assert isinstance(chat_with_messages["messages"], list)
        assert len(chat_with_messages["messages"]) == 1
        assert chat_with_messages["messages"][0]["text"] == "Привет"

        bad_chat_resp = await client.post("/chats/", json={"title": ""})
        assert bad_chat_resp.status_code == 422

        bad_msg_resp = await client.post(
            "/chats/9999/messages/",
            json={"text": "Тест"}
        )
        assert bad_msg_resp.status_code == 404
