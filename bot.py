import logging
import os
import json
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext,
)
from utils.google_api import GoogleSheetsHelper
from utils.keyboard import create_keyboard
import constants
from utils.common import log_user_action, is_allowed_user, get_current_month_column

from dotenv import load_dotenv
load_dotenv()

# Загрузка переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")
GOOGLE_SPREADSHEET_TOKEN = os.getenv("GOOGLE_SPREADSHEET_TOKEN")
ALLOWED_USERS = [user.strip("'") for user in os.getenv("ALLOWED_USERS").split(",")]

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()]
)
logging.info("Бот запущен")

# Инициализация Google Sheets
service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
gs_helper = GoogleSheetsHelper(service_account_info, GOOGLE_SPREADSHEET_TOKEN, constants.SCOPES)


async def start(update: Update, context: CallbackContext) -> int:
    """Обработка команды /start."""
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    if not is_allowed_user(user_id, ALLOWED_USERS):
        logging.info(f"Несанкционированный пользователь {user_name} попытался получить доступ.")
        await update.message.reply_text(constants.SORRY)
        return ConversationHandler.END

    log_user_action("start", user_name)
    keyboard = create_keyboard([constants.ADD_INCOME, constants.ADD_EXPENSE])
    await update.message.reply_text(constants.CHOOSE_OPERATION, reply_markup=keyboard)
    return constants.CHOOSE_CATEGORY


