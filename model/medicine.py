# models/medicine.py
from . import get_db_connection
from flask import jsonify

class Medicine:
    @staticmethod
    def add(name, price, quantity):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO Medicine (name, price, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, price, quantity))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(medicine_id, name, price, quantity):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE Medicine SET name = %s, price = %s, quantity = %s WHERE id = %s"
        cursor.execute(query, (name, price, quantity, medicine_id))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(medicine_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM Medicine WHERE id = %s"
        cursor.execute(query, (medicine_id,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_all():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Medicine")
        medicines = cursor.fetchall()
        cursor.close()
        connection.close()
        return medicines

    @staticmethod
    def get_medicines_names(medicine_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, price FROM Medicine WHERE id = %s", (medicine_id,))
        medicines = cursor.fetchall()
        cursor.close()
        connection.close()

        if medicines:
            return {"id": medicines[0][0], "name": medicines[0][1], "price": medicines[0][2]}
        else:
            return None  # Return None if no medicine found

