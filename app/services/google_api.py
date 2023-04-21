from typing import Dict, List

from aiogoogle import Aiogoogle

import app.services.table_constants as constants
from app.core.config import settings


def get_request_body():
    return dict(
        properties=dict(
            title=constants.TABLE_TITLE,
            locale=constants.LOCALE
        ),
        sheets=[
            dict(
                properties=dict(
                    sheetType=constants.SHEET_TYPE,
                    sheetId=constants.SHEET_ID,
                    title=constants.SHEET_TITLE,
                    gridProperties=dict(
                        rowCount=constants.TABLE_ROWS,
                        columnCount=constants.TABLE_COLUMNS
                    )
                )
            )
        ]
    )


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    service = await wrapper_service.discover('sheets', 'v4')
    spreadsheets_body = get_request_body()
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
    table_values = constants.TABLE_HEADER
    for project in projects:
        new_row = [
            project['name'],
            project['time_diff'],
            project['description']
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': constants.UPDATE_MAJOR_DIMENSION,
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=constants.UPDATE_RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
