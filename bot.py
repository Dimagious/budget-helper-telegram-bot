import logging
import os
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters,)
import constants
from handlers import start, handle_category, add_income, add_expense, set_income_amount, set_expense_amount, help, cancel
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()]
)
logging.info("Бот запущен")


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
