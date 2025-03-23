from scripts.extract_data import extract
from scripts.merge_data import merge_data
from scripts.clean_transform_data import clean, convert_dtypes
from scripts.create_schema import create_star_schema
from scripts.load_data import load_data

def main():
    """Main function to execute the ETL pipeline."""
    print("Extracting data...")
    extract()  # Extracts the data
    
    print("Merging data...")
    merged_df = merge_data()  # Merges data

    print(merged_df[['product_category_name', 'product_category_name_english']].drop_duplicates().head(20))

    
    print("Cleaning data...")
    cleaned_df = clean(merged_df)  # Cleans data
    
    print("Converting data types...")
    final_df = convert_dtypes(cleaned_df)  # Converts data types
    
    print("Creating star schema...")
    create_star_schema()  # Creates the database schema
    
    print("Loading data into MySQL...")
    load_data(final_df)  # Inserts data into the database
    
    print("ETL pipeline completed successfully!")
    print(final_df.head())

if __name__ == "__main__":
    main()