async def handle_category(update: Update, context: CallbackContext) -> int:
    """Обработка выбора действия: доход или расход."""
    choice = update.message.text
    context.user_data['choice'] = choice

    if choice == constants.ADD_INCOME:
        # Клавиатура для категорий доходов
        income_categories = gs_helper.get_categories(constants.INCOME_SHEET_NAME, constants.RANGE_FOR_INCOME_CATEGORIES)
        keyboard = create_keyboard(income_categories, True)
        await update.message.reply_text("Выбери категорию дохода:", reply_markup=keyboard)
        return constants.SET_INCOME_CATEGORY
    elif choice == constants.ADD_EXPENSE:
        # Клавиатура для категорий расходов
        expense_categories = gs_helper.get_categories(constants.EXPENSE_SHEET_NAME, constants.RANGE_FOR_EXPENSE_CATEGORIES)
        keyboard = create_keyboard(expense_categories, True)
        await update.message.reply_text("Выбери категорию расхода:", reply_markup=keyboard)
        return constants.SET_EXPENSE_CATEGORY
    else:
        await update.message.reply_text("Пожалуйста, выберите один из вариантов.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def add_income(update: Update, context: CallbackContext) -> None:
    """Обработка команды 'Внести доход': выбор категории."""
    log_user_action("add_income", update.message.from_user.username)
    
    # Получение категорий доходов
    categories = gs_helper.get_categories(constants.INCOME_SHEET_NAME, constants.RANGE_FOR_INCOME_CATEGORIES)
    keyboard = create_keyboard(categories, True)
    
    context.user_data['categories'] = categories
    
    chosen_category = update.message.text
    if chosen_category in categories:
        context.user_data['category'] = chosen_category
        await update.message.reply_text(constants.HOW_MUCH_DO_YOU_GET, reply_markup=ReplyKeyboardRemove())
        return constants.SET_INCOME_AMOUNT
    else:
        await update.message.reply_text(constants.CHOOSE_CATEGORY)
        return constants.SET_INCOME_CATEGORY
    

async def add_expense(update: Update, context: CallbackContext) -> int:
    """Обработка команды 'Внести расход': выбор категории."""
    log_user_action("add_expense", update.message.from_user.username)

    # Получение категорий расходов
    categories = gs_helper.get_categories(constants.EXPENSE_SHEET_NAME, constants.RANGE_FOR_EXPENSE_CATEGORIES)
    keyboard = create_keyboard(categories, True)

    context.user_data['categories'] = categories

    chosen_category = update.message.text
    if chosen_category in categories:
        context.user_data['category'] = chosen_category
        await update.message.reply_text(constants.HOW_MUCH_DID_YOU_SPEND, reply_markup=ReplyKeyboardRemove())
        return constants.SET_EXPENSE_AMOUNT
    else:
        await update.message.reply_text(constants.CHOOSE_CATEGORY)
        return constants.SET_EXPENSE_CATEGORY


async def set_expense_amount(update: Update, context: CallbackContext) -> int:
    """Обработка ввода суммы и обновление Google Sheets."""
    try:
        # Извлекаем категорию из user_data
        category = context.user_data.get('category')
        if not category:
            await update.message.reply_text(constants.CHOOSE_CATEGORY)
            return constants.SET_EXPENSE_CATEGORY

        # Удаляем запятую или заменяем её на точку для корректной обработки
        expense_str = update.message.text.replace(',', '').strip()
        if not expense_str.isdigit():
            await update.message.reply_text(constants.WRONG_AMOUNT)
            return constants.SET_EXPENSE_AMOUNT

        expense = float(expense_str)  # Преобразуем строку в число

        row_to_update = constants.EXPENSE_CATEGORIES.get(category)
        col_to_update = get_current_month_column()

        existing_value_str = gs_helper.get_cell_value(row_to_update, col_to_update, constants.EXPENSE_SHEET_NAME)
        existing_value = float(existing_value_str.replace(',', '') if existing_value_str else 0)
        updated_value = existing_value + expense

        gs_helper.update_cell(row_to_update, col_to_update, updated_value, constants.EXPENSE_SHEET_NAME)
        user_name = update.message.from_user.username
        logging.info(f"{user_name} внёс расход {expense} в \"{category}\". Было: {existing_value}. Стало: {updated_value}")

        await update.message.reply_text(constants.EXPENSE_ADDED.format(category, expense))
    except (ValueError, AttributeError) as e:
        logging.error(f"Ошибка обновления: {e}")
        await update.message.reply_text(constants.ERROR_PROCESSING)
    return ConversationHandler.END


async def set_income_amount(update: Update, context: CallbackContext) -> int:
    """Обработка ввода суммы и обновление Google Sheets."""
    try:
        # Извлекаем категорию из user_data
        category = context.user_data.get('category')
        if not category:
            await update.message.reply_text(constants.CHOOSE_CATEGORY)
            return constants.SET_INCOME_CATEGORY
        
        # Удаляем запятую или заменяем её на точку для корректной обработки
        income_str = update.message.text.replace(',', '').strip()
        if not income_str.isdigit():
            await update.message.reply_text(constants.WRONG_AMOUNT)
            return constants.SET_INCOME_AMOUNT
        
        income = float(income_str)  # Преобразуем строку в число
        
        row_to_update = constants.INCOME_CATEGORIES.get(category)
        col_to_update = get_current_month_column()
        
        existing_value_str = gs_helper.get_cell_value(row_to_update, col_to_update, constants.INCOME_SHEET_NAME)
        existing_value = float(existing_value_str.replace(',', '') if existing_value_str else 0)
        updated_value = existing_value + income
        
        gs_helper.update_cell(row_to_update, col_to_update, updated_value, constants.INCOME_SHEET_NAME)
        user_name = update.message.from_user.username
        logging.info(f"{user_name} внёс доход {income} в \"{category}\". Было: {existing_value}. Стало: {updated_value}")
        
        await update.message.reply_text(constants.INCOME_ADDED.format(category, income))
    except (ValueError, AttributeError) as e:
        logging.error(f"Ошибка обновления: {e}")
        await update.message.reply_text(constants.ERROR_PROCESSING)
    return ConversationHandler.END


async def help(update: Update, context: CallbackContext) -> None:
    """Обработка команды /help."""
    help_text = constants.HELP_TEXT
    await update.message.reply_text(help_text)


async def cancel(update: Update, context: CallbackContext) -> int:
    """Обработка команды /cancel."""
    user_name = update.message.from_user.username
    log_user_action("cancel", user_name)
    await update.message.reply_text(constants.CANCELLED, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("help", help))  # Обрабатывает /help в любое время
    application.add_handler(CommandHandler("cancel", cancel))  # Отдельный обработчик для /cancel

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            constants.CHOOSE_CATEGORY: [MessageHandler(filters.Text([constants.ADD_INCOME, constants.ADD_EXPENSE]), handle_category),],
            constants.SET_INCOME_CATEGORY: [MessageHandler(filters.ALL, add_income)],
            constants.SET_EXPENSE_CATEGORY: [MessageHandler(filters.ALL, add_expense)],
            constants.SET_INCOME_AMOUNT: [MessageHandler(filters.Regex(constants.REGEX_FOR_AMOUNT), set_income_amount)],
            constants.SET_EXPENSE_AMOUNT: [MessageHandler(filters.Regex(constants.REGEX_FOR_AMOUNT), set_expense_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],  # Обработчик для команды /cancel во время диалога
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
