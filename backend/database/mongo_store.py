import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.mongo_client import get_mongo_db
from pipeline.data_loader import load_all_data
from pipeline.data_cleaner import clean_data

def store_raw_data(df):
    """Store raw orders data in MongoDB"""
    db = get_mongo_db()
    collection = db['raw_orders']

    # Clear existing data
    collection.drop()

    # Convert to dict and insert
    records = df.head(1000).to_dict('records')  # storing 1000 records (Atlas free tier limit)
    collection.insert_many(records)

    print(f"✅ Stored {len(records)} records in MongoDB!")
    return len(records)

def store_analytics(analytics):
    """Store analytics results in MongoDB"""
    db = get_mongo_db()

    # Store summary
    db['analytics_summary'].drop()
    db['analytics_summary'].insert_one(analytics['summary'])
    print("✅ Summary stored!")

    # Store top categories
    db['top_categories'].drop()
    db['top_categories'].insert_many(analytics['top_categories'].to_dict('records'))
    print("✅ Top categories stored!")

    # Store monthly trend
    db['monthly_trend'].drop()
    db['monthly_trend'].insert_many(analytics['monthly_trend'].to_dict('records'))
    print("✅ Monthly trend stored!")

if __name__ == "__main__":
    from pipeline.analytics import get_analytics

    data = load_all_data()
    df = clean_data(data)

    from models.ml_models import build_features
    monthly_revenue, customer_features = build_features(df)

    analytics = get_analytics(df)
    store_raw_data(df)
    store_analytics(analytics)
    print("\n🎉 All data stored in MongoDB!")