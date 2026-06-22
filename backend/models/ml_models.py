import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pipeline.data_loader import load_all_data
from pipeline.data_cleaner import clean_data

def build_features(df):
    """Engineer features for ML models"""

    # Monthly revenue
    monthly_revenue = df.groupby(['year', 'month'])['payment_value'].sum().reset_index()
    monthly_revenue.columns = ['year', 'month', 'total_revenue']

    # Customer purchase frequency
    customer_orders = df.groupby('customer_unique_id')['order_id'].nunique().reset_index()
    customer_orders.columns = ['customer_unique_id', 'order_count']

    # Average order value per customer
    customer_spend = df.groupby('customer_unique_id')['payment_value'].mean().reset_index()
    customer_spend.columns = ['customer_unique_id', 'avg_spend']

    # Merge customer features
    customer_features = customer_orders.merge(customer_spend, on='customer_unique_id')

    # Churn label — customers who ordered only once = churned
    customer_features['churned'] = (customer_features['order_count'] == 1).astype(int)

    print(f"✅ Features built!")
    print(f"Monthly revenue shape: {monthly_revenue.shape}")
    print(f"Customer features shape: {customer_features.shape}")
    print(f"Churn rate: {customer_features['churned'].mean():.2%}")

    return monthly_revenue, customer_features

def train_churn_model(customer_features):
    """Train customer churn prediction model"""

    X = customer_features[['order_count', 'avg_spend']]
    y = customer_features['churned']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"✅ Churn Model Accuracy: {accuracy:.2%}")

    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'churn_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ Churn model saved!")

    return model, accuracy

def train_revenue_model(monthly_revenue):
    """Train monthly revenue forecasting model"""

    monthly_revenue['month_number'] = (
        (monthly_revenue['year'] - monthly_revenue['year'].min()) * 12 + 
        monthly_revenue['month']
    )

    X = monthly_revenue[['month_number']]
    y = monthly_revenue['total_revenue']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"✅ Revenue Model - MAE: R${mae:,.2f}, R2 Score: {r2:.2f}")

    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'revenue_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ Revenue model saved!")

    return model, mae, r2

if __name__ == "__main__":
    data = load_all_data()
    df = clean_data(data)
    monthly_revenue, customer_features = build_features(df)
    churn_model, accuracy = train_churn_model(customer_features)
    revenue_model, mae, r2 = train_revenue_model(monthly_revenue)
    print("\n🎉 All models trained and saved!")