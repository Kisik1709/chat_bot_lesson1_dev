# 🤖 Homework Notifier

Python-бот для автоматического уведомления в Telegram о результатах проверки домашних заданий на [Devman.org](https://dvmn.org/).

## 🚀 Возможности

- Получение статуса проверки домашней работы с Devman.
- Уведомление в Telegram о результатах (успешно / есть ошибки).
- Настройка через переменные окружения или аргументы командной строки.
- Поддержка логирования в файл `app.log`.

## 🔧 Установка

1. Склонируйте репозиторий или скопируйте файлы в свою директорию
2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корне проекта и добавьте в него свои ключи:

```bash
API_TELEGRAM=your_telegram_bot_token
TOKEN_DEV=your_devman_api_token
CHAT_ID=your_telegram_chat_id
```
Telegram API можно получить через [@BotFather](https://t.me/BotFather)
Узнать chat_id можно, отправив сообщение боту.

## ▶️ Использование

- Запуск с chat_id если указали в .env:

```bash
python homework_notifier.py
```

- Можно указать chat_id через аргумент:

```bash
python homework_notifier.py 123456789  # ваш chat_id
```


## 📦 Зависимости
- requests — HTTP-запросы.
- python-dotenv — загрузка переменных из .env.
- telegram — работа с Telegram Bot API.
- argparse — парсинг аргументов командной строки.
- logging — логирование.

## 🔗 Используемые API

- [Devman.org](https://dvmn.org/api/docs/)

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).


