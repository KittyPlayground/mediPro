from flask import Flask, render_template, request, jsonify
from model.customer import Customer
from model.medicine import Medicine
from model.order import Order
import logging

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/customers")
def customer_management():
    return render_template('customerMgt.html')


@app.route("/medicines")
def medicines_management():
    return render_template('medicineMgt.html')


@app.route("/placeOrder")
def place_order():
    return render_template('placeOrderMgt.html')


@app.route("/api/customers", methods=["GET", "POST"])
def manage_customers():
    if request.method == "POST":
        data = request.json
        customer_id = data.get("customer_id")
        customer_name = data.get("customer_name")
        customer_email = data.get("customer_email")
        customer_address = data.get("customer_address")

        if customer_id:
            # Update existing customer
            Customer.update(customer_id, customer_name, customer_email, customer_address)
            return jsonify({'message': 'Customer updated successfully'})
        else:
            # Add a new customer
            Customer.add(customer_name, customer_email, customer_address)
            return jsonify({'message': 'Customer added successfully'})

    # Fetch customers from the database
    customers = Customer.get_all()
    return jsonify({'customers': [{'id': c[0], 'name': c[1], 'email': c[2], 'address': c[3]} for c in customers]})


@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    Customer.delete(customer_id)
    return jsonify({'message': 'Customer deleted successfully'})


@app.route("/api/medicines", methods=["GET", "POST"])
def manage_medicines():
    if request.method == "POST":
        data = request.get_json()  # Use get_json() to get JSON data
        medicine_id = data.get("medicine_id")
        medicine_name = data.get("medicine_name")
        medicine_price = data.get("medicine_price")
        medicine_quantity = data.get("medicine_quantity")

        if medicine_id:
            # Update existing medicine
            Medicine.update(medicine_id, medicine_name, medicine_price, medicine_quantity)
            return jsonify({'message': 'Medicine updated successfully'}), 200
        else:
            Medicine.add(medicine_name, medicine_price, medicine_quantity)
            return jsonify({'message': 'Medicine added successfully'}), 201

    medicines = Medicine.get_all()
    return jsonify({'medicines': [{'id': m[0], 'name': m[1], 'price': m[2], 'quantity': m[3]} for m in medicines]})


@app.route("/api/medicines/<int:medicine_id>", methods=["DELETE"])
def delete_medicine(medicine_id):
    Medicine.delete(medicine_id)
    return jsonify({'message': 'Medicine deleted successfully'})


@app.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        return Customer.get_customers_names()
    except Exception as e:
        logging.error(f"Error fetching customers: {str(e)}")
        return jsonify({'error': 'Failed to fetch customers'}), 500


@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    try:
        medicines = Medicine.get_medicines_names()
        return jsonify({'medicines': medicines}), 200
    except Exception as e:
        logging.error(f"Error fetching medicines: {str(e)}")
        return jsonify({'error': 'Failed to fetch medicines'}), 500


@app.route("/api/placeOrder", methods=["POST"])
def handle_order():
    try:
        data = request.get_json()

        # Input validation
        required_fields = ['customer_id', 'medicine_id', 'quantity', 'discount', 'priceToPay']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        order_id = data.get("order_id")
        customer_id = data['customer_id']
        medicine_id = data['medicine_id']
        quantity = int(data['quantity'])
        discount = float(data['discount'])
        price_to_pay = float(data['priceToPay'])
        remarks = data.get('remarks', '')

        # Fetch the medicine by ID
        medicine = Medicine.get_medicines_names(medicine_id)

        if not medicine:
            return jsonify({'error': 'Invalid medicine ID'}), 400

        price_per_item = medicine['price']
        available_quantity = medicine['quantity']  # Get the available quantity from the medicine table

        # Check if there's enough stock for the order
        if available_quantity < quantity:
            return jsonify({'error': 'Insufficient stock for the selected medicine'}), 400

        # Calculate totals
        total = quantity * price_per_item
        discounted_total = total - (total * discount / 100)
        balance = discounted_total - price_to_pay

        if order_id:
            Order.update(order_id, customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks)
            logging.info(f"Order {order_id} updated successfully.")
        else:
            Order.add(customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks)
            logging.info("New order placed successfully.")

        # Update the medicine stock after order
        new_quantity = available_quantity - quantity
        Medicine.update_quantity(medicine_id, new_quantity)

        # Fetch updated medicines list
        updated_medicines = Medicine.get_all()

        return jsonify({
            'message': 'Order placed successfully',
            'medicines': [{'id': m[0], 'name': m[1], 'price': m[2], 'quantity': m[3]} for m in updated_medicines]
        }), 201

    except ValueError as ve:
        logging.error(f"Value error: {str(ve)}")
        return jsonify({'error': 'Invalid value provided'}), 400
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500


if __name__ == "__main__":
    app.run(debug=True)
