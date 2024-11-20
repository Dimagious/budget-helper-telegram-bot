import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsHelper:
    def __init__(self, service_account_file, spreadsheet_id, scopes):
        creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.sheet = self.gc.open_by_key(spreadsheet_id).sheet1

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
