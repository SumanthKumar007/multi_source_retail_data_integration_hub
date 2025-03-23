import pandas as pd

def merge_data():
    """Merges multiple CSV files into a single dataset and returns the DataFrame."""
    
    # Load CSV files
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    #geolocation = pd.read_csv("data/olist_geolocation_dataset.csv")
    order_items = pd.read_csv("data/olist_order_items_dataset.csv")
    order_payments = pd.read_csv("data/olist_order_payments_dataset.csv")
    order_reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    products = pd.read_csv("data/olist_products_dataset.csv")
    sellers = pd.read_csv("data/olist_sellers_dataset.csv")
    category_translation = pd.read_csv("data/product_category_name_translation.csv")

    # Merge customers with orders
    df = orders.merge(customers, on="customer_id", how="left")

    # Merge order payments
    df = df.merge(order_payments, on="order_id", how="left")

    # Merge order reviews
    df = df.merge(order_reviews, on="order_id", how="left")

    # Merge order items
    df = df.merge(order_items, on="order_id", how="left")

    # Merge products
    df = df.merge(products, on="product_id", how="left")

    # Merge product category translations
    df = df.merge(category_translation, on="product_category_name", how="left")

    # Merge sellers
    df = df.merge(sellers, on="seller_id", how="left")

    print("Merging complete! Returning the merged DataFrame.")

    return df  # Returning the merged DataFrame
