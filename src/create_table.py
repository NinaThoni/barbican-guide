from db_config import get_db_connection

def create_events_table():
    """Create events table in Azure PostgreSQL if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS barbican_events (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        price TEXT,
        event_date DATE NOT NULL,
        url TEXT NOT NULL,
        inserted_at TIMESTAMP DEFAULT NOW()
    );
    """

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                print("✅ Table 'barbican_events' is ready.")
        except Exception as e:
            print(f"❌ Failed to create table: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    create_events_table()
