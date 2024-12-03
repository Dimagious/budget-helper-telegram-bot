import datetime
import logging

import constants


def get_current_month_column() -> int:
    """Возвращает номер столбца, соответствующий текущему месяцу."""
    current_month = datetime.datetime.now().month
    return constants.MONTH_TO_COLUMN.get(current_month)


def log_user_action(action: str, user_name: str, detail: str = "") -> None:
    """Логирует действия пользователя для лучшей прослеживаемости."""
    log_message = f"{user_name} выбрал команду {action}."
    if detail:  # Проверяем, есть ли значение в detail
        log_message += f" Detail: {detail}"
    logging.info(log_message)


def is_allowed_user(user_id: int, allowed_users: list) -> bool:
    """Проверяет, разрешено ли пользователю взаимодействовать с ботом."""
    return str(user_id) in allowed_users
