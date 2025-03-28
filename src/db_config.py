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

def get_db_connection():
    """Establish connection to Azure PostgreSQL with SSL."""
    
    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            sslmode="require" 
        )
        logging.info("✅ Connected to PostgreSQL")

        return conn
    except Exception as e:
        logging.error("❌ Connection failed", exc_info=True)
        return None


