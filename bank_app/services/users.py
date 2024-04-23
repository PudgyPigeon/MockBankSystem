import hashlib
import polars as pl
import typing
import logging
import os 

logging.basicConfig(level=logging.INFO)

# TO DO - parametrize os.getcwd pathing?

class UserAuthError(Exception):
    """Custom exception class for user auth errors
    
    Helps for clarity and figuring out what type of error is popping up
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
class User:
    """
    User object to mainly deal with auth and creation of users
    
    Bank account operations done in other class
    """
    def __init__(
        self, 
        username: typing.Optional[str] = None, 
        password: typing.Optional[str] = None, 
    ) -> None:
        self.username = username if username is not None else ""
        self.password = self.hash_password(password) if password is not None else ""
        self.logged_in = False
        self.csv_path = os.path.join(
            os.getcwd(), "bank_app", "data", "bank_system.csv"
        )
        
    def hash_password(self, password: str) -> str:
        """
        Hash the inputted password for security

        Args:
            password (str): Str input password

        Returns:
            str: Hashed value
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def create(
        self,
        balance: typing.Optional[float] = 0.0
    ) -> bool:
        """
        Checks CSV for existing username, then creates new user if not found.

        Args:
            balance (typing.Optional[float], optional): Balance to start account with. Defaults to 0.0.

        Raises:
            ValueError: Existing username
            e: Other general exceptions

        Returns:
            bool: True or False if success or failure
        """
        try:
            df = pl.read_csv(self.csv_path)
            df = self.cast_df_col_data_types(df)
            
            if df.filter(df["Username"] == self.username).height > 0:
                raise ValueError("Username already exists")
            
            new_row = pl.DataFrame({
                "Username": [self.username],
                "Password": [self.password],
                "Balance": [float(balance)]
            })
            df = df.vstack(new_row)
            df.write_csv(self.csv_path)
            return True
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
        
    def authorize(self, password: str) -> bool:
        """
        Compares input password with hashed password in CSV

        Args:
            password (str): Password to compare - from user input

        Raises:
            ValueError: Wrong password or username
            e: General exception obj

        Returns:
            bool: True or False for success or failure
        """
        try:
            df = pl.read_csv(self.csv_path)
            df = self.cast_df_col_data_types(df)
            user_row = df.filter(df["Username"] == self.username)
            
            # only checks if height is 0, but does not handle duplicates
            # something to check at later point if error with creation process
            if user_row.height != 0 and user_row["Password"][0] == password:
                return True
            else:
                raise ValueError("Invalid username or password")
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e    

    def login(self) -> bool:
        """
        Wrapper logic to check if current user is logged in or not
        
        If not logged in, trigger login auth process

        Raises:
            UserAuthError: Failed auth
            UserAuthError: Already logged in

        Returns:
            bool: True or False
        """
        if not self.logged_in:
            if self.authorize(self.password):
                self.logged_in = True
                return True
            else:
                raise UserAuthError("Authorization failed. Invalid password.")
        else:
            # Not sure if this is necessary but just in case
            logging.warning("User is already logged in.")
            return True
        
    def cast_df_col_data_types(self, df: pl.DataFrame) -> pl.DataFrame:
        """Explicitly define column data types for Polars dataframes

        Args:
            df (pl.DataFrame): Dataframe from CSV

        Returns:
            pl.DataFrame: Dataframe with casted types
        """
        df = df.with_columns(
            [
                df["Username"].cast(pl.datatypes.Utf8), 
                df["Password"].cast(pl.datatypes.Utf8), 
                df["Balance"].cast(pl.datatypes.Float64)
            ]
        )
        return df
    
class UserService():
    """
    Services module to define logical operations for user creation and login
    
    Separated for cleanliness
    """
    # TO DO - maybe tie User class to state of user service
    # but not necessary for PoC'
    def __init__(self) -> None:
        pass
    
    def create_user(self) -> None:
        """General user creation process logic
        
        Retry mechanism if user input is invalid or creation fails

        Raises:
            UserAuthError: Auth failure
        """
        try:
            # Maybe collapse this functionality into user module but not enough time for now
            logging.info("Please enter the desired username and password for the newly created account:")
            logging.info("You may also input a starting balance for the account. If no balance is entered, the account will start with a balance of 0.")
            
            # TODO - input validation of data types, length, etc
            username = input("Username: ")
            password = input("Password: ")
            balance = input("Starting balance: ")
            
            if balance == "":
                balance = 0.0 
            else:
                balance = float(balance)
                
            new_user = User(username, password)
            
            if new_user.create(balance):
                logging.info("Successfully created new user!")
                logging.info("Please restart the program and login to access your account.")
            else:
                raise UserAuthError("Error creating user")
            
        except Exception as e:
            retry_input = input("Type '1' to retry creation process or '2' to exit...")
            
            if retry_input == "1":
                self.create_user()
            elif retry_input == "2":
                return
        
    def login(self) -> typing.Tuple[bool, User]:
        """Attempts login

        Returns:
            typing.Tuple[bool, User]: True or False + User object
        """
        try:
            logging.info("Please enter the username and password of the account you want to access")
            
            username = input("Username: ")
            password = input("Password: ")
            
            user = User(username, password)   
            
            if user.login():
                logging.info("Login successful!")
                # return user obj so bank account module can use it
                return True, user
            
        except Exception as e:
            raise e
                 
