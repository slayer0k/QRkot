from datetime import datetime

# table parameters:
DATETIME_FORMAT: str = '%Y/%m/%d %H:%M:%S'
TABLE_ROWS: int = 100
TABLE_COLUMNS: int = 3
TABLE_TITLE: str = f'Отчет на {datetime.now().strftime(DATETIME_FORMAT)}'
LOCALE: str = 'ru_RU'
SHEET_TYPE: str = 'GRID'
SHEET_ID: int = 0
SHEET_TITLE: str = 'Лист1'
TABLE_HEADER = [
    ['Отчет от', datetime.now().strftime(DATETIME_FORMAT)],
    ['Количество регистраций переговорок'],
    ['ID переговорки', 'Кол-во бронирований']
]
UPDATE_RANGE = 'R1C1:R100C3'
UPDATE_MAJOR_DIMENSION = 'ROWS'
