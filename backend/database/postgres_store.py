import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.postgres_client import get_postgres_connection
from pipeline.data_loader import load_all_data
from pipeline.data_cleaner import clean_data
from models.ml_models import build_features

def store_monthly_revenue(monthly_revenue):
    conn = get_postgres_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM monthly_revenue")

    for _, row in monthly_revenue.iterrows():
        cursor.execute("""
            INSERT INTO monthly_revenue (year, month, total_revenue)
            VALUES (%s, %s, %s)
        """, (int(row['year']), int(row['month']), float(row['total_revenue'])))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Stored {len(monthly_revenue)} monthly revenue records!")

def store_customer_stats(customer_features):
    conn = get_postgres_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customer_stats")

    for _, row in customer_features.head(500).iterrows():
        cursor.execute("""
            INSERT INTO customer_stats 
            (customer_unique_id, order_count, avg_spend, churned)
            VALUES (%s, %s, %s, %s)
        """, (
            str(row['customer_unique_id']),
            int(row['order_count']),
            float(row['avg_spend']),
            int(row['churned'])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Stored 500 customer stats records!")

if __name__ == "__main__":
    data = load_all_data()
    df = clean_data(data)
    monthly_revenue, customer_features = build_features(df)
    store_monthly_revenue(monthly_revenue)
    store_customer_stats(customer_features)
    print("\n🎉 All data stored in PostgreSQL!")