Телеграм-бот для учета расходов, который позволяет записывать траты по категориям и автоматически обновлять данные в Google Sheets.


# Описание
Этот проект представляет собой Телеграм-бота, который позволяет пользователям записывать свои расходы, классифицировать их по категориям и автоматически обновлять таблицу Google Sheets с данными о расходах.
Бот использует API Google Sheets для взаимодействия с таблицами, а также предоставляет интерфейс через Телеграм для ввода данных. Код развёрнут на Heroku.

![Budget Helper Bot Demo](https://github.com/Dimagious/Dimagious.github.io/blob/master/budget-helper-bot-demo.gif?raw=true)

# Функции
- Поддержка нескольких пользователей (ограничение доступа по ID).
- Категоризация расходов с возможностью выбора из списка.
- Возможность записывать и обновлять сумму доходов и расходов в таблице Google Sheets.
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
SERVICE_ACCOUNT_JSON=your-json
GOOGLE_SPREADSHEET_TOKEN=your-google-spreadsheet-id
ALLOWED_USERS='telegram-user1','telegram-user2'
```

Замените значения на ваши собственные данные:
- `TELEGRAM_BOT_TOKEN`: Токен вашего Телеграм-бота, который можно получить у [BotFather](@BotFather).
- `SERVICE_ACCOUNT_JSON`: Путь к вашему файлу учетных данных для доступа к Google Sheets API. [Инструкция](https://codd-wd.ru/instrukciya-po-polucheniyu-klyucha-servisnogo-akkaunta-google-dlya-raboty-s-sheets-api/).
- `GOOGLE_SPREADSHEET_TOKEN`: ID вашей таблицы Google Sheets, в которой будут храниться данные о расходах. Найти его можно в ссылке вашего документа:
```
https://docs.google.com/spreadsheets/d/GOOGLE_SPREADSHEET_TOKEN/edit
```
- `ALLOWED_USERS`: ID пользователей, которым разрешен доступ к боту.

## Развёртывание на Heroku
### 1. Установите Heroku CLI
Heroku CLI нужен для управления приложением из терминала.
1. Зайдите на [страницу скачивания Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
2. Установите CLI для вашей операционной системы.
3. После установки откройте терминал и выполните команду:
```bash
heroku login
```   
Это откроет браузер для авторизации в вашем Heroku-аккаунте.
### 2. Инициализация репозитория Heroku
Перейдите в директорию с вашим проектом и выполните команды для инициализации проекта на Heroku:
```bash
heroku create
```
Это создаст новое приложение на Heroku и подключит его к вашему локальному репозиторию.
### 3. Настройка переменных окружения на Heroku
Добавьте все необходимые переменные окружения в настройках вашего приложения на Heroku:
- Перейдите на панель управления вашим приложением на Heroku.
- Откройте вкладку Settings.
- Нажмите на Config Vars и добавьте следующие переменные:
```bash
TELEGRAM_BOT_TOKEN
SERVICE_ACCOUNT_JSON
GOOGLE_SPREADSHEET_TOKEN
ALLOWED_USERS
```
Значения подставьте свои

# Структура проекта
`bot.py`: Основной файл или точка входа
`handler.py`: Модуль для взаимодействия с функциями-обработчиками бота
`google_api.py`: Модуль для взаимодействия с Google Sheets API.
`keyboard.py`: Модуль для создания клавиатуры Telegram.
`constants.py`: Файл с константами и регулярными выражениями для работы с категориями и расходами.
`common.py`: Файл для вспомогательных функций
`.env`: Файл с переменными окружения.
`requirements.txt`: Список зависимостей Python.

# Использование
После запуска бота в Telegram:
1. Напишите команду /start, чтобы начать.
2. Выберите операцию: Внести доход или Внести расход
3. Выберите категорию расхода или дохода из предложенного списка.
4. Введите сумму, которую вы потратили.
5. Бот автоматически обновит таблицу Google Sheets с вашими данными.