import pytest
import polars as pl
from unittest.mock import Mock, patch
import services.users as user_module
from services.users import UserService, User, UserAuthError

# Should just create mock_files and set that as mock fixture into user object but not enough time
class TestUser:
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
    def user(self, mock_dataframe, mocker) -> User:
        user = User("Test", "hello")
        return user 
    
    def test_user_init(self, user: User) -> None:
        assert user.username == "Test"
        assert user.password == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        assert user.logged_in == False
    
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
            
    def test_login_valid(self, user: User, mocker) -> None:
        user.authorize = Mock(return_value=True)
        assert user.login() == True
        assert user.authorize.call_args_list == [mocker.call(user.password)]
        
    def test_login_invalid(self, user: User, mocker) -> None:
        user.authorize = Mock(return_value=False)
        with pytest.raises(UserAuthError) as err_obj:
            user.login()
        assert user.authorize.call_args_list == [mocker.call(user.password)]
        assert str(err_obj.value) == "Authorization failed. Invalid password."
        
    def test_login_already(self, user: User, mocker, caplog) -> None:
        mocker.patch.object(user, "logged_in", return_value=True)
        user.login()
        assert "User is already logged in." in caplog.text
        
    def test_authorize(self, user: User, mocker, caplog, mock_dataframe) -> None:
        mocker.patch('services.users.pl.read_csv', return_value=mock_dataframe)
        return_value = user.authorize(user.password)
        assert return_value == True
        
    # def test_create(self, mocker, caplog, mock_dataframe) -> None:
    #     mock_read = mocker.patch('services.users.pl.read_csv', return_value=mock_dataframe)
    #     mock_write = mocker.patch('services.users.pl.DataFrame.write_csv', return_value=None)    
    #     mock_user = User("Test3", "hellothere")
        
    #     mocker.spy(user_module.pl.DataFrame, 'vstack')
    #     mock_user.create(100)
        
    #     pl.DataFrame.vstack.assert_called_once_with(pl.DataFrame({
    #         "Username": ["Test3"],
    #         "Password": ["1d996e033d612d9af2b44b70061ee0e868bfd14c2dd90b129e1edeb7953e7985"],
    #         "Balance": [100.0]
    #     }))
        
    #     assert mock_read.call_args_list == [mocker.call("data/bank_system.csv")]
    #     assert mock_write.call_args_list == [mocker.call("data/bank_system.csv")]