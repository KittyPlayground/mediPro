from flask import Blueprint, request, jsonify
from flask.templating import render_template

from model.order import Order
from model.medicine import Medicine
import logging

bp = Blueprint('orders', __name__)


@bp.route("/placeOrder")
def place_order():
    return render_template('placeOrderMgt.html')


@bp.route("/api/placeOrder", methods=["POST"])
def handle_order():
    try:
        data = request.get_json()
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

        medicine = Medicine.get_medicines_names(medicine_id)

        if not medicine:
            return jsonify({'error': 'Invalid medicine ID'}), 400

        price_per_item = medicine['price']
        available_quantity = medicine['quantity']

        if available_quantity < quantity:
            return jsonify({'error': 'Insufficient stock for the selected medicine'}), 400

        total = quantity * price_per_item
        discounted_total = total - (total * discount / 100)
        balance = discounted_total - price_to_pay

        if order_id:
            Order.update(order_id, customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks)
            logging.info(f"Order {order_id} updated successfully.")
        else:
            Order.add(customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks)
            logging.info("New order placed successfully.")

        new_quantity = available_quantity - quantity
        Medicine.update_quantity(medicine_id, new_quantity)

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
