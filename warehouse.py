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
    
    @action_decorator("sale")
    def record_sale(self):
        """Record a sale."""
        global account_balance, inventory, operations
        product = input("Enter product name: ")
        if product in inventory:
            price = inventory[product][1]
            quantity = int(input("Enter product quantity: "))
            if quantity <= inventory[product][0]:
                total_sale = price * quantity
                account_balance += total_sale
                inventory[product] = (inventory[product][0] - quantity, price)
                if inventory[product][0] == 0:
                    del inventory[product]
                operations.append(("Sale", (product, quantity, price, total_sale)))
                print(f"Sale recorded. New account balance: {account_balance}")
                key_press()
            else:
                print(f"Insufficient quantity of {product} in the inventory.")
                key_press()
        else:
            print(f"{product} is not available in the inventory.")
            key_press()

    @action_decorator("purchase")
    def record_purchase(self):
        """Record a purchase."""
        global account_balance, inventory, operations
        product = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        total_cost = price * quantity
        if total_cost <= account_balance:
            account_balance -= total_cost
            if product in inventory:
                inventory[product] = (inventory[product][0] + quantity, price)
            else:
                inventory[product] = (quantity, price)
            operations.append(("Purchase", (product, quantity, price, total_cost)))
            print(f"Purchase recorded. New account balance: {account_balance}")
            key_press()
        else:
            print("ERROR! INSUFFICIENT BALANCE FOR THIS PURCHASE!")
            key_press()

    @action_decorator("account")
    def display_account_balance(self):
        """Display current account balance."""
        global account_balance
        print(f"\nCurrent account balance: {account_balance}")
        key_press()

    @action_decorator("list")
    def display_inventory(self):
        """Display warehouse inventory."""
        global inventory
        print("Warehouse Inventory:")
        for product, (quantity, price) in inventory.items():
            print(f"{product}:\n\tStock: {quantity} \n\tPrice: {price}")
        key_press()

    @action_decorator("warehouse")
    def display_product_status(self):
        """Display product status in warehouse."""
        global inventory
        product = input("Enter product name: ")
        if product in inventory:
            quantity, price = inventory[product]
            print(f"{product}:\n\tStock: {quantity} \n\tPrice: {price}")
            key_press()
        else:
            print(f"Error! {product} is not in the warehouse.".upper())
            key_press()

    @action_decorator("review")
    def review_operations(self):
        """Review recorded operations."""
        global operations
        start = input("Enter starting index (leave blank to start from the beginning): ")
        end = input("Enter ending index (leave blank to go until the end): ")
        if not start:
            start = 0
        else:
            start = int(start)
        if not end:
            end = len(operations)
        else:
            end = int(end)
        if start < 0 or end > len(operations) or start >= end:
            print("Invalid range.")
            key_press()
        else:
            for i in range(start, end):
                operation, details = operations[i]
                if operation == "Balance":
                    amount = details
                    print(f"{i+1}. Balance changed by {amount}")
                elif operation == "Sale":
                    product, quantity, price, total_sale = details
                    print(f"{i+1}. Sold {quantity} units of {product} for {total_sale}")
                elif operation == "Purchase":
                    product, quantity, price, total_cost = details
                    print(f"{i+1}. Purchased {quantity} units of {product} for {total_cost}")
            key_press()

    