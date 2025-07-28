from src.reports import get_date_optional, get_path, spending_by_category
from src.services import excel_func, simple_search
from src.views import main_info

if __name__ == "__main__":
    date_time = "2021-06-14 15:30:00"
    print(main_info(date_time))

    datas = excel_func("../data/operations.xlsx")
    print("Введите данные поиска:")
    search_s = input()
    answer = simple_search(datas, search_s)
    print(answer)

    transactions = get_path("../data/operations.xlsx")
    print("Введите категорию: ")
    category = str(input())
    data = str("2021-07-14 15:30:00")
    dates = get_date_optional(data)
    spend = spending_by_category(transactions, category, data)
