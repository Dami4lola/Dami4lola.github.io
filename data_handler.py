import json
from datetime import datetime

class Account:
    _account_counter = 1000

    def __init__(self, account_number=None, balance=0.0):
        if account_number is not None:
            self.account_number = account_number
        else:
            self.account_number = Account._account_counter
            
        self.balance = balance

    def add_charge(self, amount):
        self.balance += amount

    def make_payment(self, amount):
        self.balance -= amount
    
    
    def to_dict(self):
        return {"account_number": self.account_number, "balance": self.balance}

    @classmethod
    def from_dict(cls, data):
        return cls(account_number=data["account_number"], balance=data["balance"])


class Customer:
    _id_counter = 1

    def __init__(self, name, customer_id=None, account=None, orders=None,payments=None):
        if customer_id is not None:
            self.customer_id = customer_id
        else:
            self.customer_id = Customer._id_counter
            Customer._id_counter += 1
            Account._account_counter += 1
        self.name = name
        self.account = account if account else Account()
        self.orders = orders if orders else []
        self.payments = payments if payments else []

    def make_payment(self, amount):
        """Calls make_payment from Account to reduce the balance or add credit."""
        self.account.make_payment(amount)
        # Log the payment
        payment_details = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amount
        }
        self.payments.append(payment_details)
        
    def add_charge(self, amount):
        """Calls add_charge from Account to reduce the balance or add credit."""
        self.account.add_charge(amount)

    def make_order(self, size_of_order, price_per_unit, amount_paid=0.0):
        """Calculates the charge, applies payment, and records the order with date."""
        total_cost = size_of_order * price_per_unit
        # Record the order details with the current date
        order_details = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'size_of_order': size_of_order,
            'price_per_unit': price_per_unit,
            'total_cost': total_cost,
            'amount_paid': amount_paid
        }
        self.add_charge(total_cost)
        self.orders.append(order_details)
        
        self.make_payment(amount_paid)
        

    def view_orders(self):
        """Displays the customer's order history, including dates."""
        if not self.orders:
            print("No previous orders found.")
        else:
            for i, order in enumerate(self.orders, 1):
                print(f"Order {i} (Date: {order['date']}):")
                print(f"  Size of Order: {order['size_of_order']}")
                print(f"  Price per Unit: ${order['price_per_unit']}")
                print(f"  Total Cost: ${order['total_cost']}")
                print(f"  Amount Paid: ${order['amount_paid']}")
                print()

    def to_dict(self):
        """Convert customer information to dictionary format."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "account": self.account.to_dict(),
            "orders": self.orders,
            "payments" : self.payments
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Customer instance from a dictionary."""
        account = Account.from_dict(data["account"])
        return cls(name=data["name"], customer_id=data["customer_id"], account=account, orders=data["orders"],payments=data["payments"])

def load_data():
    try:
        with open("customers.json", "r") as file:
            data = json.load(file)
            customers = {int(cid): Customer.from_dict(cust) for cid, cust in data.items()}
            if customers:
                Customer._id_counter = max(customers.keys()) + 1
            return customers
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Check the file format.")
        return {}

def save_data(customers):
    try:
        data = {cid: customer.to_dict() for cid, customer in customers.items()}
        with open("customers.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error while saving data: {e}")