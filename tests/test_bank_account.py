import os
import pytest
import polars as pl
from pytest_mock import MockerFixture
from unittest.mock import Mock, patch
from bank_app.services.bank_account import BankAccount, BankAccountService
from bank_app.services.users import User, UserService

class TestBankAccount:
    @classmethod
    def teardown_class(cls) -> None:
        csv_path = os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        data = {
            "Username": ["Test", "Test2"],
            "Password": ["2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", 
                        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"],
            # passwords are all "hello"
            "Balance": [399.0, 1000.0]
        }
        df = pl.DataFrame(data)
        df.write_csv(csv_path)

    @pytest.fixture
    def user(self, mocker: MockerFixture) -> User:
        user = User("Test", "hello")
        user.csv_path = os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        yield user 
    
    @pytest.fixture
    def bank_account(self, user: User, mocker: MockerFixture):
        bank_account = BankAccount(user)
        bank_account.csv_path = os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        yield bank_account
    
    def test_read_balance(
        self, 
        bank_account: BankAccount, 
        mocker: MockerFixture, 
    ) -> None:
        assert bank_account.balance == 399.0
        
    def test_deposit(
        self,
        bank_account: BankAccount,
    ) -> None:
        bank_account.deposit(100.0)
        assert bank_account.balance == 499.0

    @pytest.mark.parametrize(
        "deposit",
        [
            -1000.0, -1.0, -893475983.0, -0.1
        ]
    )
    def test_deposit_invalid(
        self,
        deposit: float,
        bank_account: BankAccount,
    ) -> None:
        with pytest.raises(ValueError) as err_obj:
            bank_account.deposit(deposit)
        assert err_obj.value.args[0] == "Deposit must be greater than 0"
    
    def test_withdraw(
        self,
        bank_account: BankAccount,
    ) -> None:
        bank_account.withdraw(150.0)
        assert bank_account.balance == 349.0

    def test_withdraw_invalid(
        self,
        bank_account: BankAccount,
    ) -> None:
        with pytest.raises(ValueError) as err_obj:
            bank_account.withdraw(100000000.0)
        assert err_obj.value.args[0] == "Insufficient funds"    
        
    def test_write_balance(
        self,
        bank_account: BankAccount,
    ) -> None:
        bank_account.balance = 12345.0
        assert bank_account.balance == 12345.0
