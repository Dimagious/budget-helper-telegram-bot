from telegram import ReplyKeyboardMarkup


def create_keyboard(categories: list, two_per_row: bool = False) -> ReplyKeyboardMarkup:
    """Создание клавиатуры для категорий."""
    if two_per_row:
        buttons = [categories[i : i + 2] for i in range(0, len(categories), 2)]
    else:
        buttons = [[category] for category in categories]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
