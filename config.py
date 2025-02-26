from dotenv import load_dotenv
import os

load_dotenv()
# DB_URL=os.environ.get("DB_URL")
# ALGORITHM=os.environ.get("ALGORITHM")
# SECRET_KEY=os.environ.get("SECRET_KEY")

DB_URL = os.getenv("DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
