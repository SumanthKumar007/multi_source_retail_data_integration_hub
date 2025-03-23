import pymysql

def connect_db():
    """Establish connection to MySQL database."""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="Project_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def create_aggregation_tables():
    """Creates aggregation tables in MySQL."""
    queries = [
        """CREATE TABLE IF NOT EXISTS total_sales_by_customer AS
           SELECT f.customer_id, COUNT(f.order_id) AS total_orders, SUM(f.price) AS total_revenue
           FROM fact_orders f GROUP BY f.customer_id;""",
           
        """CREATE TABLE IF NOT EXISTS revenue_by_category AS
           SELECT p.product_category_name, SUM(f.price) AS total_revenue
           FROM fact_orders f JOIN dim_products p ON f.product_id = p.product_id
           GROUP BY p.product_category_name;""",
           
        """CREATE TABLE IF NOT EXISTS monthly_sales_summary AS
           SELECT d.year, d.month, COUNT(f.order_id) AS total_orders, SUM(f.price) AS total_revenue
           FROM fact_orders f JOIN dim_dates d ON f.purchase_date_id = d.date_id
           GROUP BY d.year, d.month;""",

        """CREATE TABLE IF NOT EXISTS daily_sales_summary AS
           SELECT d.date, COUNT(f.order_id) AS total_orders, SUM(f.price) AS total_revenue
           FROM fact_orders f JOIN dim_dates d ON f.purchase_date_id = d.date_id
           GROUP BY d.date;"""
    ]

    try:
        conn = connect_db()
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
        print("Aggregation tables created successfully!")
    except Exception as e:
        print(f"Error creating aggregation tables: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_aggregation_tables()
