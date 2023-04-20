from typing import Optional

from pydantic import BaseSettings, EmailStr

# field constants
USER_PASSWORD_MIN_LENGTH: int = 3
FIELD_MIN_LENGTH: int = 1
FIELD_MAX_LENGTH: int = 100

# errors messages
DESCRIPTION_ERROR: str = 'описание должно содержать минимум 1 символ'
EMPTY_REQUEST: str = 'Вы передаете пустой запрос!'
CANT_UPDATE_CLOSED_PROJECT: str = 'Закрытый проект нельзя редактировать!'
PROJECT_WAS_FUNDED: str = 'В проект были внесены средства, не подлежит удалению!'
PROJECT_NAME_OCCUPIED: str = 'Проект с таким именем уже существует!'
PROJECT_DOESNT_EXISTS: str = 'Такого проекта не существует.'
CANT_REDUCE_AMOUNT: str = 'Нельзя снижать сумму проекта ниже инвестированной!'
PASSWORD_VALIDATION_ERROR: str = 'Password should be at least 3 characters'

# table parameters:
TABLE_ROWS = 100
TABLE_COLUMNS = 10


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    superuser_email: Optional[EmailStr] = None
    superuser_password: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
