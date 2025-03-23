import pymysql

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "Project_db"
}

def connect_db():
    """Establishes connection with MySQL."""
    return pymysql.connect(**DB_CONFIG)

def create_star_schema():
    """It will Creates the database and the required tables for the star schema in MySQL."""
    connection = connect_db()
    cursor = connection.cursor()

    # Ensure database exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS Project_db;")
    cursor.execute("USE Project_db;") 

    queries = [
        #1. It will Create dimension tables FIRST
        """
        CREATE TABLE IF NOT EXISTS dim_customers (
            customer_id VARCHAR(45) PRIMARY KEY,
            customer_unique_id VARCHAR(45),
            customer_zip_code_prefix INT,
            customer_city VARCHAR(100),
            customer_state VARCHAR(10)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_products (
            product_id VARCHAR(45) PRIMARY KEY,
            product_category_name VARCHAR(255),
            product_name_length FLOAT,
            product_description_length FLOAT,
            product_photos_qty FLOAT,
            product_weight_g FLOAT,
            product_length_cm FLOAT,
            product_height_cm FLOAT,
            product_width_cm FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_sellers (
            seller_id VARCHAR(45) PRIMARY KEY,
            seller_zip_code_prefix INT,
            seller_city VARCHAR(100),
            seller_state VARCHAR(10)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_dates (
            date_id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE UNIQUE NOT NULL,
            year INT NOT NULL,
            month INT NOT NULL,
            day INT NOT NULL,
            weekday VARCHAR(10) NOT NULL
        );
        """,
        #2. It will Create fact table AFTER dimension tables
        """
        CREATE TABLE IF NOT EXISTS fact_orders (
            order_id VARCHAR(45) PRIMARY KEY,
            customer_id VARCHAR(45),
            order_status VARCHAR(50),
            purchase_date_id INT,
            approved_date_id INT,
            delivered_carrier_date_id INT,
            delivered_customer_date_id INT,
            estimated_delivery_date_id INT,
            product_id VARCHAR(45),
            seller_id VARCHAR(45),
            price FLOAT,
            freight_value FLOAT,
            FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
            FOREIGN KEY (purchase_date_id) REFERENCES dim_dates(date_id),
            FOREIGN KEY (approved_date_id) REFERENCES dim_dates(date_id),
            FOREIGN KEY (delivered_carrier_date_id) REFERENCES dim_dates(date_id),
            FOREIGN KEY (delivered_customer_date_id) REFERENCES dim_dates(date_id),
            FOREIGN KEY (estimated_delivery_date_id) REFERENCES dim_dates(date_id),
            FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
            FOREIGN KEY (seller_id) REFERENCES dim_sellers(seller_id)
        );
        """,
        #3. It will Create `dim_payments` AFTER `fact_orders`
        """
        CREATE TABLE IF NOT EXISTS dim_payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(45),
            payment_type VARCHAR(50),
            payment_installments INT,
            payment_value FLOAT,
            FOREIGN KEY (order_id) REFERENCES fact_orders(order_id) ON DELETE CASCADE
        );
        """
    ]

    # Executing Query
    for query in queries:
        cursor.execute(query)
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Star schema created successfully!")

if __name__ == "__main__":
    create_star_schema()
