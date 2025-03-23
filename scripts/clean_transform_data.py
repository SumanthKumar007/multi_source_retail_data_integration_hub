import pandas as pd

def clean(df):
    """
    Cleans the merged e-commerce DataFrame by handling missing values, renaming columns, and filling timestamps.
    
    Parameters:
    - df: Merged DataFrame
    
    Returns:
    - Cleaned DataFrame
    """
    # Handle missing reviews
    df['review_comment_title'] = df['review_comment_title'].fillna("Not Available")
    df['review_comment_message'] = df['review_comment_message'].fillna("Not Available")
    
    # Fill missing review scores with mean
    df['review_score'] = df['review_score'].fillna(df['review_score'].mean())
    
    # Fill review creation date with delivery date
    df['review_creation_date'] = df['review_creation_date'].fillna(df['order_delivered_customer_date'].where(df['order_delivered_customer_date'].notna()))
    
    # Replace NaN values with "Unknown" for categorical columns
    df[['payment_type', 'product_category_name', 'product_category_name_english']] = \
        df[['payment_type', 'product_category_name', 'product_category_name_english']].fillna("Unknown")
    
    # Replace NaN values with median values for numerical columns
    num_cols = [
        'payment_sequential', 'payment_installments', 'order_item_id', 'price', 'freight_value', 
        'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    df[num_cols] = df[num_cols].apply(lambda x: x.fillna(x.median()), axis=0)
    
    # Rename misspelled columns
    df = df.rename(columns={
        'product_name_lenght': 'product_name_length',
        'product_description_lenght': 'product_description_length'
    })
    
    # Fill timestamps with relevant values
    df['order_approved_at'] = df['order_approved_at'].fillna(df['order_purchase_timestamp'])
    df['order_delivered_carrier_date'] = df['order_delivered_carrier_date'].fillna(df['order_approved_at'])
    df['order_delivered_customer_date'] = df['order_delivered_customer_date'].fillna(df['order_estimated_delivery_date'])
    
    # Drop remaining null values (~less than 5%)
    df = df.dropna()
    
    print("Cleaning step complete!")
    return df

def convert_dtypes(df):
    """
    Converts data types of the merged DataFrame for optimized memory usage and faster processing.

    Parameters:
    - df: Merged DataFrame

    Returns:
    - DataFrame with updated data types
    """
    
    dtype_mapping = {
        "order_id": "string",
        "customer_id": "string",
        "order_status": "category",
        "order_purchase_timestamp": "datetime64[ns]",
        "order_approved_at": "datetime64[ns]",
        "order_delivered_carrier_date": "datetime64[ns]",
        "order_delivered_customer_date": "datetime64[ns]",
        "order_estimated_delivery_date": "datetime64[ns]",
        "customer_unique_id": "string",
        "customer_zip_code_prefix": "Int32",
        "customer_city": "string",
        "customer_state": "category",
        "payment_sequential": "Int32",
        "payment_type": "category",
        "payment_installments": "Int32",
        "payment_value": "float32",
        "review_id": "string",
        "review_score": "float32",
        "order_item_id": "Int32",
        "product_id": "string",
        "seller_id": "string",
        "shipping_limit_date": "datetime64[ns]",
        "price": "float32",
        "freight_value": "float32",
        "product_category_name": "category",
        "product_name_length": "float32",
        "product_description_length": "float32",
        "product_photos_qty": "float32",
        "product_weight_g": "float32",
        "product_length_cm": "float32",
        "product_height_cm": "float32",
        "product_width_cm": "float32",
        "product_category_name_english": "category",
        "seller_zip_code_prefix": "Int32",
        "seller_city": "string",
        "seller_state": "category",
    }

    # Convert columns safely
    for col, dtype in dtype_mapping.items():
        if col in df.columns:
            if "datetime" in str(dtype):
                df[col] = pd.to_datetime(df[col], errors='coerce')  # Convert dates, set errors to NaT
            elif dtype == "Int32":
                df[col] = pd.to_numeric(df[col], errors="coerce", downcast="integer").astype("Int32")
            else:
                df[col] = df[col].astype(dtype)

    print("Data type conversion complete!")
    return df

