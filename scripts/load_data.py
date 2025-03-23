import pymysql
import pandas as pd
from scripts.create_schema import connect_db

def load_data(df):
    """Inserts data into the MySQL database using INSERT IGNORE."""
    connection = connect_db()
    cursor = connection.cursor()
    
    # Ensure the correct database is being used
    cursor.execute("USE Project_db;")

    # Insert customers
    customers = df[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']].drop_duplicates()
    for _, row in customers.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO dim_customers VALUES (%s, %s, %s, %s, %s);
        """, tuple(row))

    # Insert products
    products = df[['product_id', 'product_category_name_english', 'product_name_length', 'product_description_length', 
                   'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']].drop_duplicates()
    # Ensure column names match the database table
    products = products.rename(columns={'product_category_name_english': 'product_category_name'})

    for _, row in products.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO dim_products VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, tuple(row))

    # Insert sellers
    sellers = df[['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state']].drop_duplicates()
    for _, row in sellers.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO dim_sellers VALUES (%s, %s, %s, %s);
        """, tuple(row))

    # Insert payment details
    payments = df[['order_id', 'payment_type', 'payment_installments', 'payment_value']].drop_duplicates()
    for _, row in payments.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO dim_payments (order_id, payment_type, payment_installments, payment_value) 
            VALUES (%s, %s, %s, %s);
        """, tuple(row))

    # Extract unique dates from all timestamp columns
    date_columns = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date'
    ]
    
    unique_dates = pd.concat([df[col].dropna().dt.date for col in date_columns]).drop_duplicates().sort_values()

    # Insert unique dates into dim_dates
    for date in unique_dates:
        cursor.execute("""
            INSERT IGNORE INTO dim_dates (date, year, month, day, weekday)
            VALUES (%s, %s, %s, %s, %s);
        """, (date, date.year, date.month, date.day, date.strftime("%A")))

    # Fetch all date mappings from dim_dates in one query
    cursor.execute("SELECT date, date_id FROM dim_dates;")
    date_mapping = {str(row[0]): row[1] for row in cursor.fetchall()}  # Dictionary: {"YYYY-MM-DD": date_id}
    
    print("Date mapping:", date_mapping)  # Debugging step

    # Function to get date_id from dim_dates (faster lookup)
    def get_date_id(date):
        if pd.isna(date):
            return None
        return date_mapping.get(str(date.date()), None)  # Convert to string "YYYY-MM-DD"

    # Insert orders (fact table)
    orders = df[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date', 
                 'product_id', 'seller_id', 'price', 'freight_value']]
    
    # Insert orders into fact_orders with foreign key references
    for _, row in orders.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO fact_orders (
                order_id, customer_id, order_status, purchase_date_id, approved_date_id, 
                delivered_carrier_date_id, delivered_customer_date_id, estimated_delivery_date_id, 
                product_id, seller_id, price, freight_value
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            row['order_id'], row['customer_id'], row['order_status'], 
            get_date_id(row['order_purchase_timestamp']),
            get_date_id(row['order_approved_at']),
            get_date_id(row['order_delivered_carrier_date']),
            get_date_id(row['order_delivered_customer_date']),
            get_date_id(row['order_estimated_delivery_date']),
            row['product_id'], row['seller_id'], row['price'], row['freight_value']
        ))

    connection.commit()
    cursor.close()
    connection.close()
    print("Data inserted successfully!")
