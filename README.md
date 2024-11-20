Телеграм-бот для учета расходов, который позволяет записывать траты по категориям и автоматически обновлять данные в Google Sheets.
# Описание 
Этот проект представляет собой Телеграм-бота, который позволяет пользователям записывать свои расходы, классифицировать их по категориям и автоматически обновлять таблицу Google Sheets с данными о расходах.

Бот использует API Google Sheets для взаимодействия с таблицами, а также предоставляет интерфейс через Телеграм для ввода данных. 

# Функции 
- Поддержка нескольких пользователей (ограничение доступа по ID).
- Категоризация расходов с возможностью выбора из списка.
- Возможность записывать и обновлять сумму расходов в таблице Google Sheets.
- Простота в использовании через Telegram.
- Автоматическое обновление данных в Google Sheets по месяцам.
# Установка и настройка 
## 1. Клонировать репозиторий
```bash
git clone https://github.com/yourusername/telegram-budget-helper-bot.git
cd telegram-budget-helper-bot
```
## 2. Установить зависимости
Для установки зависимостей используйте pip:
```bash
pip install -r requirements.txt
```
## 3. Настроить переменные окружения
Создайте файл .env в корне проекта и добавьте следующие переменные:
```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
SERVICE_ACCOUNT_FILE=path/to/your/service-account-file.json
GOOGLE_SPREADSHEET_TOKEN=your-google-spreadsheet-id
ALLOWED_USERS='telegram-user1','telegram-user2'
```
Замените значения на ваши собственные данные:
`TELEGRAM_BOT_TOKEN`: Токен вашего Телеграм-бота, который можно получить у BotFather.
`SERVICE_ACCOUNT_FILE`: Путь к вашему файлу учетных данных для доступа к Google Sheets API.
`GOOGLE_SPREADSHEET_TOKEN`: ID вашей таблицы Google Sheets, в которой будут храниться данные о расходах.
`ALLOWED_USERS`: ID пользователей, которым разрешен доступ к боту.

## 4. Запуск
После настройки переменных окружения, вы можете запустить бота с помощью следующей команды:
```bash
python bot.py
```
Бот будет работать в режиме polling, отвечая на команды и сообщения.
# Структура проекта

`bot.py`: Основной файл, содержащий логику работы с Telegram API и Google Sheets API.
`google_api.py`: Модуль для взаимодействия с Google Sheets API.
`keyboard.py`: Модуль для создания клавиатуры Telegram.
`constants.py`: Файл с константами и регулярными выражениями для работы с категориями и расходами.
`common.py`: Файл для вспомогательных функций
`.env`: Файл с переменными окружения.
`requirements.txt`: Список зависимостей Python.

# Использование
После запуска бота в Telegram:
1. Напишите команду /start, чтобы начать.
2. Выберите категорию расхода из предложенного списка.
3. Введите сумму, которую вы потратили.
4. Бот автоматически обновит таблицу Google Sheets с вашими данными.

# Логирование
Все действия пользователей и ошибки бота логируются в файл bot.log. Это поможет отслеживать проблемы и анализировать действия пользователей.
