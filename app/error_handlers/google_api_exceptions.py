from aiogoogle import Aiogoogle


class SpreadsheetException(Exception):
    pass


async def update_exceptions_handler(
    message: str,
    spreadsheet_id: int,
    wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('drive', 'v3')
    await wrapper_service.as_service_account(
        service.files.delete(fileId=spreadsheet_id)
    )
    raise SpreadsheetException(message)
