# import os
# import psycopg2
# from dotenv import load_dotenv
# import logging

# # ✅ Configure logging for terminal output
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler()]
# )

# # ✅ Load environment variables
# load_dotenv()

# # ✅ Database credentials (Stored in .env)
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")

# def get_db_connection():
#     """Establish connection to Azure PostgreSQL with SSL."""
#     logging.info(f"🔍 Attempting connection to: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
    
#     try:
#         conn = psycopg2.connect(
#             host=DB_HOST,
#             database=DB_NAME,
#             user=DB_USER,
#             password=DB_PASS,
#             port=5432,
#             sslmode="require"
#         )
#         logging.info("✅ Connected to PostgreSQL")

#         return conn
#     except Exception as e:
#         logging.info(f"❌ Connection failed: {e}")

#         return None

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

# ✅ Validate environment variables BEFORE connecting
if not DB_HOST or DB_HOST.lower() in ["localhost", "127.0.0.1"]:
    logging.error("❌ ERROR: DB_HOST is set to localhost! This script should connect to Azure PostgreSQL.")
    exit(1)

logging.info(f"🔍 Using database connection settings:")
logging.info(f"    DB_HOST={DB_HOST}")
logging.info(f"    DB_NAME={DB_NAME}")
logging.info(f"    DB_USER={DB_USER}")
logging.info(f"    DB_PORT={DB_PORT}")

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
