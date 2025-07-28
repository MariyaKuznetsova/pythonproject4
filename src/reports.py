import json
from datetime import datetime, timedelta
from typing import Dict, List, Union, Any, Optional
import pandas as pd
from pandas import DataFrame
import os
import logging


logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
os.makedirs("../logs", exist_ok=True)
file_handler = logging.FileHandler("../logs/reports.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def log(filename=None):
    """Декоратор с параметрами внешняя функция, которая принимает аргументы для декоратора"""

    def decorator(func):
        """Декоратор функции который автоматически логирует начало и конец выполнения функции,
        а также ее результаты или возникшие ошибки, и выводит в файл"""

        def wrapper(*args, **kwargs):
            """Обертка функции"""
            try:
                """Выполняется если функция работает"""
                result = func(*args, **kwargs)
                logger.info(f"Получаем результат функции {'spending_by_category'}")
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        result_str = result.to_string()
                        logger.info(f"Результат функции: {'spending_by_category'} записывается в файл: {filename}")
                        file.write(result_str)
                return result
            except Exception as e:
                """Выполняется если функция выдает ошибку"""
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)

        return wrapper

    return decorator


def get_path(path_fo_file: str) -> DataFrame:
    """Функция принимает путь к Excel файлу и возвращает таблицу"""
    logger.info(f"Функция {'get_path'} принимает путь к Excel файлу и возвращает таблицу")
    df = pd.read_excel(path_fo_file, sheet_name='Отчет по операциям')
    return df


def get_date_optional(period_date_optional: str, date_format="%Y-%m-%d %H:%M:%S") -> [str, str]:
    """Функция принимает дату возвращает период за последние три месяца от вводимой даты"""
    logger.info(f"Функция {'get_date_optional'} принимает дату возвращает период за последние три месяца от вводимой даты")
    end_date = datetime.strptime(period_date_optional, date_format)
    start_date = end_date - timedelta(days=90)
    end_date_optional = end_date.strftime("%d.%m.%Y %H:%M:%S")
    start_date_optional = start_date.strftime("%d.%m.%Y %H:%M:%S")
    return start_date_optional, end_date_optional

@log(filename="mylog.txt")
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Функция принимает DataFrame, название категории и дату возвращает транзакции заданной категории за заданный период"""
    logger.debug(f"Выполняется функция которая принимает DataFrame, название категории и дату возвращает транзакции заданной категории за заданный период: {'spending_by_category'}")
    category_transactions = transactions.loc[transactions["Категория"] == category]
    datas = get_date_optional(date)
    start = datas[0]
    start_pd = pd.to_datetime(start, format='%d.%m.%Y %H:%M:%S')
    end = datas[1]
    end_pd = pd.to_datetime(end, format='%d.%m.%Y %H:%M:%S')
    filtered_category_transactions = category_transactions.loc[(pd.to_datetime(category_transactions['Дата операции'], dayfirst=True) >= start_pd) & (pd.to_datetime(category_transactions['Дата операции'], dayfirst=True) <= end_pd)]
    sorted_category_transactions = filtered_category_transactions.sort_values(by='Дата операции', ascending=True)
    return(sorted_category_transactions)





if __name__ == "__main__":
    transactions = get_path("../data/operations.xlsx")
    print("Введите категорию: ")
    category = str(input())
    data = str("2021-07-14 15:30:00")
    dates = get_date_optional(data)
    spend = spending_by_category(transactions, category, data)
