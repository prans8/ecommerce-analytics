import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pipeline.data_loader import load_all_data
from pipeline.data_cleaner import clean_data

def get_analytics(df):
    """Generate key business insights"""

    # Top 10 product categories by revenue
    top_categories = (
        df.groupby('product_category_name_english')['payment_value']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_categories.columns = ['category', 'revenue']

    # Monthly revenue trend
    monthly_trend = (
        df.groupby(['year', 'month'])['payment_value']
        .sum()
        .reset_index()
    )
    monthly_trend['period'] = monthly_trend['year'].astype(str) + '-' + monthly_trend['month'].astype(str).str.zfill(2)

    # Average review score by category
    avg_review = (
        df.groupby('product_category_name_english')['review_score']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    # Average delivery days by state
    avg_delivery = (
        df.groupby('customer_state')['delivery_days']
        .mean()
        .sort_values()
        .reset_index()
    )

    # Total summary stats
    summary = {
        'total_orders': int(df['order_id'].nunique()),
        'total_revenue': float(df['payment_value'].sum()),
        'avg_order_value': float(df['payment_value'].mean()),
        'avg_review_score': float(df['review_score'].mean()),
        'avg_delivery_days': float(df['delivery_days'].mean()),
        'total_customers': int(df['customer_unique_id'].nunique()),
        'total_sellers': int(df['seller_id'].nunique()),
    }

    print("✅ Analytics generated!")
    print(f"Total Revenue: R${summary['total_revenue']:,.2f}")
    print(f"Total Orders: {summary['total_orders']:,}")
    print(f"Avg Order Value: R${summary['avg_order_value']:.2f}")
    print(f"Avg Review Score: {summary['avg_review_score']:.2f}/5")
    print(f"Avg Delivery Days: {summary['avg_delivery_days']:.1f} days")
    print(f"\nTop 5 Categories:")
    print(top_categories.head())

    return {
        'summary': summary,
        'top_categories': top_categories,
        'monthly_trend': monthly_trend,
        'avg_review': avg_review,
        'avg_delivery': avg_delivery
    }

if __name__ == "__main__":
    data = load_all_data()
    df = clean_data(data)
    analytics = get_analytics(df)