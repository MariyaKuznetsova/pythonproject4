import re
import json
from typing import Dict, Any, Union, List
import pandas as pd

def simple_search(data: list[dict], search: str) -> list[dict]:
    """Функция для поиска в списке словарей операций по заданной строке"""
    dict_new = []
    pattern = search
    try:
        for operation in data:
            print(operation) # выдает все транзакции
            if re.search(pattern, operation["Описание"], flags=re.IGNORECASE):
                print(operation) # выдает пустой список
                dict_new.append(operation)
                print(operation)
            else:
                continue
        return dict_new
    except Exception:
        return []


def excel_func(excel_file: Union[str]) -> List[Dict]:
    """Функция для считывания финансовых операций из Excel"""
    try:
        excel_trans = pd.read_excel(excel_file)
        dictionary = excel_trans.to_dict("records")
        return dictionary
    except Exception:
        return []


if __name__ == "__main__":
    datas = excel_func("../data/operations.xlsx")
    searchs = input()
    answer = simple_search(datas, searchs)
    print(answer)
