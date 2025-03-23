import pymysql
import sys
import os

# Dynamically added the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from scripts.create_schema import connect_db


def create_sales_performance_mart():
    """Creates the sales performance data mart (dm_sales_performance) in MySQL."""
    connection = connect_db()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS dm_sales_performance AS
    SELECT 
        c.customer_city,
        c.customer_state,
        COUNT(DISTINCT f.order_id) AS total_orders,
        SUM(f.price) AS total_revenue,
        SUM(f.freight_value) AS total_shipping_cost
    FROM fact_orders f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY c.customer_city, c.customer_state;
    """
    
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    print("dm_sales_performance created successfully!")

if __name__ == "__main__":
    create_sales_performance_mart()
