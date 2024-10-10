from . import get_db_connection
from flask import jsonify

class Medicine:
    @staticmethod
    def add(name, price, quantity, image_path):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "INSERT INTO Medicine (name, price, quantity, image_path) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (name, price, quantity, image_path))
            connection.commit()
            return jsonify({'message': 'Medicine added successfully'}), 201
        except Exception as e:
            print(f"Error adding medicine: {e}")
            if connection:
                connection.rollback()
            return jsonify({'message': 'Error adding medicine'}), 500
        finally:
            if connection:
                connection.close()
    @staticmethod
    def update_quantity(medicine_id, new_quantity):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = """
                    UPDATE Medicine
                    SET quantity = %s 
                    WHERE id = %s
                """
                cursor.execute(query, (new_quantity, medicine_id))
            connection.commit()
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating medicine quantity: {e}")
            if connection:
                connection.rollback()
            return False  # Indicate failure
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_all():
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, price, quantity, image_path FROM Medicine")
                medicines = cursor.fetchall()
            return medicines
        finally:
            if connection:
                connection.close()


    @staticmethod
    def get_medicines_names(medicine_id):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, price, quantity, image_path FROM Medicine WHERE id = %s", (medicine_id,))
                medicines = cursor.fetchall()
            if medicines:
                return {"id": medicines[0][0], "name": medicines[0][1], "price": medicines[0][2], "quantity": medicines[0][3], "image_path": medicines[0][4]}
            else:
                return None  # Return None if no medicine found
        finally:
            if connection:
                connection.close()
