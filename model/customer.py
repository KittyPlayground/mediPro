# models/customer.py
from . import get_db_connection
from flask import jsonify

class Customer:
    @staticmethod
    def add(name, email, address):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO Customer (name, email, address) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, address))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(customer_id, name, email, address):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE Customer SET name = %s, email = %s, address = %s WHERE id = %s"
        cursor.execute(query, (name, email, address, customer_id))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(customer_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM Customer WHERE id = %s"
        cursor.execute(query, (customer_id,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_all():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Customer")
        customers = cursor.fetchall()
        cursor.close()
        connection.close()
        return customers

    @staticmethod
    def get_customers_names():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM Customer")
        customers = cursor.fetchall()
        cursor.close()
        connection.close()
        customer_list = [{"id": customer[0], "name": customer[1]} for customer in customers]
        return jsonify({"customers": customer_list})

    @staticmethod
    def get_count():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Customer")
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count
