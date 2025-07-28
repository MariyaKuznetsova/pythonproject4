import pytest

from src.services import excel_func, simple_search

from unittest.mock import Mock, mock_open, patch

import pandas as pd


def test_excel_func():
    mock_excel_func = Mock(
        return_value={'Yes': [50, 21], 'No': [131, 2]}
    )
    get_path = mock_excel_func
    assert get_path() == {'Yes': [50, 21], 'No': [131, 2]}
    mock_excel_func.assert_called_with()


def test_excel_func_1():
    mock_excel_func_1 = Mock(
        return_value={}
    )
    excel_func = mock_excel_func_1
    assert excel_func() == {}
    mock_excel_func_1.assert_called_with()


@patch("pandas.read_excel")
def test_excel_func_2(mock_excel_file):
    mock_excel_file.return_value = pd.DataFrame([{'Валюта операции': 'RUB', 'Номер карты': '*7197', 'Статус': 'OK'}])
    assert excel_func("../data/operation_test.xlsx") == [{'Валюта операции': 'RUB', 'Номер карты': '*7197', 'Статус': 'OK'}]
    mock_excel_file.assert_called_with('../data/operation_test.xlsx')


@patch("pandas.read_excel")
def test_excel_func_3(mock_excel_file):
    mock_excel_file.return_value = pd.DataFrame([])
    assert excel_func(" ") == []
    mock_excel_file.assert_called_with(" ")


def test_simple_search():
    mock_simple_search = Mock(
        return_value=[{'Yes': 4, 'No': 6}]
    )
    simple_search = mock_simple_search
    assert simple_search() == [{'Yes': 4, 'No': 6}]
    mock_simple_search.assert_called_with()


def test_simple_search_1():
    mock_simple_search_1 = Mock(
        return_value=[{}]
    )
    simple_search = mock_simple_search_1
    assert simple_search() == [{}]
    mock_simple_search_1.assert_called_with()






