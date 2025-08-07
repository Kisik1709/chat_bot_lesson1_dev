import os
import sys
import time
import logging
import telegram
import requests
from dotenv import load_dotenv


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)

        self.bot.send_message(self.chat_id, log_entry)


def setup_logger(bot, chat_id):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(TelegramLogHandler(bot, chat_id))


def main():
    load_dotenv()

    tg_token = os.getenv("API_TELEGRAM")
    if not tg_token:
        sys.exit("Нет ключа доступа к TG. Завершение программы!")

    dev_token = os.getenv("TOKEN_DEV")
    if not dev_token:
        sys.exit("Нет API от devman. Завершение программы!")

    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        sys.exit("Не указан chat_id. Завершение программы!")

    bot = telegram.Bot(token=tg_token)
    setup_logger(bot, chat_id)
    logging.info("BOT STARTED")

    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {dev_token}"
    }
    params = {}

    while True:
        try:
            response = requests.get(
                url, headers=headers, params=params)
            response.raise_for_status()
            review_result = response.json()

            timestamp_to_request = review_result.get("timestamp_to_request")
            params["timestamp"] = timestamp_to_request

            if review_result["status"] == "found":
                lesson_title = review_result["new_attempts"][0]["lesson_title"]
                is_negative = review_result["new_attempts"][0]["is_negative"]
                lesson_url = review_result["new_attempts"][0]["lesson_url"]

                text_message = f"Работа проверена работа по уроку: '{lesson_title}'. \nОшибок нет! Можно приступать к следующему уроку! \n{lesson_url}"

                if is_negative:
                    text_message = f"Работа проверена по уроку: '{lesson_title}'. \nВ работе нашлись ошибки. Нужно исправить! \n{lesson_url}"

                bot.send_message(chat_id, text=text_message)

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logging.exception(
                "Ошибка подключения к интернету. Повтор через 5 минут.")
            time.sleep(300)
        except telegram.error.TelegramError:
            logging.exception(
                "Ошибка отправки сообщения в бот.")


if __name__ == "__main__":
    main()
