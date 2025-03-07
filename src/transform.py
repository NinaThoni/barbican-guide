import logging
from urllib.parse import urlparse
from dateutil import parser

# ✅ Configure logging to print to terminal only
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Only print to terminal
)

def standardize_date(date_str):
    """Convert date string to YYYY-MM-DD format."""
    try:
        formatted_date = parser.parse(date_str).strftime("%Y-%m-%d")
        return formatted_date
    except Exception:
        logging.warning(f"⚠️ Could not parse date: {date_str}")
        return None  # Handle invalid dates gracefully

def remove_duplicates(events_df):
    """Remove duplicate events while keeping different dates."""
    before_count = len(events_df)
    events_df = events_df.drop_duplicates(subset=["Title", "Description", "Date"], keep="first")
    after_count = len(events_df)
    logging.info(f"✅ Removed {before_count - after_count} duplicate events (keeping different dates).")
    return events_df

def handle_missing_data(events_df):
    """Handle missing values by filling or dropping rows."""
    before_count = len(events_df)
    
    # Drop rows where critical fields (Title, URL) are missing
    events_df.dropna(subset=["Title", "URL"], inplace=True)
    
    # Fill missing non-critical fields with default values
    events_df.fillna({"Category": "Unknown", "Price": "Unknown"}, inplace=True)
    
    after_count = len(events_df)
    logging.info(f"✅ Removed {before_count - after_count} rows with missing critical fields.")
    
    return events_df

def is_valid_url(url):
    """Check if URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)  # Must have scheme (https) and domain

def validate_urls(events_df):
    """Remove rows with invalid URLs."""
    before_count = len(events_df)
    events_df = events_df[events_df["URL"].apply(is_valid_url)]
    after_count = len(events_df)
    logging.info(f"✅ Removed {before_count - after_count} rows with invalid URLs.")
    return events_df

def transform_events(raw_events_df):
    """Clean and structure the extracted events data."""
    logging.info("📌 Transforming data: Standardizing dates...")
    raw_events_df["Date"] = raw_events_df["Date"].apply(standardize_date)

    logging.info("📌 Handling missing data...")
    raw_events_df = handle_missing_data(raw_events_df)

    logging.info("📌 Validating URLs...")
    raw_events_df = validate_urls(raw_events_df)

    logging.info("📌 Removing duplicates while keeping different dates...")
    raw_events_df = remove_duplicates(raw_events_df)

    logging.info(f"🎉 Transformation complete! {len(raw_events_df)} events ready.")
    return raw_events_df
