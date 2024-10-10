import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG


def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def create_tables(connection):
    cursor = connection.cursor()
    create_customer_table = """
    CREATE TABLE IF NOT EXISTS Customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        address VARCHAR(200)
    );
    """

    create_medicine_table = """
CREATE TABLE IF NOT EXISTS Medicine (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    image_path VARCHAR(255)  
);
"""

    create_order_table = """
    CREATE TABLE IF NOT EXISTS Orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        medicine_id INT NOT NULL,
        quantity INT NOT NULL,
        total FLOAT NOT NULL,
        discount FLOAT,
        price_to_pay FLOAT NOT NULL,
        balance FLOAT,
        remarks VARCHAR(200),
        FOREIGN KEY (customer_id) REFERENCES Customer(id),
        FOREIGN KEY (medicine_id) REFERENCES Medicine(id)
    );
    """

    # Execute table creation
    try:
        cursor.execute(create_customer_table)
        cursor.execute(create_medicine_table)
        cursor.execute(create_order_table)
        print("Tables created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


if __name__ == "__main__":
    connection = get_db_connection()
    if connection:
        create_tables(connection)
        connection.close()  # Close the connection when done
