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

def create_views():
    """Creates necessary views in MySQL."""
    connection = connect_db()
    cursor = connection.cursor()

    queries = [
        "DROP VIEW IF EXISTS sales_performance;",
        """
        CREATE VIEW sales_performance AS
        SELECT 
            f.order_id, 
            c.customer_id, 
            c.customer_city, 
            c.customer_state, 
            f.product_id, 
            f.seller_id, 
            f.price, 
            f.freight_value,
            d.date AS order_date
        FROM fact_orders f
        JOIN dim_customers c ON f.customer_id = c.customer_id
        JOIN dim_dates d ON f.purchase_date_id = d.date_id;
        """,

        "DROP VIEW IF EXISTS product_category_analysis;",
        """
        CREATE VIEW product_category_analysis AS
        SELECT 
            p.product_category_name, 
            COUNT(f.order_id) AS total_orders, 
            SUM(f.price) AS total_revenue
        FROM fact_orders f
        JOIN dim_products p ON f.product_id = p.product_id
        GROUP BY p.product_category_name;
        """,
         "DROP VIEW IF EXISTS seller_performance;",
    """
    CREATE VIEW seller_performance AS
    SELECT 
        s.seller_id, 
        s.seller_city, 
        s.seller_state, 
        COUNT(f.order_id) AS total_orders, 
        SUM(f.price) AS total_revenue
    FROM fact_orders f
    JOIN dim_sellers s ON f.seller_id = s.seller_id
    GROUP BY s.seller_id, s.seller_city, s.seller_state;
    """
    ]

    try:
        for query in queries:
            cursor.execute(query)

        connection.commit()
        print("Views created successfully!")

    except pymysql.MySQLError as e:
        print(f"Error creating views: {e}")

    finally:
        cursor.close()
        connection.close()


# **Calls the function when script runs**
if __name__ == "__main__":
    create_views()
