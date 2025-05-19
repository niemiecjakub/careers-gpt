from db_models import Company, Review
from dotenv import load_dotenv
import ollama
from  database import SessionLocal
import os

def initialize_db():
    from init_database import InitDatabase
    db = InitDatabase(r'C:\Users\komputerek\Desktop\dev\all_reviews.csv')
    db.insert_employment_statuses()
    db.insert_companies()
    db.insert_reviews()
    
    
load_dotenv()   

session = SessionLocal()
review = session.query(Review).filter_by(id=32974).first()
company = session.query(Company).filter_by(id=review.company_id).first()
review_summary = f"""** {review.review_title} **
Company: {company.name}
Job title: {review.job_title}  
+ Pros: {review.pros}
- Cons: {review.cons}
"""
print(review_summary)

embeding_model = os.getenv("OLLAMA_EMBEDDING_MODEL") 
embedding = ollama.embed(
    model= embeding_model, 
    input= review_summary)
print(embedding.embeddings)

