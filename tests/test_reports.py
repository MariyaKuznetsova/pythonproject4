from unittest.mock import Mock, patch

import pytest

from src.reports import get_date_optional, get_path


def test_get_path():
    mock_get_path = Mock(return_value={"Yes": [50, 21], "No": [131, 2]})
    get_path = mock_get_path
    assert get_path() == {"Yes": [50, 21], "No": [131, 2]}
    mock_get_path.assert_called_with()


def test_get_date_optional():
    mock_get_date_optional = Mock(return_value=("2021-07-14 15:30:00", "2021-03-14 15:30:00"))
    get_date_optional = mock_get_date_optional
    assert get_date_optional() == ("2021-07-14 15:30:00", "2021-03-14 15:30:00")
    mock_get_date_optional.assert_called_with()


def test_spending_by_category():
    mock_spending_by_category = Mock(return_value=[{"Yes": [50, 21], "No": [131, 2]}])
    spending_by_category = mock_spending_by_category
    assert spending_by_category() == [{"Yes": [50, 21], "No": [131, 2]}]
    mock_spending_by_category.assert_called_with()


@patch("pandas.read_excel")
def test_get_path_1(mock_get_path):
    mock_get_path.return_value = {"Валюта операции": "RUB", "Номер карты": "*7197", "Статус": "OK"}
    assert get_path("../data/operation_test.xlsx") == {
        "Валюта операции": "RUB",
        "Номер карты": "*7197",
        "Статус": "OK",
    }
    mock_get_path.assert_called_with("../data/operation_test.xlsx", sheet_name="Отчет по операциям")


def test_get_date_optional_1():
    assert get_date_optional("2021-04-14 15:30:00") == ("14.01.2021 15:30:00", "14.04.2021 15:30:00")


@pytest.fixture
def examples_of_values1():
    return ("14.01.2021 15:30:00", "14.04.2021 15:30:00")


def test_get_date_optional_2(examples_of_values1):
    assert get_date_optional("2021-04-14 15:30:00") == examples_of_values1


@pytest.mark.parametrize(
    "entering_a_value, function_output",
    [
        ("2021-04-14 15:30:00", ("14.01.2021 15:30:00", "14.04.2021 15:30:00")),
        ("2000-12-14 15:30:00", ("15.09.2000 15:30:00", "14.12.2000 15:30:00")),
        ("2020-04-05 15:30:00", ("06.01.2020 15:30:00", "05.04.2020 15:30:00")),
        ("2018-04-01 15:30:00", ("01.01.2018 15:30:00", "01.04.2018 15:30:00")),
    ],
)
def test_get_date_optional_3(entering_a_value, function_output):
    assert get_date_optional(entering_a_value) == function_output


def test_spending_by_category_1():
    mock_spending_by_category = Mock(return_value=[{"Yes": "Yes"}])
    spending_by_category_1 = mock_spending_by_category
    assert spending_by_category_1() == [{"Yes": "Yes"}]
    mock_spending_by_category.assert_called_with()
