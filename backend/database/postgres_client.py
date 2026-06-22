import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_postgres_connection():
    conn = psycopg2.connect(os.getenv("POSTGRESQL_URL"))
    return conn

def create_tables():
    """Create tables for storing processed analytics"""
    conn = get_postgres_connection()
    cursor = conn.cursor()

    # Monthly revenue table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_revenue (
            id SERIAL PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            total_revenue FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Customer stats table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_stats (
            id SERIAL PRIMARY KEY,
            customer_unique_id VARCHAR(255),
            order_count INTEGER,
            avg_spend FLOAT,
            churned INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ML predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ml_predictions (
            id SERIAL PRIMARY KEY,
            prediction_type VARCHAR(50),
            input_data JSONB,
            prediction FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ PostgreSQL tables created!")

if __name__ == "__main__":
    create_tables()