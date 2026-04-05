import os
from dotenv import load_dotenv

# Load all variables from .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Email Settings
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # (App Password)
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER") # email to receive the report

# Model Settings 
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

# Search Settings
SEARCH_MAX_RESULTS = 7