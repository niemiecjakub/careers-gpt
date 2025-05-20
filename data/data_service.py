from init_database import InitDatabase

def initialize_db():
    db = InitDatabase(r'C:\Users\komputerek\Desktop\dev\all_reviews.csv')
    db.initialize_tables()
    db.insert_employment_statuses()
    db.insert_companies()
    db.insert_opinions()
    db.insert_reviews()
    
    
initialize_db()

