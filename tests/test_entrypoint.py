import pytest
from unittest.mock import patch, Mock
from services.bank_account import BankAccount, BankAccountService
from services.users import UserService
from entrypoint import run

def test_run_create_user(mocker):
    mock_create_user = mocker.patch.object(UserService, 'create_user')
    mocker.patch('builtins.input', return_value="1")
    run()    
    assert mock_create_user.call_count == 1

def test_run_login(mocker):
    mock_manage_account = mocker.patch.object(BankAccountService, 'manage_account')
    mock_login = mocker.patch.object(UserService, 'login', return_value=(True, Mock()))
    mocker.patch('builtins.input', return_value="2")
    run()
    assert mock_login.call_count == 1
    assert mock_manage_account.call_count == 1
    
def test_run_login_failed_with_exception(mocker):
    mock_login = mocker.patch.object(UserService, 'login', return_value=(False, None))
    mocker.patch('builtins.input', return_value="2")
    with pytest.raises(Exception) as e_info:
        run()
    assert str(e_info.value) == "Invalid login attempt, please try again"
    assert mock_login.call_count == 1