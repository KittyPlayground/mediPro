from flask import Blueprint, request, jsonify, render_template
from model.customer import Customer

bp = Blueprint('customers', __name__)


@bp.route("/customers")
def customer_management():
    return render_template('customerMgt.html')


@bp.route("/api/customer-count", methods=["GET"])
def get_customer_count():
    count = Customer.get_count()
    return jsonify({'count': count})


@bp.route("/api/customers", methods=["GET", "POST"])
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

    customers = Customer.get_all()
    return jsonify({'customers': [{'id': c[0], 'name': c[1], 'email': c[2], 'address': c[3]} for c in customers]})


@bp.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    Customer.delete(customer_id)
    return jsonify({'message': 'Customer deleted successfully'})
