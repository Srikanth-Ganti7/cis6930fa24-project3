import re
import urllib.request
from pypdf import PdfReader
import pandas as pd
import logging

from urllib.error import HTTPError, URLError

def fetch_incidents(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    try:
        # Attempt to fetch the URL
        response = urllib.request.urlopen(req)
        print(f"Response status: {response.status}")

        pdf_data = response.read()
        print(f"Downloaded PDF size: {len(pdf_data)} bytes")

        # Save the file locally
        pdf_path = '../incident_report.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf_data)

        return pdf_path

    except HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
        raise Exception(f"Failed to fetch PDF. HTTP Error {e.code}: {e.reason}")
    except URLError as e:
        print(f"URLError: {e.reason}")
        raise Exception(f"Failed to fetch PDF. URL Error: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error occurred: {e}")



def split_line_regex(line):
    parts = re.split(r"\s{2,}", line)
    return [part.strip() for part in parts]

def extract_incidents(pdf_file_path):
    incidents = []
    reader = PdfReader(pdf_file_path)
    first_page = True

    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        if text:
            lines = text.split('\n')
            if first_page:
                lines = lines[2:]
                first_page = False
            for line in lines:
                fields = split_line_regex(line)
                if len(fields) == 5:
                    incidents.append({
                        'date_time': fields[0],
                        'incident_number': fields[1],
                        'location': fields[2],
                        'nature': fields[3],
                        'incident_ori': fields[4]
                    })
                else:
                    logging.info(f"Skipped line (incomplete): {line}")
    return pd.DataFrame(incidents, columns=['date_time', 'incident_number', 'location', 'nature', 'incident_ori'])


from sklearn.preprocessing import LabelEncoder

def preprocess_dataframe(df):
    """
    Ensures all necessary columns are created and handles missing or invalid data gracefully.
    Converts date_time column to datetime format and encodes time of day as a new column.
    """
    le = LabelEncoder()

    # Ensure 'date_time' is a valid datetime field
    if 'date_time' in df.columns:
        df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')  # Convert to datetime
        df.dropna(subset=['date_time'], inplace=True)  # Drop rows with invalid dates

        # Create time of day categories
        df['time_of_day'] = df['date_time'].apply(
            lambda x: 'morning' if 5 <= x.hour < 12 else 
                      'afternoon' if 12 <= x.hour < 17 else 
                      'evening' if 17 <= x.hour < 21 else 'night'
        )

        # Encode time of day categories
        df['date_time_encoded'] = le.fit_transform(df['time_of_day'])
    else:
        raise KeyError("'date_time' column is missing from the dataset")

    return df