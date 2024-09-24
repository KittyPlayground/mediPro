from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
customers = []
medicines = []

@app.route("/")
def home():
    return render_template('home.html')
@app.route("/customers")
def customer_management():
    return render_template('customerMgt.html', customers=customers)

@app.route("/medicines")
def medicines_management():
    return render_template('medicineMgt.html', medicines=medicines)

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

@app.route("/api/medicines", methods=["GET", "POST"])
def manage_medicines():
    if request.method == "POST":
        data = request.json

        medicine_id = data.get("medicine_id")
        medicine_name = data.get("medicine_name")
        medicine_price = data.get("medicine_price")
        medicine_quantity = data.get("medicine_quantity")

        if medicine_id:
            for medicine in medicines:
                if medicine['id'] == int(medicine_id):
                    medicine['name'] = medicine_name
                    medicine['price'] = medicine_price
                    medicine['quantity'] = medicine_quantity
                    return jsonify({'message': 'Medicine updated successfully'})
        else:
            # Add a new medicine
            medicine = {
                'id': len(medicines) + 1,
                'name': medicine_name,
                'price': medicine_price,
                'quantity': medicine_quantity
            }
            medicines.append(medicine)
            return jsonify({'message': 'Medicine added successfully'})

    return jsonify({'medicines': medicines})

@app.route("/api/medicines/<int:medicine_id>", methods=["DELETE"])
def delete_medicine(medicine_id):
    global medicines
    medicines = [medicine for medicine in medicines if medicine['id'] != medicine_id]
    return jsonify({'message': 'Medicine deleted successfully'})





if __name__ == "__main__":
    app.run(debug=True)
