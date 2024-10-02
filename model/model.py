import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Create a database connection to a MySQL database """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',            # Change if needed
            user='root',        # Replace with your MySQL username
            password='Ijse@1234',    # Replace with your MySQL password
            database='mediPro' # Replace with your database name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_tables(connection):
    """ Create tables in the MySQL database """
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
        quantity INT NOT NULL
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

# Usage
if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_tables(connection)
        connection.close()  # Close the connection when done
