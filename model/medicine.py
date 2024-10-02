from . import get_db_connection
from flask import jsonify

class Medicine:
    @staticmethod
    def add(name, price, quantity):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "INSERT INTO Medicine (name, price, quantity) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, price, quantity))
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
    def update(medicine_id, name, price, quantity):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "UPDATE Medicine SET name = %s, price = %s, quantity = %s WHERE id = %s"
                cursor.execute(query, (name, price, quantity, medicine_id))
            connection.commit()
            return jsonify({'message': 'Medicine updated successfully'}), 200
        except Exception as e:
            print(f"Error updating medicine: {e}")
            if connection:
                connection.rollback()
            return jsonify({'message': 'Error updating medicine'}), 500
        finally:
            if connection:
                connection.close()

    @staticmethod
    def update_quantity(medicine_id, new_quantity):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "UPDATE Medicine SET quantity = %s WHERE id = %s"
                cursor.execute(query, (new_quantity, medicine_id))
            connection.commit()
            return jsonify({'message': 'Quantity updated successfully'}), 200
        except Exception as e:
            print(f"Error updating medicine quantity: {e}")
            if connection:
                connection.rollback()
            return jsonify({'message': 'Error updating quantity'}), 500
        finally:
            if connection:
                connection.close()

    @staticmethod
    def delete(medicine_id):
        connection = None
        try:
            connection = get_db_connection()
            # Check if medicine is referenced in orders before deleting
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM orders WHERE medicine_id = %s", (medicine_id,))
                if cursor.fetchone()[0] > 0:
                    return jsonify({'message': 'Cannot delete medicine, it is referenced in orders.'}), 400

                query = "DELETE FROM Medicine WHERE id = %s"
                cursor.execute(query, (medicine_id,))
            connection.commit()
            return jsonify({'message': 'Medicine deleted successfully'}), 200
        except Exception as e:
            print(f"Error deleting medicine: {e}")
            if connection:
                connection.rollback()
            return jsonify({'message': 'An error occurred while deleting the medicine'}), 500
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_all():
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Medicine")
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
                cursor.execute("SELECT id, name, price, quantity FROM Medicine WHERE id = %s", (medicine_id,))
                medicines = cursor.fetchall()
            if medicines:
                return {"id": medicines[0][0], "name": medicines[0][1], "price": medicines[0][2], "quantity": medicines[0][3]}
            else:
                return None  # Return None if no medicine found
        finally:
            if connection:
                connection.close()
