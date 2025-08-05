import os
import sys
import logging
import telegram
import requests
from dotenv import load_dotenv


def setup_logger():
    base_dir = os.path.dirname(__file__)
    log_filepath = os.path.join(base_dir, "app.log")
    logging.basicConfig(level=logging.INFO,
                        filename=log_filepath, filemode="a")


def main():
    load_dotenv()
    setup_logger()

    tg_token = os.getenv("API_TELEGRAM")
    if not tg_token:
        sys.exit("Нет ключа доступа к TG. Завершение программы!")

    dev_token = os.getenv("TOKEN_DEV")
    if not dev_token:
        sys.exit("Нет API от devman. Завершение программы!")

    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        sys.exit("Не указан chat_id. Завершение программы!")

    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {dev_token}"
    }
    params = {}

    bot = telegram.Bot(token=tg_token)

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

                text_message = f"Работа проверена {lesson_title}. \nОшибок нет! Можно приступать к следующему уроку! \n{lesson_url}"

                if is_negative:
                    text_message = f"Работа проверена {lesson_title}. \nВ работе нашлись ошибки. Нужно исправить! \n{lesson_url}"

                bot.send_message(chat_id, text=text_message)

        except requests.exceptions.ReadTimeout:
            logging.exception("Ошибка запроса")
        except requests.exceptions.ConnectionError:
            logging.exception("Ошибка подключения к интернету")
        except telegram.error.TelegramError:
            logging.exception("Ошибка отправки сообщения в бот")


if __name__ == "__main__":
    main()
