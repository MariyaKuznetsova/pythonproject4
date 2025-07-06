from src.views import main_info
#from src.reports import
from src.services import excel_func, simple_search

from pprint import pprint

if __name__ == "__main__":
    date_time = "2021-06-14 15:30:00"
    print(main_info(date_time))
