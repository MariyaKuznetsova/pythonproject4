import re
from typing import Dict, Union, List
import pandas as pd
import logging
import os

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
os.makedirs("../logs", exist_ok=True)
file_handler = logging.FileHandler("../logs/services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

logger.debug(f"Выполняется функция поиска операций: {'simple_search'}")

def excel_func(excel_file: Union[str]) -> List[Dict]:
    """Функция для считывания финансовых операций из Excel"""
    try:
        logger.info(f"Выполняется считывания финансовых операций из Excel: {excel_file}")
        excel_trans = pd.read_excel(excel_file)
        dictionary = excel_trans.to_dict("records")
        logger.debug(f"Произведено считывания финансовых операций из Excel в словарь: {dictionary}")
        return dictionary
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return []


def simple_search(data: list[dict], search: str) -> list[dict]:
    """Функция для поиска в списке словарей операций по заданной строке"""
    dict_new = []
    pattern = search
    try:
        logger.info(f"Выполняется поиск в списке словарей операций по заданной строке: {pattern}")
        for operation in data:
            if re.search(pattern, str(operation["Описание"]), flags=re.IGNORECASE):
                logger.debug(f"Выполнился поиск в списке словарей операций по заданной строке: {pattern} в столбце Описание")
                dict_new.append(operation)
            elif re.search(pattern, str(operation["Категория"]), flags=re.IGNORECASE):
                logger.debug(f"Выполнился поиск в списке словарей операций по заданной строке: {pattern} в столбце Категория")
                dict_new.append(operation)
            else:
                continue
        logger.info(f"Выводится список операций {dict_new} по заданным параметрам поиска")
        return dict_new
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return []


if __name__ == "__main__":
    datas = excel_func("../data/operations.xlsx")
    print("Введите данные поиска:")
    search_s = input()
    answer = simple_search(datas, search_s)
    print(answer)



