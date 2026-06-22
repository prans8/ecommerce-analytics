import pandas as pd
import numpy as np
from pipeline.data_loader import load_all_data

def clean_data(data):
    """Clean and merge all datasets"""
    
    orders = data['orders'].copy()
    customers = data['customers'].copy()
    order_items = data['order_items'].copy()
    payments = data['payments'].copy()
    reviews = data['reviews'].copy()
    products = data['products'].copy()
    category_translation = data['category_translation'].copy()

    # Convert date columns to datetime
    date_cols = ['order_purchase_timestamp', 'order_approved_at',
                 'order_delivered_carrier_date', 'order_delivered_customer_date',
                 'order_estimated_delivery_date']
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])

    # Drop rows with missing delivery dates
    orders.dropna(subset=['order_delivered_customer_date'], inplace=True)

    # Add useful time features
    orders['year'] = orders['order_purchase_timestamp'].dt.year
    orders['month'] = orders['order_purchase_timestamp'].dt.month
    orders['day_of_week'] = orders['order_purchase_timestamp'].dt.dayofweek
    orders['delivery_days'] = (
        orders['order_delivered_customer_date'] - 
        orders['order_purchase_timestamp']
    ).dt.days

    # Translate product categories to English
    products = products.merge(category_translation, on='product_category_name', how='left')

    # Build master dataframe
    df = orders.merge(customers, on='customer_id', how='left')
    df = df.merge(order_items, on='order_id', how='left')
    df = df.merge(payments, on='order_id', how='left')
    df = df.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')
    df = df.merge(products[['product_id', 'product_category_name_english']], 
                  on='product_id', how='left')

    # Drop nulls
    df.dropna(subset=['payment_value', 'review_score'], inplace=True)

    print(f"✅ Data cleaned successfully!")
    print(f"Final dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    return df

if __name__ == "__main__":
    data = load_all_data()
    df = clean_data(data)
    print(df.head())