from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
customers = []

@app.route("/")
def customer_management():
    return render_template('customerMgt.html', customers=customers)

@app.route("/api/customers", methods=["GET", "POST"])
def manage_customers():
    if request.method == "POST":
        data = request.json

        customer_id = data.get("customer_id")
        customer_name = data.get("customer_name")
        customer_email = data.get("customer_email")

        # Check if it's an update request
        if customer_id:
            for customer in customers:
                if customer['id'] == int(customer_id):
                    customer['name'] = customer_name
                    customer['email'] = customer_email
                    return jsonify({'message': 'Customer updated successfully'})
        else:
            # Add a new customer
            customer = {
                'id': len(customers) + 1,
                'name': customer_name,
                'email': customer_email
            }
            customers.append(customer)
            return jsonify({'message': 'Customer added successfully'})

    return jsonify({'customers': customers})


@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    global customers
    customers = [customer for customer in customers if customer['id'] != customer_id]
    return jsonify({'message': 'Customer deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
