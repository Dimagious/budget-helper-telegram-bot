import gspread
import time
from gspread.exceptions import APIError
from google.oauth2.service_account import Credentials

class GoogleSheetsHelper:
    def __init__(self, service_account_info, spreadsheet_id, scopes):
        """Инициализация GoogleSheets"""
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        self.gc = gspread.authorize(creds)
        
        # Пытаемся открыть таблицу, пока не получится
        for _ in range(3):
            try:
                self.sheet = self.gc.open_by_key(spreadsheet_id).sheet1 
                break  # Если открыли таблицу, выходим из цикла
            except APIError as e:
                print(f"Error opening sheet: {e}")
                time.sleep(2) 

    def get_categories(self, cell_range):
        """Возвращает список категорий."""
        cells = self.sheet.range(cell_range)
        return [cell.value for cell in cells]

    def update_cell(self, row, col, value):
        """Обновляет значение ячейки"""
        self.sheet.update_cell(row, col, value)

    def get_cell_value(self, row, col):
        """Возвращает значение ячейки"""
        value = self.sheet.cell(row, col).value
        return value if value else "0"
