from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    superuser_email: Optional[EmailStr] = None
    superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
