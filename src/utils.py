import json
from datetime import datetime
from typing import Dict, List, Union, Any
import pandas as pd
from pandas import DataFrame
import os

import requests
from dotenv import load_dotenv
# from dadata import Dadata

load_dotenv("../.env")
"""Читаем API ключ из окружения"""
API_KEY = os.getenv("API_KEY")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")



def get_time_for_greeting():
   """
     Функция возвращает приветствие
     в зависимости от текущего времени
   """
   user_datetime = datetime.now()
   hour = user_datetime.hour
   if 5 <= hour < 12:
     return "Доброе утро"
   elif  12 <= hour < 18:
     return "Добрый день"
   elif  18 <= hour < 23:
     return "Добрый вечер"
   else:
     return "Доброй ночи"


def get_date_time(date_time, date_format="%Y-%m-%d %H:%M:%S"):
    """Функция преобразования формат даты"""
    end_date = datetime.strptime(date_time, date_format)
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
    return [
        start_date.strftime("%d.%m.%Y %H:%M:%S"),
        end_date.strftime("%d.%m.%Y %H:%M:%S")
    ]


def get_path_and_period(path_fo_file: str, period_date: List) -> DataFrame:
    """Функция принимает путь к Excel файлу и список дат и возвращает таблицу в данном периоде"""
    df = pd.read_excel(path_fo_file, sheet_name='Отчет по операциям')

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
    sorted_df = filtered_df.sort_values(by='Дата операции', ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> List[dict]:
    """Функция принимает DataFrame и возвращает список карт с расходами"""
    card_spend_transactions = []
    card_sorted = sorted_df[["Номер карты", "Сумма операции", "Кэшбэк", "Сумма операции с округлением"]]

    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            cashback = total_spent // 100
            row = {"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback}
            card_spend_transactions.append(row)
    return card_spend_transactions


def get_top_transactions(sorted_df: DataFrame, get_top):
    """Функция принимает DataFrame и возвращает список get_top топ-транзакций по сумме платежа"""
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by='Сумма операции', ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[["Дата платежа", "Сумма операции", "Категория", "Описание"]]
    for index, row in top_transactions_sorted.iterrows():
        date = row["Дата платежа"]
        amount = row["Сумма операции"]
        category = row["Категория"]
        description = row["Описание"]
        transaction = {"date": date, "amount": amount, "category": category, "description": description}
        top_pay_transactions.append(transaction)
    return top_pay_transactions


def get_currency(path_to_json: str) -> List[dict]:
    """Функция, которая принимает на вход JSON-файл и возвращает список словарей с данными
    о курсах валют"""

    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        currences = data['user_currencies']

        currency_rates = []

        for currence in currences:
            url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"
            response = requests.get(url)
            repos = response.json()
            answer = repos.get("rates")
            answer_rub = round(answer.get("RUB"), 2)

            if currence == "USD":
                all_answers = answer_rub
            else:
                answer_currence = answer.get(currence)
                answer_usd = 1 / answer_currence
                answer_need = round((answer_usd * answer_rub), 2)
                all_answers = answer_need

            currency_rates.append({"currency": f'{currence}', "rate": f'{all_answers}'})
        return currency_rates


# print(get_currency("../data/user_settings.json"))

def get_stock(path_to_json: str) -> List[dict]:
    """Функция, которая принимает на вход JSON-файл и возвращает список словарей с данными
        о стоимости валют"""

    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        stocks = data['user_stocks']

        stock_rates = []

        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol={stock}&apikey={API_KEY_STOCK}"
            response = requests.get(url)
            repos = response.json()
            print(repos)
            dicts_repos = repos['data']
            print(dicts_repos)
            for dicts in dicts_repos:
                stock_symbol = dicts['symbol']
                stock_close = dicts['close']
                stock_need = {"stock": f"{stock_symbol}", "price": f"{stock_close}"}
            stock_rates.append(stock_need)
        print(stock_rates)
# {
#       "stock": f"{stock}",
#       "price": 1007.08
#     }
print(get_stock("../data/user_settings.json"))
# {'Дата операции': '03.01.2018 15:03:35',
#  'Дата платежа': '04.01.2018',
#  'Номер карты': '*7197',
#  'Статус': 'OK',
#  'Сумма операции': -73.06,
#  'Валюта операции': 'RUB',
#  'Сумма платежа': -73.06,
#  'Валюта платежа': 'RUB',
#  'Кэшбэк': nan,
#  'Категория': 'Супермаркеты',
#  'MCC': 5499.0,
#  'Описание': 'Magazin 25',
#  'Бонусы (включая кэшбэк)': 1,
#  'Округление на инвесткопилку': 0,
#  'Сумма операции с округлением': 73.06}