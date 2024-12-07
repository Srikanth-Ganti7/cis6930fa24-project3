import pytest
import pandas as pd
from app.utils import fetch_incidents, split_line_regex, extract_incidents, preprocess_dataframe

def test_split_line_regex():
    line = "2023-01-01 12:00:00  123456  Some Location  Some Nature  ORI123"
    expected = ["2023-01-01 12:00:00", "123456", "Some Location", "Some Nature", "ORI123"]
    assert split_line_regex(line) == expected

def test_fetch_incidents_real_pdf():
    # Use the real PDF URL for testing
    url = "https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-01_daily_incident_summary.pdf"
    pdf_path = fetch_incidents(url)

    # Check if the file was downloaded correctly
    assert pdf_path == "../incident_report.pdf"
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()
    assert pdf_content.startswith(b"%PDF")  # Ensure it's a valid PDF file

def test_extract_incidents_real_pdf():
    # Extract incidents from the real PDF
    pdf_file_path = "../incident_report.pdf"
    incidents_df = extract_incidents(pdf_file_path)

    # Check if the DataFrame is populated and has the correct columns
    assert not incidents_df.empty
    assert list(incidents_df.columns) == ['date_time', 'incident_number', 'location', 'nature', 'incident_ori']

def test_preprocess_dataframe():
    data = {
        'date_time': ["2023-01-01 12:00:00", "2023-01-02 18:00:00", "invalid_date"],
        'incident_number': ["123456", "789012", "345678"],
        'location': ["Location1", "Location2", "Location3"],
        'nature': ["Nature1", "Nature2", "Nature3"],
        'incident_ori': ["ORI123", "ORI456", "ORI789"]
    }
    df = pd.DataFrame(data)
    processed_df = preprocess_dataframe(df)

    # Check if preprocessing added the required columns and handled invalid dates
    assert 'time_of_day' in processed_df.columns
    assert 'date_time_encoded' in processed_df.columns
    assert processed_df['time_of_day'].iloc[0] == 'afternoon'
    assert processed_df['time_of_day'].iloc[1] == 'evening'
    assert len(processed_df) == 2  # Invalid date row should be dropped
