import pymysql
import sys
import os

# Dynamically added the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from scripts.create_schema import connect_db

def create_sales_trends_mart():
    """Creates the sales trends data mart (dm_sales_trends) in MySQL."""
    connection = connect_db()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS dm_sales_trends AS
    SELECT 
        d.year,
        d.month,
        COUNT(DISTINCT f.order_id) AS total_orders,
        SUM(f.price) AS total_revenue,
        SUM(f.freight_value) AS total_shipping_cost
    FROM fact_orders f
    JOIN dim_dates d ON f.purchase_date_id = d.date_id
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month;
    """
    
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    print("dm_sales_trends created successfully!")

if __name__ == "__main__":
    create_sales_trends_mart()