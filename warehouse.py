import os
from ast import literal_eval

# Initialize account balance and warehouse inventory
account_balance = 0
inventory = {}
operations = []

def clear_screen():
    if (os.name) == "nt":
        os.system('cls')
    else:
        os.system('clear')

def key_press():
    input("Press ENTER to continue...")

def save_data():
    """Save account balance, inventory, and operations to files."""
    try:
        with open("account_balance.txt", "w") as file:
            file.write(str(account_balance))
    except Exception as e:
        print(f"Error saving 'account' file: {e}")
    try:
        with open("inventory.txt", "w") as file:
            file.write(str(inventory))
    except Exception as e:
        print(f"Error saving 'inventory' file: {e}")
    try:
        with open("operations.txt", "w") as file:
            for operation in operations:
                file.write(str(operation) + "\n")
    except Exception as e:
        print(f"Error saving 'operations' file: {e}")

def load_data():
    clear_screen()
    """Load account balance, inventory, and operations from files."""
    global account_balance, inventory, operations
    try:
        print("*** >>  WAREHOUSE ACCOUNTING << ***\n")
        with open("account_balance.txt", "r") as file:
            account_balance = float(file.read())
            print("Account Balance - loaded!")
    except FileNotFoundError:
        pass
    try:
        with open("inventory.txt", "r") as file:
            inventory = literal_eval(file.read())
            print("Inventory - loaded!")
    except FileNotFoundError:
        pass
    try:
        with open("operations.txt", "r") as file:
            operations = [literal_eval(line) for line in file.readlines()]
            print("History records - loaded!")
            print("\nWarehouse Program successfully initialized!\n")
            key_press()
    except FileNotFoundError:
        pass

# Decoratort for actions
def action_decorator(action):
    def decorator(func):
        func.action = action
        return func
    return decorator

class Manager:
    def __init__(self):
        self.actions = {}

    def assign(self, action_name, func):
        """Assigns an action to a method."""
        self.actions[action_name] = func

    def get_action(self, action_name):
        """Retrieves the assigned method for the given action."""
        return self.actions.get(action_name)

    @action_decorator("balance")
    def manage_balance(self):
        """Add or subtract amount from account balance."""
        global account_balance, operations
        print("\nDo you want to: ")
        print("\t1. Add to account balance ")
        print("\t2. Subtract from account balance ")
        choice = input("Enter choice: ")
        if choice == "1":
            amount = float(input("Please enter amount to add to account balance: "))
            account_balance += amount
            operations.append(("Balance", amount))
            print(f"\nNEW ACCOUNT BALANCE: {account_balance}")
            key_press()
        elif choice == "2":
            amount = float(input("Please enter amount to subtract from account balance: "))
            account_balance -= amount
            operations.append(("Balance", -amount))
            print(f"\nNEW ACCOUNT BALANCE: {account_balance}")
            key_press()
        else:
            print("\nERROR! INVALID COMMAND. TRY AGAIN.")
            key_press()