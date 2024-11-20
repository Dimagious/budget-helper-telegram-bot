import logging
import os
import json
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext,
)
from google.oauth2.service_account import Credentials
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
    filename='bot.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CATEGORY, SPENDING = range(2)

# Инициализация Google Sheets
service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
gs_helper = GoogleSheetsHelper(service_account_info, GOOGLE_SPREADSHEET_TOKEN, constants.SCOPES)

async def start(update: Update, context: CallbackContext) -> int:
    """Обработка команды /start."""
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    if str(user_id) not in ALLOWED_USERS:
        logging.info(f"Несанкционированный пользователь {user_name} попытался получить доступ.")
        await update.message.reply_text(constants.SORRY)
        return ConversationHandler.END

    log_user_action("start", user_id)
    categories = gs_helper.get_categories(constants.RANGE_FOR_CATEGORIES)
    keyboard = create_keyboard(categories)

    await update.message.reply_text(constants.WHAT_DID_YOU_SPEND, reply_markup=keyboard)
    return CATEGORY


async def set_category(update: Update, context: CallbackContext) -> int:
    """Обработка выбора категории."""
    user_id = update.message.from_user.id
    context.user_data['category'] = update.message.text
    log_user_action("set_category", user_id, context.user_data['category'])

    await update.message.reply_text(constants.HOW_MUCH_DID_YOU_SPEND, reply_markup=ReplyKeyboardRemove())
    return SPENDING


async def set_spending(update: Update, context: CallbackContext) -> int:
    """Обработка ввода суммы и обновление Google Sheets."""
    try:
        category = context.user_data['category']
        # Удаляем запятую или заменяем её на точку для корректной обработки
        spending_str = update.message.text.replace(',', '').strip()
        spending = float(spending_str)  # Преобразуем строку в число

        row_to_update = constants.CATEGORIES.get(category)
        col_to_update = get_current_month_column()

        existing_value_str = gs_helper.get_cell_value(row_to_update, col_to_update)
        existing_value = float(existing_value_str.replace(',', '') if existing_value_str else 0)
        updated_value = existing_value + spending

        gs_helper.update_cell(row_to_update, col_to_update, updated_value)
        user_name = update.message.from_user.username
        logging.info(f"{user_name} внёс значение в \"{category}\". Было: {existing_value}. Стало: {updated_value}")

        await update.message.reply_text(constants.SPENDING_ADDED.format(category, spending))
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
    user_id = update.message.from_user.id
    log_user_action("cancel", user_id)
    await update.message.reply_text(constants.CANCELLED, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORY: [MessageHandler(filters.Regex(constants.REGEX_FOR_CATEGORIES), set_category)],
            SPENDING: [MessageHandler(filters.Regex(constants.REGEX_FOR_SPENDING), set_spending)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("help", help)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
