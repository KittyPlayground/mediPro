from flask import Blueprint, request, jsonify, render_template
from model.medicine import Medicine

bp = Blueprint('medicines', __name__)


@bp.route("/medicines")
def medicines_management():
    return render_template('medicineMgt.html')


@bp.route("/api/medicines", methods=["GET", "POST"])
def manage_medicines():
    if request.method == "POST":
        data = request.get_json()
        medicine_id = data.get("medicine_id")
        medicine_name = data.get("medicine_name")
        medicine_price = data.get("medicine_price")
        medicine_quantity = data.get("medicine_quantity")

        if medicine_id:
            Medicine.update(medicine_id, medicine_name, medicine_price, medicine_quantity)
            return jsonify({'message': 'Medicine updated successfully'}), 200
        else:
            Medicine.add(medicine_name, medicine_price, medicine_quantity)
            return jsonify({'message': 'Medicine added successfully'}), 201

    medicines = Medicine.get_all()
    return jsonify({'medicines': [{'id': m[0], 'name': m[1], 'price': m[2], 'quantity': m[3]} for m in medicines]})


@bp.route("/api/medicines/<int:medicine_id>", methods=["DELETE"])
def delete_medicine(medicine_id):
    Medicine.delete(medicine_id)
    return jsonify({'message': 'Medicine deleted successfully'})


@bp.route("/api/medicines/<int:medicine_id>", methods=["PUT"])
def update_medicine(medicine_id):
    data = request.get_json()  # Use get_json() to get JSON data
    medicine_name = data.get("medicine_name")
    medicine_price = data.get("medicine_price")
    medicine_quantity = data.get("medicine_quantity")

    if medicine_id:
        # Update existing medicine
        return Medicine.update(medicine_id, medicine_name, medicine_price, medicine_quantity)
    else:
        return jsonify({'message': 'Medicine ID is required'}), 400
