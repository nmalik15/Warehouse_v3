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

