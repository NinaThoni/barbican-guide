import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Only print to terminal, no file logging
)

# URL of the Barbican Events Page
url = "https://www.barbican.org.uk/whats-on"

def extract_events():
    """Scrape event details from the Barbican website with error handling & logging."""
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Failed to fetch page: {e}")
        return pd.DataFrame(), pd.DataFrame()
    
    event_cards = soup.find_all("div", class_="views-row")

    if not event_cards:
        logging.warning("⚠️ No events found on the page.")
        return pd.DataFrame(), pd.DataFrame()

    all_events = []
    unique_events = {}

    for event in event_cards:
        try:
            # Extract the event date
            event_date = event.get("data-day", "N/A")

            # Extract title
            title_tag = event.find("h2", class_="listing-title listing-title--event")
            title = title_tag.text.strip() if title_tag else "N/A"

            # Extract category
            category_tag = event.find("span", class_="tag__plain")
            category = category_tag.text.strip() if category_tag else "N/A"

            # Extract description
            description_tag = event.find("div", class_="search-listing__intro")
            description = description_tag.get_text(separator=" ").strip() if description_tag else "N/A"

            # Extract pricing
            price_tag = event.find("div", class_="search-listing__label search-listing__label--promoted")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Extract event URL
            link_tag = event.find("a", class_="button button--branded button--inline")
            event_url = f"https://www.barbican.org.uk{link_tag['href']}" if link_tag else "N/A"

            # Store ALL events (with dates) for PostgreSQL
            all_events.append({
                "Date": event_date,
                "Title": title,
                "Category": category,
                "Description": description,
                "Price": price,
                "URL": event_url
            })

            # Store UNIQUE events (without dates) for Vector DB
            unique_key = (title, description)  
            if unique_key not in unique_events:
                unique_events[unique_key] = {
                    "Title": title,
                    "Category": category,
                    "Description": description,
                    "Price": price,
                    "URL": event_url
                }

        except Exception as e:
            logging.error(f"❌ Error processing an event: {e}")

    # Convert lists to DataFrames
    all_events_df = pd.DataFrame(all_events)
    unique_events_df = pd.DataFrame(unique_events.values())

    logging.info(f"✅ Successfully extracted {len(all_events_df)} total events and {len(unique_events_df)} unique events.")

    return all_events_df, unique_events_df

# Run extraction
all_events_df, unique_events_df = extract_events()

print(all_events_df)
