import logging
from bank_app.services.bank_account import BankAccount, BankAccountService
from bank_app.services.users import UserService
logging.basicConfig(level=logging.INFO)
    
# Maybe refactor later to use Rich-Click package for formatting and pretty printing + colors
def run() -> None:
    """
    Entrypoint script for mock banking system
    """
    try:
        logging.info("Welcome to the bank system!")
        user_input = input("\n1: Create a new user\n2: Login to existing user\nEnter your choice (1/2): ")
        
        user_service = UserService()
        
        if user_input == "1":
            logging.info("Process will now create a new user")
            user_service.create_user()
            
        elif user_input == "2":
            logging.info("Attempting login process now...")
            
            # Get boolean for success and user object
            logged_in_bool, user = user_service.login()
            
            if logged_in_bool and user is not None:
                logging.info("Setting up connection to banking services...")
                account = BankAccount(user)
                bank_service = BankAccountService(user, account)
                bank_service.manage_account()
            else:
                raise Exception("Invalid login attempt, please try again")
            
        logging.info("Exiting process...")
            
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    run()