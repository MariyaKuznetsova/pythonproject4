import os
from unittest.mock import Mock, patch

import pytest
from dotenv import load_dotenv

import src.utils
from src.utils import get_date_time

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")


def test_get_time_for_greeting():
    mock_get_time_for_greeting = Mock(return_value="Доброе утро")
    get_time_for_greeting = mock_get_time_for_greeting
    assert get_time_for_greeting() == "Доброе утро"
    mock_get_time_for_greeting.assert_called_with()


def test_get_path_and_period():
    mock_get_path_and_period = Mock(return_value={"Yes": [50, 21], "No": [131, 2]})
    get_path_and_period = mock_get_path_and_period
    assert get_path_and_period() == {"No": [131, 2], "Yes": [50, 21]}
    mock_get_path_and_period.assert_called_with()


def test_get_card_with_spend():
    mock_get_card_with_spend = Mock(return_value=[{"Yes": "52", "No": "2"}])
    get_card_with_spend = mock_get_card_with_spend
    assert get_card_with_spend() == [{"Yes": "52", "No": "2"}]
    mock_get_card_with_spend.assert_called_with()


def test_get_date_time_1():
    assert get_date_time("2021-04-14 08:30:00") == ["01.04.2021 00:00:00", "14.04.2021 08:30:00"]


@pytest.fixture
def examples_of_values1():
    return ["01.04.2021 00:00:00", "14.04.2021 08:30:00"]


def test_get_date_time_2(examples_of_values1):
    assert get_date_time("2021-04-14 08:30:00") == examples_of_values1


@pytest.mark.parametrize(
    "date_a_value, function_output",
    [
        ("2021-04-14 08:30:00", ["01.04.2021 00:00:00", "14.04.2021 08:30:00"]),
        ("2000-12-14 18:30:00", ["01.12.2000 00:00:00", "14.12.2000 18:30:00"]),
        ("2020-04-05 15:30:00", ["01.04.2020 00:00:00", "05.04.2020 15:30:00"]),
        ("2018-04-01 00:30:00", ["01.04.2018 00:00:00", "01.04.2018 00:30:00"]),
    ],
)
def test_get_date_time(date_a_value, function_output):
    assert get_date_time(date_a_value) == function_output


def test_get_top_transactions():
    mock_get_top_transactions = Mock(return_value=[{"Yes": "Yes"}])
    get_top_transactions = mock_get_top_transactions
    assert get_top_transactions() == [{"Yes": "Yes"}]
    mock_get_top_transactions.assert_called_with()


@patch("requests.get")
def test_get_currency(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 78.496243, "EUR": 0.862627}}
    result_1 = src.utils.get_currency("../data/user_settings_1.json")
    assert result_1 == [{"currency": "USD", "rate": "78.5"}, {"currency": "EUR", "rate": "91.0"}]
    mock_get.assert_called_with(f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}", encoding="utf-8")


@patch("requests.get")
def test_get_stock(mock_get):
    mock_get.return_value.json.return_value = {"Global Quote": {"01. symbol": "AAPL", "05. price": "213.8800"}}
    result_2 = src.utils.get_stock("../data/user_settings_1.json")
    assert result_2 == [{"price": "213.8800", "stock": "AAPL"}]
    stock = "AAPL"
    mock_get.assert_called_with(
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK}",
        encoding="utf-8",
    )
