# models/order.py
from . import get_db_connection

class Order:
    @staticmethod
    def add(customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO Orders (customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(order_id, customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            UPDATE Orders 
            SET customer_id = %s, medicine_id = %s, quantity = %s, total = %s, 
                discount = %s, price_to_pay = %s, balance = %s, remarks = %s 
            WHERE id = %s
        """
        cursor.execute(query, (customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks, order_id))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_all():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Orders")
        orders = cursor.fetchall()
        cursor.close()
        connection.close()
        return orders
