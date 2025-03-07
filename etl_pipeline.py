import logging
from src.extract import extract_events
from src.transform import transform_events
from src.load import insert_events
from src.db_config import get_db_connection
import sys

# ✅ Configure logging for terminal output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def run_pipeline():
    """End-to-end ETL pipeline: Extract → Transform → Load"""
    logging.info("🚀 Starting Barbican Events ETL Pipeline")

    # ✅ Step 1: Extract
    logging.info("📌 Extracting events from Barbican website...")
    try:
        all_events_df, _ = extract_events()
        logging.info(f"✅ Extracted {len(all_events_df)} events.")
    except Exception as e:
        logging.error(f"❌ Extraction failed: {e}")
        return

    # ✅ Step 2: Transform
    logging.info("📌 Transforming extracted events...")
    try:
        cleaned_events_df = transform_events(all_events_df)
        logging.info(f"✅ Transformed {len(cleaned_events_df)} events.")
    except Exception as e:
        logging.error(f"❌ Transformation failed: {e}")
        return

# ✅ Step 3: Load (Insert into PostgreSQL)
    logging.info("📌 Loading events into PostgreSQL...")
    conn = get_db_connection()
    if not conn:
        logging.error("❌ Database connection failed.")
        sys.exit(1)  

    try:
        insert_events(cleaned_events_df, conn)
        logging.info("🎉 Data successfully inserted into PostgreSQL!")
    except Exception as e:
        logging.error(f"❌ Data loading failed: {e}")
        sys.exit(1)  
    finally:
        conn.close()

if __name__ == "__main__":
    run_pipeline()
