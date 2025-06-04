import os
from dotenv import load_dotenv
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

load_dotenv()

vn = MyVanna(config={
    'api_key': os.getenv("OPENAI_API_KEY"), 
    'model': os.getenv("CHAT_MODEL_ID"),
})

vn.connect_to_postgres(
    host=os.getenv("DB_HOST"), 
    dbname=os.getenv("DB_DBNAME"),
    user=os.getenv("DB_USER") ,
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)


vn.get_training_data()