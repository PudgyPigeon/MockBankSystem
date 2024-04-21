import polars as pl
import logging
from services.users import User

logging.basicConfig(level=logging.INFO)

class BankAccount:
    def __init__(self, user: User):
        self.user = user
        
    @property
    def balance(self) -> float:
        """
        Simplify balance operations by using property decorator
        
        All setters + getters will interface with this balance property
        
        Balance can be updated with simple reassignment of value in 
        class context.

        Returns:
            float: Balance in account
        """
        return self.read_balance_from_file()
    
    @balance.setter
    def balance(self, new_balance: float):
        """
        This function dictates that a setter function will be called
        any time this self.balance attribute is being assigned

        Args:
            new_balance (float): new balance to be set
        """
        self.write_balance_to_file(new_balance, self.user.username)
    
    def read_balance_from_file(self) -> float:
        """
        Every operation will read the balance from file.
        
        Not holding state within class context

        Raises:
            e: Exception

        Returns:
            float: Balance from file
        """
        try:
            df = pl.read_csv(f"data/bank_system.csv")
            user_row = df.filter(df["Username"] == self.user.username)
            if user_row.height != 0:
                return float(user_row["Balance"][0])
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
        
    def write_balance_to_file(self, new_balance: float, username: str) -> None:
        """
        Overwrites balance for user in CSV File

        Args:
            new_balance (float): new balance
            username (str): current user

        Raises:
            e: Error with write operation
        """
        try:
            df = pl.read_csv(f"data/bank_system.csv")
            user_row = df.filter(df["Username"] == username)
            if user_row.height != 0:
                df = df.with_columns(
                    (
                        pl.when(pl.col("Username") == username)
                            .then(pl.lit(new_balance))
                            .otherwise(pl.col("Balance"))
                        .alias("Balance")
                    )
                )
                df.write_csv(f"data/bank_system.csv")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e 
        
    def deposit(self, amount: float) -> None:
        """
        Add amount to balance of current user

        Args:
            amount (float): Any float value

        Raises:
            ValueError: Deposit can't be negative
        """
        if amount <= 0:
            raise ValueError("Deposit must be greater than 0")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Subtract amount from balance of current user

        Args:
            amount (float): Any float value

        Raises:
            ValueError: Can't withdraw more than balance
        """
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
            
class BankAccountService:
    def __init__(self, user, bank_account):
        """
        User object + bank account object for current authorized user

        Args:
            user (User): Current service user
            bank_account (BankAccount): Bank account of current user
        """
        self.user = user
        self.bank_account = bank_account
        
    def manage_account(self):
        """
        While loop to manage account operations
        
        User inputs 1-5 to manage account
        
        Will update balance in CSV file after every transaction
        """
        logging.info("Welcome to your account!")
        logging.info("Select from the following options to manage your account:")
        
        while True:
            try:
                choice = input("\n1: Deposit\n2: Withdraw\n3: Transfer\n4: Check Balance\n5: Exit\n")
                
                if choice == "1":
                    amount = float(input("Enter the amount you want to deposit: "))
                    self.bank_account.deposit(amount)
                    logging.info(f"Deposited {amount} into your account.")
                    logging.info(f"Your new balance is: {self.bank_account.balance}")
                    
                elif choice == "2":
                    amount = float(input("Enter the amount you want to withdraw: "))
                    self.bank_account.withdraw(amount)
                    logging.info(f"Withdrew {amount} from your account.")
                    logging.info(f"Your new balance is: {self.bank_account.balance}")
                    
                elif choice == "3":
                    recipient = input("Enter the username of the recipient: ")
                    amount = float(input("Enter the amount you want to transfer: "))
                    
                    self.bank_account.withdraw(amount)
                    recipient_account = BankAccount(User(recipient))
                    recipient_account.deposit(amount)
                    logging.info(f"Transferred {amount} to {recipient}.")
                    logging.info(f"Your new balance is: {self.bank_account.balance}")
                    
                elif choice == "4":
                    logging.info(f"Your current balance is: {self.bank_account.balance}")
                    
                elif choice == "5":
                    break
                
            except Exception as e:
                logging.error(f"Error: {e}")
                logging.error("Please try again or exit the process with '5'")