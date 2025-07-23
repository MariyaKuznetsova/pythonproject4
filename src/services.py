import re
from typing import Dict, Union, List
import pandas as pd


def excel_func(excel_file: Union[str]) -> List[Dict]:
    """Функция для считывания финансовых операций из Excel"""
    try:
        excel_trans = pd.read_excel(excel_file)
        dictionary = excel_trans.to_dict("records")
        return dictionary
    except Exception:
        return []


def simple_search(data: list[dict], search: str) -> list[dict]:
    """Функция для поиска в списке словарей операций по заданной строке"""
    dict_new = []
    pattern = search
    try:
        for operation in data:
            if re.search(pattern, str(operation["Описание"]), flags=re.IGNORECASE):
                dict_new.append(operation)
            elif re.search(pattern, str(operation["Категория"]), flags=re.IGNORECASE):
                dict_new.append(operation)
            else:
                continue

        return dict_new
    except Exception:
        return []




