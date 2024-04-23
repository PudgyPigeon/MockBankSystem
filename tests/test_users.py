import os
import logging
import pytest
import polars as pl
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, Mock, patch
import bank_app
from bank_app.services.users import UserService, User, UserAuthError

# Should just create mock_files and set that as mock fixture into user object but not enough time
class TestExistingUser:
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
    
    def test_user_init(self, user: User) -> None:
        assert user.username == "Test"
        assert user.password == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        assert user.logged_in == False
        assert user.csv_path == os.path.join(os.getcwd(), "tests", "test_data", "bank_system.csv")
        
    @pytest.mark.parametrize(
        "raw_string, expected_hash",
        [
            ("hellothere", "1d996e033d612d9af2b44b70061ee0e868bfd14c2dd90b129e1edeb7953e7985"),
            ("another_password", "a22780199b8babd7715bf67c839328ee6c0e93153b046d4734c1505a82498561"),
            ("password123", "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f")
        ]
    )
    def test_hash_password(self, user: User, raw_string: str, expected_hash: str) -> None:
        assert user.hash_password(raw_string) == expected_hash
        
    def test_cast_df_col_data_types(self, user: User) -> None:
        df = pl.DataFrame({
            "Username": ["test_user"],
            "Password": ["password"],
            "Balance": [100.0]
        })
        expected_df = pl.DataFrame({
            "Username": pl.Series(["test_user"], dtype=pl.datatypes.Utf8),
            "Password": pl.Series(["password"], dtype=pl.datatypes.Utf8),
            "Balance": pl.Series([100.0], dtype=pl.datatypes.Float64)
        })
        assert user.cast_df_col_data_types(df).equals(expected_df)
            
    def test_login_valid(self, user: User, mocker: MockerFixture) -> None:
        user.authorize = Mock(return_value=True)
        assert user.login() == True
        assert user.authorize.call_args_list == [mocker.call(user.password)]
        
    def test_login_invalid(self, user: User, mocker: MockerFixture) -> None:
        user.authorize = Mock(return_value=False)
        with pytest.raises(UserAuthError) as err_obj:
            user.login()
        assert user.authorize.call_args_list == [mocker.call(user.password)]
        assert str(err_obj.value) == "Authorization failed. Invalid password."
        
    def test_login_already(self, user: User, mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
        mocker.patch.object(user, "logged_in", return_value=True)
        user.login()
        assert "User is already logged in." in caplog.text
        
    def test_authorize(self, user: User, mocker: MockerFixture, caplog: pytest.LogCaptureFixture, mock_dataframe) -> None:
        mocker.patch('bank_app.services.users.pl.read_csv', return_value=mock_dataframe)
        return_value = user.authorize(user.password)
        assert return_value == True
        
    def test_create(self, user: User, mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
        with pytest.raises(ValueError) as err_obj:
            user.create(100)
        assert err_obj.value.args[0] == "Username already exists"

     
class TestNewUser:
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
        user = User("Robert", "hellothere")
        user.csv_path = os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        yield user   
        
    def test_create(self, user: User, mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
        result = user.create(100)
        df = pl.read_csv(user.csv_path)
        assert df.filter(df["Username"] == "Robert").height > 0
        assert result == True

class TestUserService:
    @pytest.fixture
    def user_service(self) -> UserService:
        yield UserService()
        
    @pytest.fixture
    def mock_csv_path(self) -> str:
        yield os.path.join(
            os.getcwd(), "tests", "test_data", "bank_system.csv"
        )
        
    def test_create_user(
        self, 
        user_service: UserService, 
        mocker: MockerFixture, 
        caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.INFO)
        mocker.patch("builtins.input", side_effect=["Robert", "hellothere", "100"])

        mocker.patch("bank_app.services.users.User.create", return_value=True)
        user_service.create_user()
        assert "Successfully created new user!" in caplog.text
        assert bank_app.services.users.User.create.call_args_list == [mocker.call(100)]
        
        print(caplog.text)

    def test_login(
        self, 
        user_service: UserService, 
        mocker: MockerFixture, 
        caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.INFO)
        mocker.patch("builtins.input", side_effect=["Test", "hello"])        
        mocker.patch(
            "bank_app.services.users.User.login", 
            return_value=(True, MagicMock(spec=User)))
        user_service.login()
        assert "Login successful!" in caplog.text
        assert bank_app.services.users.User.login.call_count == 1
        print(caplog.text)