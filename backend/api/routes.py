from fastapi import APIRouter
from database.mongo_client import get_mongo_db
from database.postgres_client import get_postgres_connection
import pickle
import os

router = APIRouter()

# Load ML models
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

with open(os.path.join(MODEL_PATH, 'churn_model.pkl'), 'rb') as f:
    churn_model = pickle.load(f)

with open(os.path.join(MODEL_PATH, 'revenue_model.pkl'), 'rb') as f:
    revenue_model = pickle.load(f)

@router.get("/analytics/summary")
def get_summary():
    db = get_mongo_db()
    summary = db['analytics_summary'].find_one({}, {'_id': 0})
    return summary

@router.get("/analytics/top-categories")
def get_top_categories():
    db = get_mongo_db()
    categories = list(db['top_categories'].find({}, {'_id': 0}))
    return categories

@router.get("/analytics/monthly-trend")
def get_monthly_trend():
    db = get_mongo_db()
    trend = list(db['monthly_trend'].find({}, {'_id': 0}))
    return trend

@router.get("/analytics/customer-stats")
def get_customer_stats():
    conn = get_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_stats LIMIT 100")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "customer_id": r[1], "order_count": r[2], 
             "avg_spend": r[3], "churned": r[4]} for r in rows]

@router.post("/predict/churn")
def predict_churn(order_count: int, avg_spend: float):
    prediction = churn_model.predict([[order_count, avg_spend]])[0]
    probability = churn_model.predict_proba([[order_count, avg_spend]])[0][1]
    return {
        "churned": bool(prediction),
        "churn_probability": round(float(probability), 2)
    }

@router.post("/predict/revenue")
def predict_revenue(month_number: int):
    prediction = revenue_model.predict([[month_number]])[0]
    return {"predicted_revenue": round(float(prediction), 2)}




from rag.rag_engine import ask_question
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(request: ChatRequest):
    answer = ask_question(request.question)
    return {"question": request.question, "answer": answer}