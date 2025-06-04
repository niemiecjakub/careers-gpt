from dotenv import load_dotenv
from agent import Agent

load_dotenv()
Agent().run_conversation_loop()