import logging
import datetime
import constants

def get_current_month_column() -> int:
    """Возвращает номер столбца, соответствующий текущему месяцу."""
    current_month = datetime.datetime.now().month
    return constants.MONTH_TO_COLUMN.get(current_month)

def log_user_action(action: str, user_id: int, detail: str = "") -> None:
    """Логирует действия пользователя для лучшей прослеживаемости."""
    logging.info(f"User {user_id} performed {action}. Detail: {detail}")


def is_allowed_user(user_id: int, allowed_users: list) -> bool:
    """Проверяет, разрешено ли пользователю взаимодействовать с ботом."""
    return str(user_id) in allowed_users
