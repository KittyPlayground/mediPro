from . import get_db_connection
from flask import jsonify

class Order:
    @staticmethod
    def add(customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Orders (customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks))
            connection.commit()
            return jsonify({'message': 'Order added successfully'}), 201
        except Exception as e:
            print(f"Error adding order: {e}")
            if connection:
                connection.rollback()
            return jsonify({'message': 'Error adding order'}), 500
        finally:
            if connection:
                connection.close()

    @staticmethod
    def update(order_id, customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks):
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = """
                    UPDATE Orders 
                    SET customer_id = %s, medicine_id = %s, quantity = %s, total = %s, 
                        discount = %s, price_to_pay = %s, balance = %s, remarks = %s 
                    WHERE id = %s
                """
                cursor.execute(query, (customer_id, medicine_id, quantity, total, discount, price_to_pay, balance, remarks, order_id))
            connection.commit()
            return jsonify({'message': 'Order updated successfully'}), 200
        except Exception as e:
            print(f"Error updating order: {e}")
            if connection:
                connection.rollback()
            return jsonify({'message': 'Error updating order'}), 500
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_all():
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Orders")
                orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return jsonify({'message': 'Error fetching orders'}), 500
        finally:
            if connection:
                connection.close()
