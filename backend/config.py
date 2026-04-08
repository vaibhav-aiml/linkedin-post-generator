import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    MODEL_NAME = 'distilbert-base-uncased'  # For text analysis
    MAX_POST_LENGTH = 3000
    GENERATION_MODEL = 'gpt-3.5-turbo'  # or use local model
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:5500']