from unittest.mock import Mock


def test_main_info():
    mock_main_info = Mock(return_value={"Yes": 50, "No": 131})
    main_info = mock_main_info
    assert main_info() == {"Yes": 50, "No": 131}
    mock_main_info.assert_called_with()


def test_main_info_1():
    mock_main_info_1 = Mock(return_value={})
    main_info = mock_main_info_1
    assert main_info() == {}
    mock_main_info_1.assert_called_with()
