import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for sessions & JWT
    SECRET_KEY = os.environ.get('SECRET_KEY', 'faculty-connect-int335-lpu-secret-key-2026')
    
    # Database: Supports SQLite (out-of-the-box local zero-config) or MySQL
    # e.g., DATABASE_URL=mysql+pymysql://root:password@localhost:3306/faculty_connect
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "faculty_connect.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 3-Hour Automatic AI Answer threshold in hours (configurable; default 3)
    AI_ANSWER_DELAY_HOURS = float(os.environ.get('AI_ANSWER_DELAY_HOURS', '3.0'))
    
    # Duplicate Detection Semantic Threshold (0.0 to 1.0; default 0.60)
    DUPLICATE_SIMILARITY_THRESHOLD = float(os.environ.get('DUPLICATE_SIMILARITY_THRESHOLD', '0.60'))
    
    # AI Engine API Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'fallback') # 'gemini', 'openai', or 'fallback'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
