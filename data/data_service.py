from database import engine
from db_models import Base
from init_database import InitDatabase

# Create tables
Base.metadata.create_all(bind=engine)

db = InitDatabase(r'C:\Users\komputerek\Desktop\dev\all_reviews.csv')
db.insert_reviews()