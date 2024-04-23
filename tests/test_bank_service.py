import logging
import os
import pytest
import polars as pl
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, Mock, patch
import bank_app
from bank_app.services.bank_account import BankAccount, BankAccountService
from bank_app.services.users import User, UserService
        
class TestBankService:
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
    def bank_account_service(self, mocker: MockerFixture) -> BankAccountService:
        csv_path = os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        user = User("Test", "hello")
        user.csv_path = csv_path
        bank_account = BankAccount(user)
        bank_account.csv_path = csv_path
        yield BankAccountService(user, bank_account)
        
    @pytest.fixture(scope="function", autouse=False)
    def recipient_bank_account(self, mocker: MockerFixture) -> BankAccount:
        csv_path = os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        user = User("Test2")
        user.csv_path = csv_path
        bank_account = BankAccount(user)
        bank_account.csv_path = csv_path
        yield bank_account
    
    def test_user_input_deposit(
        self,
        bank_account_service: BankAccountService,
        mocker: MockerFixture,
    ) -> None:
        # The side effects are as follows:
        # 1 -> Deposit command
        # 100.0 is the amount
        # 5 is to exit the while loop
        mocker.patch("builtins.input", side_effect=["1", "100.0", "5"])
        bank_account_service.manage_account()
        assert bank_account_service.bank_account.balance == 499.0
        
    def test_user_input_withdraw(
        self,
        bank_account_service: BankAccountService,
        mocker: MockerFixture,
    ) -> None:
        # The side effects are as follows:
        # 2 -> Deposit command
        # 100.0 is the amount
        # 5 is to exit the while loop
        mocker.patch("builtins.input", side_effect=["2", "100.0", "5"])
        bank_account_service.manage_account()
        assert bank_account_service.bank_account.balance == 399.0
    
    def test_user_input_check_balance(
        self,
        bank_account_service: BankAccountService,
        mocker: MockerFixture,
        caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.INFO)
        # The side effects are as follows:
        # 3 -> Check balance command
        # 5 is to exit the while loop
        mocker.patch("builtins.input", side_effect=["4", "5"])
        bank_account_service.manage_account()
        assert bank_account_service.bank_account.balance == 399.0
        assert "Your current balance is: 399.0" in caplog.text
        print(caplog.text)

    def test_user_input_transfer(
        self,
        bank_account_service: BankAccountService,
        recipient_bank_account: BankAccount,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("builtins.input", side_effect=["3", "Test2", "100", "5"])
        
        mock_transfer_fn = mocker.patch.object(bank_account_service, "transfer")
        mocker.patch("bank_app.services.bank_account.BankAccount", autospec=True, return_value=recipient_bank_account)

        
        bank_account_service.manage_account()
        
        assert mock_transfer_fn.call_count == 1
        assert mock_transfer_fn.call_args == mocker.call(
            bank_account_service.bank_account, 
            recipient_bank_account, 
            100.0
        )
        
    def test_transfer_fn(
        self,
        bank_account_service: BankAccountService,
        recipient_bank_account: BankAccount,
        mocker: MockerFixture,
        caplog: pytest.LogCaptureFixture    
    ) -> None:
        
        caplog.set_level(logging.INFO)
        
        bank_account_service.transfer(bank_account_service.bank_account, recipient_bank_account, 100.0)
        
        assert bank_account_service.bank_account.balance == 299.0
        assert recipient_bank_account.balance == 1100.0
        
        print(caplog.text)
