# Регулярные выражения
REGEX_FOR_AMOUNT = r"^[1-9]\d*(\.\d+)?$"

# Общие сообщения бота
SORRY = "У вас нет прав для работы с ботом."
CHOOSE_CATEGORY = "Выбери категорию."
ERROR_PROCESSING = "Ошибка обработки. Попробуй снова."
CANCELLED = "Ок. Позови меня, когда захочешь записать доход/расход."
WRONG_AMOUNT = "Введено не числовое значение. Попробуй ещё раз вписать сумму:"
HELP_TEXT = (
    "Доступные команды:\n"
    "/start - Вызвать бота и записать расход\n"
    "/cancel - Отменить текущую операцию или ввод данных\n"
    "/help - Получить список доступных команд."
)

# Состояния для управления диалогом
CHOOSE_CATEGORY, SET_EXPENSE_CATEGORY, SET_EXPENSE_AMOUNT, SET_INCOME_CATEGORY, SET_INCOME_AMOUNT = range(5)

# Сообщения бота по сценарию "Внести доход"
ADD_INCOME = "Внести доход"
WHERE_DO_YOU_GET_MONEY = "Куда внести доход?"
HOW_MUCH_DO_YOU_GET = "Сколько было получено? Впиши сумму:"
INCOME_ADDED = 'Записал в категорию "{}": {}'
INCOME_SHEET_NAME = "Доходы"

# Сообщения бота по сценарию "Внести расход"
ADD_EXPENSE = "Внести расход"
CHOOSE_OPERATION = "Какую операцию ты хочешь совершить?"
HOW_MUCH_DID_YOU_SPEND = "Сколько было потрачено? Впиши сумму:"
EXPENSE_ADDED = 'Записал в категорию "{}": {}'
EXPENSE_SHEET_NAME = "Расходы"

# Диапазоны для работы с Google Sheets
RANGE_FOR_EXPENSE_CATEGORIES = "A2:A15"
RANGE_FOR_INCOME_CATEGORIES = "A3:A7"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

# Маппинг месяцев на столбцы Google Sheets
MONTH_TO_COLUMN = {
    1: 2,   # Январь -> Столбец B (2)
    2: 3,   # Февраль -> Столбец C (3)
    3: 4,   # Март -> Столбец D (4)
    4: 5,   # Апрель -> Столбец E (5)
    5: 6,   # Май -> Столбец F (6)
    6: 7,   # Июнь -> Столбец G (7)
    7: 8,   # Июль -> Столбец H (8)
    8: 9,   # Август -> Столбец I (9)
    9: 10,  # Сентябрь -> Столбец J (10)
    10: 11, # Октябрь -> Столбец K (11)
    11: 12, # Ноябрь -> Столбец L (12)
    12: 13, # Декабрь -> Столбец M (13)
}

# Логирование действий пользователей
USER_ACTION_LOG = "Пользователь {user_name} выполнил действие: {action}."
