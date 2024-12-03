import logging
import time

import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError


class GoogleSheetsHelper:
    """Класс для работы с Google Sheets."""

    def __init__(self, service_account_info, spreadsheet_id, scopes):
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.spreadsheet = self._open_spreadsheet(spreadsheet_id)

    def _open_spreadsheet(self, spreadsheet_id):
        """Открывает таблицу, с обработкой ошибок."""
        for attempt in range(3):
            try:
                return self.gc.open_by_key(spreadsheet_id)
            except APIError as e:
                logging.error(f"Ошибка при открытии таблицы: {e}")
                time.sleep(2)
        raise Exception("Не удалось открыть таблицу после 3 попыток.")

    def get_categories(self, sheet_name: str, cell_range: str) -> list:
        """Получить список категорий из таблицы."""
        worksheet = self.spreadsheet.worksheet(sheet_name)
        cells = worksheet.range(cell_range)
        return [cell.value for cell in cells if cell.value]

    def get_cell_value(self, row: int, col: int, sheet_name: str) -> float:
        """Получить значение ячейки по строке и столбцу."""
        worksheet = self.spreadsheet.worksheet(sheet_name)
        value = worksheet.cell(row, col).value
        return value if value else 0.0

    def update_cell(self, row: int, col: int, value: int, sheet_name: str):
        """Обновить значение ячейки."""
        worksheet = self.spreadsheet.worksheet(sheet_name)
        worksheet.update_cell(row, col, value)
