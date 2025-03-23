import pymysql
import sys
import os

# Dynamically added the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from scripts.create_schema import connect_db

def create_product_analysis_mart():
    """Creates the product category analysis data mart (dm_product_category_analysis) in MySQL."""
    connection = connect_db()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS dm_product_category_analysis AS
    SELECT 
        p.product_category_name,
        COUNT(DISTINCT f.order_id) AS total_orders,
        SUM(f.price) AS total_revenue,
        SUM(f.freight_value) AS total_shipping_cost,
        AVG(p.product_weight_g) AS avg_weight_g,
        AVG(p.product_length_cm) AS avg_length_cm,
        AVG(p.product_height_cm) AS avg_height_cm,
        AVG(p.product_width_cm) AS avg_width_cm
    FROM fact_orders f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.product_category_name;
    """
    
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    print("dm_product_category_analysis created successfully!")

if __name__ == "__main__":
    create_product_analysis_mart()
