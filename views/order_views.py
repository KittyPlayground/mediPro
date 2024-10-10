from flask import Blueprint, request, jsonify
from flask.templating import render_template

from model.order import Order
from model.medicine import Medicine
import logging
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

bp = Blueprint('orders', __name__)

sender_email = os.getenv('EMAIL_USER')
sender_password = os.getenv('EMAIL_PASSWORD')


@bp.route("/placeOrder")
def place_order():
    return render_template('placeOrderMgt.html')


@bp.route("/api/placeOrder", methods=["POST"])
def handle_order():
    try:
        data = request.get_json()

        required_fields = ['customer_id', 'medicine_id', 'quantity', 'discount', 'priceToPay', 'customer_email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        order_id = data.get("order_id")
        customer_id = data['customer_id']
        medicine_id = data['medicine_id']
        quantity = int(data['quantity'])
        discount = float(data['discount'])
        price_to_pay = float(data['priceToPay'])
        customer_email = data['customer_email']  # Get the customer's email
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

            # Send receipt to customer
            send_receipt(customer_email, {
                'order_id': order_id,
                'customer_id': customer_id,
                'medicine_name': medicine['name'],
                'quantity': quantity,
                'total_price': discounted_total,
                'discount': discount,
                'remarks': remarks,
            })

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


def send_receipt(customer_email, receipt_data):
    subject = "Your Order Receipt"
    body = f"""
    Dear Customer,

    Thank you for your order! Here are the details:

    Customer ID: {receipt_data['customer_id']}
    Medicine: {receipt_data['medicine_name']}
    Quantity: {receipt_data['quantity']}
    Total Price: ${receipt_data['total_price']:.2f}
    Discount: {receipt_data['discount']}%
    Remarks: {receipt_data['remarks']}

    Thank you for choosing us!

    Best regards,
    MediPro Team
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = customer_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        logging.info("Receipt sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")


@bp.route("/api/order-count", methods=["GET"])
def get_order_count():
    count = Order.get_count()
    return jsonify({'count': count})
