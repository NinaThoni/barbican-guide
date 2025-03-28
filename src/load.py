import logging
import psycopg2
# from db_config import get_db_connection
from src.db_config import get_db_connection


# ✅ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def insert_events(events_df):
    """Insert cleaned events into PostgreSQL database using UPSERT."""
    conn = get_db_connection()
    if not conn:
        logging.error("❌ Database connection failed. Aborting insert.")
        return

    insert_query = """
    INSERT INTO barbican_events (title, description, category, price, event_date, url)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """

    try:
        with conn.cursor() as cur:
            batch_data = [tuple(row) for row in events_df[["Title", "Description", "Category", "Price", "Date", "URL"]].values]
            cur.executemany(insert_query, batch_data)
            conn.commit()
            logging.info(f"✅ Inserted {len(batch_data)} events into database.")
    except Exception as e:
        logging.error(f"❌ Failed to insert events: {e}")
    finally:
        conn.close()






