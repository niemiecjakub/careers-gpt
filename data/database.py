import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

host=os.getenv("DB_HOST")
dbname=os.getenv("DB_DBNAME")
user=os.getenv("DB_USER") 
password=os.getenv("DB_PASSWORD")
port=os.getenv("DB_PORT")
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()