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


def main_info(date_time: str) -> Dict[str, Any]:
    """Функцию, принимающую на вход строку с датой и временем в формате
YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ"""

    # Срез по нужному диапазону.
    time_period = get_date_time(date_time)
    sorted_df = get_path_and_period("../data/operations.xlsx", time_period)

    # 1. Приветствие
    greeting = get_time_for_greeting()

    # 2. По каждой карте
    cards = get_card_with_spend(sorted_df)

    # 3. Топ-5 транзакций по сумме платежа
    top_five_transactions = get_top_transactions(sorted_df, 5)

    # 4. Курс валют
    currency_rates = get_currency("../data/user_settings.json")

    # 5. Стоимость акций из S&P500
    stock_prices = get_stock("../data/user_settings.json")


    data = {"greeting": greeting, "cards": cards, "top_transactions": top_five_transactions, "currency_rates": currency_rates, "stock_prices": stock_prices}

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data


