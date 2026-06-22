import pandas as pd
import os

# Path to data folder
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_all_data():
    """Load all CSV files into dataframes"""
    
    orders = pd.read_csv(os.path.join(DATA_PATH, 'olist_orders_dataset.csv'))
    customers = pd.read_csv(os.path.join(DATA_PATH, 'olist_customers_dataset.csv'))
    order_items = pd.read_csv(os.path.join(DATA_PATH, 'olist_order_items_dataset.csv'))
    payments = pd.read_csv(os.path.join(DATA_PATH, 'olist_order_payments_dataset.csv'))
    reviews = pd.read_csv(os.path.join(DATA_PATH, 'olist_order_reviews_dataset.csv'))
    products = pd.read_csv(os.path.join(DATA_PATH, 'olist_products_dataset.csv'))
    sellers = pd.read_csv(os.path.join(DATA_PATH, 'olist_sellers_dataset.csv'))
    category_translation = pd.read_csv(os.path.join(DATA_PATH, 'product_category_name_translation.csv'))

    print("✅ All datasets loaded successfully!")
    print(f"Orders: {orders.shape}")
    print(f"Customers: {customers.shape}")
    print(f"Order Items: {order_items.shape}")
    print(f"Payments: {payments.shape}")
    print(f"Reviews: {reviews.shape}")
    print(f"Products: {products.shape}")
    print(f"Sellers: {sellers.shape}")

    return {
        'orders': orders,
        'customers': customers,
        'order_items': order_items,
        'payments': payments,
        'reviews': reviews,
        'products': products,
        'sellers': sellers,
        'category_translation': category_translation
    }

if __name__ == "__main__":
    data = load_all_data()