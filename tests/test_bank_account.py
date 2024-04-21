import pytest
import polars as pl
from unittest.mock import Mock, patch
from services.bank_account import BankAccount, BankAccountService
from services.users import User, UserService

class TestBankAccount:
    @pytest.fixture
    def mock_dataframe(self):
        data = {
            "Username": ["Test", "Test2"],
            "Password": ["2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", 
                        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"],
            # passwords are all "hello"
            "Balance": [399.0, 1000.0]
        }
        df = pl.DataFrame(data)
        yield df
        
    @pytest.fixture
    def user(self, mocker) -> User:
        user = User("Test", "hello")
        return user 
    
    @pytest.fixture
    def bank_account(self, user):
        return BankAccount(user)
    
    def test_read_balance(
        self, 
        bank_account: BankAccount, 
        mocker, 
        mock_dataframe: pl.DataFrame
    ) -> None:
        mocker.patch("polars.read_csv", return_value=mock_dataframe)
        assert bank_account.balance == 399.0
        
    # def test_set_balance(self, bank_account: BankAccount, mocker, mock_dataframe) -> None:
    #     mocker.patch("polars.read_csv", return_value=mock_dataframe)
    #     mocker.patch("polars.write_csv", return_value=None)
    #     bank_account.balance = 500.0
    #     assert bank_account.balance == 500.0
    
    # def test_bank_account_init(self, bank_account: BankAccount) -> None:
    #     assert bank_account.username == "test_user"
    #     assert bank_account.balance == 100.0
    #     assert bank_account.logged_in == False
    
    # def test_deposit(self, bank_account: BankAccount) -> None:
    #     bank_account.deposit(100.0)
    #     assert bank_account.balance == 200.0
        
    # def test_withdraw(self, bank_account: BankAccount) -> None:
    #     bank_account.withdraw(50.0)
    #     assert bank_account.balance == 50.0
        
    # def test_transfer(self, bank_account: BankAccount, mocker) -> None:
    #     bank_account_2 = BankAccount("test_user_2", 100.0)
    #     bank_account_2.deposit = Mock()
    #     bank_account.transfer(50.0, bank_account_2)
    #     assert bank_account.balance == 50.0
    #     assert bank_account_2.deposit.call_args_list == [mocker.call(50.0)]
        
    # def test_transfer_insufficient_funds(self, bank_account: BankAccount, mocker) -> None:
    #     bank_account_2 = BankAccount("test_user_2", 100.0)
    #     with pytest.raises(ValueError) as err_obj:
    #         bank_account.transfer(200.0, bank_account_2)
    #     assert str(err_obj.value) == "Insufficient funds."
        
    # def test_transfer_invalid_user(self, bank_account: BankAccount, mocker) -> None:
    #     bank_account_2 = BankAccount("test_user_2", 100.0)
    #     with pytest.raises(ValueError) as err_obj:
    #         bank_account.transfer(50.0, bank_account_2)
    #     assert str(err_obj.value) == "Invalid user."
        
    # def test_transfer_self(self, bank_account: BankAccount) -> None:
    #     with pytest.raises(ValueError) as err_obj:
    #         bank_account.transfer(50.0, bank_account)
    #     assert str(err_obj.value) == "Cannot transfer to self."
        
    # def test_transfer_logged_out(self, bank_account: BankAccount) -> None:
    #     bank_account_2 = BankAccount("test_user_2", 100.0)
    #     bank_account.logged_in = False
    #     with pytest.raises(ValueError) as err_obj:
