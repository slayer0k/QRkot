from datetime import datetime
from typing import Dict, List

from aiogoogle import Aiogoogle

from app.core.config import TABLE_COLUMNS, TABLE_ROWS, settings

FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    now_datetime = datetime.now().strftime(FORMAT)
    service = await wrapper_service.discover('sheets', 'v4')
    spreadsheets_body = {
        'properties': {
            'title': f'Отчет на {now_datetime}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {
                        'rowCount': TABLE_ROWS,
                        'columnCount': TABLE_COLUMNS
                    }
                }
            }
        ]
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover('drive', 'v3')
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[Dict],
    wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', datetime.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [
            project['name'],
            project['time_diff'],
            project['description']
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
