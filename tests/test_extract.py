import pandas as pd
from extract import extract_events

def test_extracted_data():
    """Test that extracted data is in the correct format."""
    all_events_df, unique_events_df = extract_events()

    # Check that it's returning DataFrames
    assert isinstance(all_events_df, pd.DataFrame)
    assert isinstance(unique_events_df, pd.DataFrame)

    # Check that the data is not empty (fails if website structure changes)
    assert not all_events_df.empty, "❌ Extracted events are empty!"

    # Check that required columns exist
    expected_columns = {"Date", "Title", "Category", "Description", "Price", "URL"}
    assert expected_columns.issubset(set(all_events_df.columns)), "❌ Missing expected columns!"

    # Check that URLs are valid
    assert all_events_df["URL"].str.startswith("https://www.barbican.org.uk").all(), "❌ Some URLs are incorrect!"

