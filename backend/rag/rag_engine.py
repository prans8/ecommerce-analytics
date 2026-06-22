import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from database.mongo_client import get_mongo_db

def get_business_context():
    """Fetch analytics data from MongoDB to use as context"""
    db = get_mongo_db()
    
    summary = db['analytics_summary'].find_one({}, {'_id': 0})
    categories = list(db['top_categories'].find({}, {'_id': 0}))
    trend = list(db['monthly_trend'].find({}, {'_id': 0}))

    context = f"""
    You are an AI business analyst for an e-commerce company. 
    Here is the current business data:
    
    SUMMARY:
    - Total Orders: {summary['total_orders']:,}
    - Total Revenue: R${summary['total_revenue']:,.2f}
    - Average Order Value: R${summary['avg_order_value']:.2f}
    - Average Review Score: {summary['avg_review_score']:.2f}/5
    - Average Delivery Days: {summary['avg_delivery_days']:.1f} days
    - Total Customers: {summary['total_customers']:,}
    - Total Sellers: {summary['total_sellers']:,}
    
    TOP 10 CATEGORIES BY REVENUE:
    {chr(10).join([f"- {c['category']}: R${c['revenue']:,.2f}" for c in categories])}
    
    MONTHLY REVENUE TREND:
{chr(10).join([f"- {t['period']}: R${t['payment_value']:,.2f}" for t in trend])}
    
    Answer questions based on this data. Be concise and insightful.
    """
    return context

def ask_question(question: str) -> str:
    """Ask a question about the business data"""
   llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)
    
    context = get_business_context()
    
    messages = [
        SystemMessage(content=context),
        HumanMessage(content=question)
    ]
    
    response = llm.invoke(messages)
    return response.content

if __name__ == "__main__":
    print("Testing RAG engine...")
    answer = ask_question("Which product category has the highest revenue?")
    print(f"Answer: {answer}")
    
    answer2 = ask_question("What is the average order value and what does it tell us?")
    print(f"\nAnswer 2: {answer2}")