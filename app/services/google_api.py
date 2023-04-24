from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Tuple

from aiogoogle import Aiogoogle

import app.core.config as conf
from app.error_handlers.google_api_exceptions import (
    SpreadsheetException, update_exceptions_handler)


def get_json(
    title: str = None,
    locale: str = None,
    sheet_type: str = None,
    sheet_id: int = None,
    sheet_title: str = None,
    grid_rows: int = None,
    grid_columns: int = None,
) -> Dict:
    spreadsheet_body = deepcopy(conf.INITIAL_SPREADSHEET_BODY)
    properties = spreadsheet_body['properties']
    if title:
        properties['title'] = title
    else:
        properties['title'] = properties['title'].format(
            datetime=datetime.now().strftime(conf.DATETIME_FORMAT)
        )
    if locale:
        properties['locale'] = locale
    sheet_properties = spreadsheet_body['sheets'][0]['properties']
    if sheet_type:
        sheet_properties['sheetType'] = sheet_type
    if sheet_id:
        sheet_properties['sheetId'] = sheet_id
    if sheet_title:
        sheet_properties['title'] = sheet_title
    grid_properties = sheet_properties['gridProperties']
    if grid_rows:
        grid_properties['rowCount'] = grid_rows
    if grid_columns:
        grid_properties['columnCount'] = grid_columns
    return spreadsheet_body


async def spreadsheets_create(
        wrapper_service: Aiogoogle
) -> Tuple[str, Dict]:
    service = await wrapper_service.discover('sheets', 'v4')
    spreadsheets_body = get_json()
    try:
        response = await wrapper_service.as_service_account(
            service.spreadsheets.create(json=spreadsheets_body)
        )
    except Exception as error:
        raise SpreadsheetException(
            conf.TABLE_CREATE_ERROR.format(error=error)
        )
    sheet_properties = spreadsheets_body['sheets'][0]['properties']
    return (response['spreadsheetId'], dict(
        rows=sheet_properties['gridProperties']['rowCount'],
        columns=sheet_properties['gridProperties']['columnCount'],
    ))


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': conf.settings.email
    }
    service = await wrapper_service.discover('drive', 'v3')
    try:
        await wrapper_service.as_service_account(
            service.permissions.create(
                fileId=spreadsheet_id,
                json=permissions_body,
                fields='id'
            )
        )
    except Exception as error:
        raise SpreadsheetException(
            conf.PERMISSIONS_ERROR.format(error=error)
        )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[Dict],
    grid: Dict,
    wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('sheets', 'v4')
    max_headers_len = max(map(len, conf.TABLE_HEADERS))
    if max_headers_len > grid['columns']:
        await update_exceptions_handler(
            conf.HEADERS_FAULT.format(
                headers_len=max_headers_len, columns=grid['columns']
            ),
            spreadsheet_id,
            wrapper_service
        )
    if len(projects[0]) > grid['columns']:
        await update_exceptions_handler(
            conf.TO_MANY_FIELDS_IN_PROJECT.format(
                columns=grid['columns'], fields=len(projects[0])
            ),
            spreadsheet_id, wrapper_service
        )
    table_values = conf.TABLE_HEADERS
    for project in projects:
        new_row = [
            project['name'],
            project['time_diff'],
            project['description']
        ]
        table_values.append(new_row)
    if len(table_values) > grid['rows']:
        await update_exceptions_handler(
            conf.TO_MANY_OBJECTS_IN_RESPONSE.format(
                values=len(table_values), rows=grid['rows']
            ),
            spreadsheet_id, wrapper_service
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    try:
        await wrapper_service.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range=f'R1C1:R{len(table_values)}C{grid["columns"]}',
                valueInputOption='USER_ENTERED',
                json=update_body
            )
        )
    except Exception as error:
        raise SpreadsheetException(
            conf.UPDATE_UNDESCRIBED_ERROR.format(error=error)
        )
