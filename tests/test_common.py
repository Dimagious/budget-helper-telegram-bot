import unittest
from unittest.mock import patch
import datetime
import constants
from utils.common import get_current_month_column, log_user_action, is_allowed_user

class TestMainFunctions(unittest.TestCase):
    @patch('utils.common.datetime')
    def test_get_current_month_column(self, mock_datetime):
        # Настраиваем фиктивную текущую дату
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 11, 1)
        mock_datetime.datetime.side_effect = datetime.datetime

        # Ожидаемый результат для ноября
        expected_column = constants.MONTH_TO_COLUMN[11]
        self.assertEqual(get_current_month_column(), expected_column)

    @patch('utils.common.datetime')
    def test_get_current_month_column_edge_case(self, mock_datetime):
        # Настраиваем фиктивную текущую дату для января
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)
        mock_datetime.datetime.side_effect = datetime.datetime

        # Ожидаемый результат для января
        expected_column = constants.MONTH_TO_COLUMN[1]
        self.assertEqual(get_current_month_column(), expected_column)

    @patch('logging.info')
    def test_log_user_action(self, mock_logging_info):
        # Проверяем логику логирования действия пользователя
        log_user_action("test_action", "test_user")
        mock_logging_info.assert_called_with("test_user выбрал команду test_action.")

        log_user_action("test_action", "test_user", "extra detail")
        mock_logging_info.assert_called_with(
            "test_user выбрал команду test_action. Detail: extra detail"
        )

    def test_is_allowed_user(self):
        # Проверяем проверку пользователя на доступ
        allowed_users = ["123", "456", "789"]
        self.assertTrue(is_allowed_user(123, allowed_users))
        self.assertFalse(is_allowed_user(111, allowed_users))

    def test_edge_cases_log_user_action(self):
        # Проверяем логирование с пустым `detail`
        with patch('logging.info') as mock_logging_info:
            log_user_action("action_name", "user_name", "")
            mock_logging_info.assert_called_with("user_name выбрал команду action_name.")

    def test_edge_cases_is_allowed_user(self):
        # Проверяем пустой список разрешенных пользователей
        self.assertFalse(is_allowed_user(123, []))

        # Проверяем с пустым user_id
        self.assertFalse(is_allowed_user("", ["123", "456"]))

if __name__ == '__main__':
    unittest.main()
