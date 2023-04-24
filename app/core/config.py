from datetime import datetime
from typing import Optional

from pydantic import BaseSettings, EmailStr

# field constants
USER_PASSWORD_MIN_LENGTH: int = 3
FIELD_MIN_LENGTH: int = 1
FIELD_MAX_LENGTH: int = 100

# fastapi errors messages
DESCRIPTION_ERROR: str = 'описание должно содержать минимум 1 символ'
EMPTY_REQUEST: str = 'Вы передаете пустой запрос!'
CANT_UPDATE_CLOSED_PROJECT: str = 'Закрытый проект нельзя редактировать!'
PROJECT_WAS_FUNDED: str = 'В проект были внесены средства, не подлежит удалению!'
PROJECT_NAME_OCCUPIED: str = 'Проект с таким именем уже существует!'
PROJECT_DOESNT_EXISTS: str = 'Такого проекта не существует.'
CANT_REDUCE_AMOUNT: str = 'Нельзя снижать сумму проекта ниже инвестированной!'
PASSWORD_VALIDATION_ERROR: str = 'Password should be at least 3 characters'
GOOGLE_API_DATA_TO_BIG: str = 'Данных слишком много'
GOOGLE_API_TO_MANY_COLUMNS_IN_ROW: str = 'Слишком много колонок в строке'

# GoogleApi spreadsheet initial data
DATETIME_FORMAT: str = '%Y/%m/%d %H:%M:%S'
INITIAL_SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет на {datetime}',
        locale='ru_RU'
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType='GRID',
                sheetId=0,
                title='Лист1',
                gridProperties=dict(
                    rowCount=100,
                    columnCount=3
                )
            )
        )
    ]
)
TABLE_HEADERS = [
    ['Отчет от', datetime.now().strftime(DATETIME_FORMAT)],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


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
