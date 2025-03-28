import os
import psycopg2
from dotenv import load_dotenv
import logging

# ✅ Configure logging for terminal output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# ✅ Load environment variables
load_dotenv()

# ✅ Database credentials (Stored in .env)
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default to 5432 if not set


def get_db_connection():
    """Establish connection to Azure PostgreSQL with SSL."""
    logging.info(f"🔍 Attempting connection to: {DB_HOST}:{DB_PORT}")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,  # ✅ Include port
            sslmode="require"
        )
        logging.info("✅ Connected to PostgreSQL")

        return conn
    except Exception as e:
        logging.error("❌ Connection failed", exc_info=True)
        return None


