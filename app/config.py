from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из .env или по умолчанию.

    Attributes:
        host (str): Хост базы данных.
        user (str): Имя пользователя для подключения к БД.
        password (str): Пароль пользователя для подключения к БД.
        db_name (str): Название базы данных.
        port (str): Порт подключения к БД.
        pg_url (str): Полный URL подключения к PostgreSQL.
        echo (bool): Включение логирования SQL-запросов (по умолчанию False).
    """

    host: str
    user: str
    password: str
    db_name: str
    port: str
    pg_url: str
    echo: bool = False

    class Config:
        """Настройки для работы с .env файлом."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
