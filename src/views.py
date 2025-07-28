import json
from locale import currency
from typing import Dict, Any
from src.utils import (
    get_time_for_greeting,
    get_date_time,
    get_path_and_period,
    get_card_with_spend,
    get_top_transactions,
    get_currency,
    get_stock
)
import logging
import os

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
os.makedirs("../logs", exist_ok=True)
file_handler = logging.FileHandler("../logs/views.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

logger.debug(f"Выполняется функция, принимающую на вход строку с датой и временем и возвращающую JSON-ответ: {'main_info'}")

def main_info(date_time: str) -> Dict[str, Any]:
    """Функцию, принимающую на вход строку с датой и временем в формате
YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ"""
    logger.info(f"Выполняется срез по нужному диапазону: {date_time}")
    # Срез по нужному диапазону.
    time_period = get_date_time(date_time)
    sorted_df = get_path_and_period("../data/operations.xlsx", time_period)
    logger.debug(f"Выполнился срез по нужному диапазону: {time_period}")

    # 1. Приветствие
    greeting = get_time_for_greeting()
    logger.debug(f"Приложение приветствует пользователя в зависимости от времени суток: {greeting}")
    # 2. По каждой карте
    cards = get_card_with_spend(sorted_df)
    logger.debug(f"Приложение выводит данные на введенную дату по картам: {cards}")
    # 3. Топ-5 транзакций по сумме платежа
    top_five_transactions = get_top_transactions(sorted_df, 5)
    logger.debug(f"Приложение показывает топ-5 транзакций по сумме платежа: {top_five_transactions}")
    # 4. Курс валют
    currency_rates = get_currency("../data/user_settings.json")
    logger.debug(f"Приложение показывает курс валют на сегодняшнюю дату: {top_five_transactions}")
    # 5. Стоимость акций из S&P500
    stock_prices = get_stock("../data/user_settings.json")
    logger.debug(f"Приложение показывает стоимость акций из S&P500 на сегодняшнюю дату: {stock_prices}")

    data = {"greeting": greeting, "cards": cards, "top_transactions": top_five_transactions, "currency_rates": currency_rates, "stock_prices": stock_prices}

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    logger.debug("Приложение выводит результат в виде JSON-ответа")
    return json_data


if __name__ == "__main__":
    date_time = "2021-06-14 15:30:00"
    print(main_info(date_time))