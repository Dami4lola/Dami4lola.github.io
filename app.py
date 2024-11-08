from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime
from data_handler import load_data, save_data, Customer, Account

app = Flask(__name__, template_folder='.')

# Load customers on startup
customers = load_data()

@app.route('/')
def index():
    return render_template('index.html', customers=customers.values())

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    customer = Customer(name)
    customers[customer.customer_id] = customer
    save_data(customers)
    return redirect(url_for('index'))

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = customers.get(customer_id)
    if not customer:
        return "Customer not found", 404

    if request.method == 'POST':
        # Handle customer deletion
        if 'delete' in request.form:
            del customers[customer_id]
            save_data(customers)
            return redirect(url_for('index'))

        # Check if we are placing an order
        if 'size_of_order' in request.form and 'price_per_unit' in request.form:
            size_of_order = float(request.form['size_of_order'])
            price_per_unit = float(request.form['price_per_unit'])
            amount_paid = float(request.form.get('amount_paid', 0))
            
            # Place the order (make_order will handle the payment if provided)
            customer.make_order(size_of_order, price_per_unit, amount_paid)
        
        # If we are only making a payment without placing an order
        elif 'amount_paid' in request.form:
            amount_paid = float(request.form['amount_paid'])
            customer.make_payment(amount_paid)
        
        if 'delete' in request.form:
            del customers[customer_id]
            save_data(customers)
            return redirect(url_for('index'))

        save_data(customers)
        return redirect(url_for('index'))

    return render_template('edit_customer.html', customer=customer)

if __name__ == '__main__':
    app.run(debug=True)
