from flask import Blueprint, request, jsonify, render_template, send_from_directory
from model.medicine import Medicine
import os
from werkzeug.utils import secure_filename

bp = Blueprint('medicines', __name__)


@bp.route("/medicines")
def medicines_management():
    return render_template('medicineMgt.html')


UPLOAD_FOLDER = '/Users/tharushikawodya/Developer/mediPro/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp','avif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(image_path):
    return '.' in image_path and image_path.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/api/medicines", methods=["GET", "POST"])
def manage_medicines():
    if request.method == "POST":
        if 'image' not in request.files:
            return jsonify({'message': 'No image part'}), 400
        image_file = request.files['image']

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)  # Save the image

            data = request.form
            medicine_name = data.get("medicine_name")
            medicine_price = data.get("medicine_price")
            medicine_quantity = data.get("medicine_quantity")

            if not (medicine_name and medicine_price and medicine_quantity):
                return jsonify({'message': 'Missing medicine data'}), 400

            Medicine.add(medicine_name, medicine_price, medicine_quantity, filename)
            return jsonify({'message': 'Medicine added successfully'}), 201

        return jsonify({'message': 'Invalid file type'}), 400

    medicines = Medicine.get_all()
    medicines_list = [
        {
            'id': m[0],
            'name': m[1],
            'price': m[2],
            'quantity': m[3],
            'image_path': m[4]  # This should only be the filename
        } for m in medicines
    ]
    return jsonify({'medicines': medicines_list})


@bp.route('/uploads/<path:image_path>')
def uploaded_file(image_path):
    return send_from_directory(UPLOAD_FOLDER, image_path)


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


@bp.route("/api/medicine-count", methods=["GET"])
def get_medicine_count():
    count = Medicine.get_count()
    return jsonify({'count': count})
