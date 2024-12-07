
# cis6930fa24 -- Project3

## Author

**Name**: Balasai Srikanth Ganti

**UFID** : 5251-6075

## Assignment Description 
This project is a web application that processes incident reports from PDFs, visualizes the data, and provides insights like clustering, bar graphs, pie charts, and statistics. The application is built using Flask and integrates with various Python libraries for data manipulation and visualization.


## Features

- Upload incident reports as files or provide URLs to fetch PDF reports.
- Extracts structured data from the PDFs.
- Preprocesses the data to clean and transform it.
- Visualizes data using:
  - Clustering: Groups similar incidents together.
  - Bar Graph: Displays frequency of incidents by time of day.
  - Pie Chart: Summarizes the proportion of different incident types.
- Displays key statistics like the count of incidents by type.
- Stores extracted data into a SQLite database for further use.

## Technologies Used
- Backend: Flask
- PDF Processing: PyPDF
- Data Manipulation: Pandas
- Data Visualization: Matplotlib, Seaborn
- Clustering: Scikit-learn
- Database: SQLite

## How to install

To set up the environment, use pipenv to install the dependencies.

```bash
pipenv install .
```

## How to run
Run the program using the following commands:

### Run the application:
```bash
pipenv run python main.py
```

#### Access the application in your browser at:

```bash 
http://127.0.0.1:5000/
```

### Run the test file:

```bash
pipenv run python -m pytest -v
```


## Video demo:


### Steps to Visualise the document:

- Visit the home page.
Upload a PDF or provide a URL to fetch a PDF of incident reports.
- The application extracts data, preprocesses it, and generates:
  - Clustering visualization
  - Bar graph
  - Pie chart
  - Incident statistics
- View the visualizations and statistics on the results page.
- For a new file/files click the "Go Back" Button at the bottom and repeat the steps above.


## Visualization Choices and Justifications

This project uses three main types of visualizations to represent and analyze the data extracted from the incident reports. Below is a description of each chart type and the rationale for its selection:

---

### 1. Clustering Visualization (Scatter Plot with PCA)
#### Description:
- A scatter plot generated using Principal Component Analysis (PCA) to reduce the dimensionality of the data. DBSCAN, clustering algorithms is used to group similar incidents, and the clusters are visualized in 2D.
- PCA simplifies high-dimensional data into two dimensions while preserving meaningful variance.

#### Why DBSCAN Was Chosen

- Identifies clusters of arbitrary shapes, making it suitable for irregular patterns in real-world incident data.
- Handles noise effectively by treating outliers as separate from clusters.
- Does not require the number of clusters to be predefined, providing flexibility for dynamic datasets.
- Aligns well with density-based groupings often seen in incident data distributions.
- More robust than KMeans, avoiding issues like sensitivity to initialization and uniform cluster assumptions.


### 2. Bar Graph
#### Description:
- A bar graph that shows the frequency of incidents categorized by the time of day (e.g., Morning, Afternoon, Evening, Night).

#### Details:
- Visualizing incidents by time of day highlights when specific types of incidents are most frequent.
- Allows users to compare the volume of incidents across time periods.
- A bar graph is an effective way to convey count-based data in a straightforward and readable format.


### 3. Pie Chart
#### Description:
- A pie chart that represents the proportion of different types of incidents (e.g., Alarm, Assist, Burglary).

#### Details:
- Ideal for understanding the distribution of incidents across categories.
- Combines smaller categories into "Other," ensuring clarity and preventing clutter.
- Pie charts are widely recognized and intuitive for non-technical audiences.


## Functions Used

### **1. `__init__.py`**
#### `create_app()`
- **Description**: Initializes and configures a Flask application instance.
- **Parameters**: None.
- **Returns**: A Flask application object.

---

### **2. `database.py`**
#### `save_to_database(df, db_path)`
- **Description**: Saves a Pandas DataFrame to a SQLite database.
- **Parameters**:
  - `df` (Pandas DataFrame): The data to save.
  - `db_path` (str): The path to the SQLite database file.
- **Returns**: None.

---

### **3. `routes.py`**
#### `home()`
- **Description**: Handles the `/` route and renders the `index.html` template.
- **Parameters**: None.
- **Returns**: HTML content of the home page.

#### `upload_file()`
- **Description**: Handles file and URL uploads, processes the data, generates visualizations, and renders the results.
- **Parameters**: None (Flask automatically handles the request context).
- **Processes**:
  - Uploaded files (`files[]`).
  - URLs to PDFs (`urls[]`).
  - Combines extracted data into a single DataFrame.
  - Preprocesses data and generates visualizations.
- **Returns**:
  - Renders `visualizations.html` with generated visualizations and statistics on success.
  - Renders `index.html` with an error message if something goes wrong.

#### `fetch_pdf()`
- **Description**: Handles fetching a PDF from a URL, processes the data, and renders visualizations.
- **Parameters**: None (Flask automatically handles the request context).
- **Processes**:
  - Fetches a PDF from the provided URL.
  - Extracts and preprocesses the data.
  - Saves the data to a SQLite database.
  - Generates visualizations.
- **Returns**:
  - Renders `visualizations.html` on success.
  - Renders `index.html` with an error message if something goes wrong.

---

### **4. `utils.py`**
#### `fetch_incidents(url)`
- **Description**: Downloads a PDF from the given URL and saves it locally.
- **Parameters**:
  - `url` (str): The URL of the PDF file.
- **Returns**: The path to the saved PDF file.

#### `split_line_regex(line)`
- **Description**: Splits a line of text using a regex pattern to extract structured data fields.
- **Parameters**:
  - `line` (str): A line of text to be split.
- **Returns**: A list of strings containing the extracted fields.

#### `extract_incidents(pdf_file_path)`
- **Description**: Extracts structured incident data from a PDF file.
- **Parameters**:
  - `pdf_file_path` (str): The path to the PDF file.
- **Returns**: A Pandas DataFrame with columns: `['date_time', 'incident_number', 'location', 'nature', 'incident_ori']`.

#### `preprocess_dataframe(df)`
- **Description**: Cleans and preprocesses the DataFrame, handling invalid/missing data and encoding time-of-day categories.
- **Parameters**:
  - `df` (Pandas DataFrame): The raw data to preprocess.
- **Returns**: A preprocessed DataFrame with added columns:
  - `time_of_day`: Categorized time periods.
  - `date_time_encoded`: Encoded time-of-day categories.

---

### **5. `visualizations.py`**
#### `generate_colors(num_colors)`
- **Description**: Generates a list of distinct colors for visualizations.
- **Parameters**:
  - `num_colors` (int): Number of distinct colors required.
- **Returns**: A list of color values.

#### `visualize_clustering(df)`
- **Description**: Generates a clustering visualization using PCA and clustering algorithms (e.g., DBSCAN or KMeans).
- **Parameters**:
  - `df` (Pandas DataFrame): The preprocessed data for clustering.
- **Returns**: A Base64-encoded string of the clustering plot image.

#### `visualize_bar_graph(df)`
- **Description**: Generates a bar graph for the frequency of incidents by time of day.
- **Parameters**:
  - `df` (Pandas DataFrame): The preprocessed data for visualization.
- **Returns**: A Base64-encoded string of the bar graph plot image.

#### `visualize_pie_chart(df)`
- **Description**: Generates a pie chart showing the distribution of incident types.
- **Parameters**:
  - `df` (Pandas DataFrame): The preprocessed data for visualization.
- **Returns**: A Base64-encoded string of the pie chart plot image.

### **6. `main.py`**
#### Main Functionality
- **Registers the `routes` blueprint**: Ensures all routes defined in `routes.py` are accessible.
- **Starts the Flask application**:
  - Runs in debug mode, allowing for live reloading during development.


## Libraries Used

Below is a list of the Python libraries used in the code along with their purpose:

### 1. Flask
- **Description**: A web application framework used to build the web interface for uploading files, fetching PDFs, and rendering visualizations.

### 2. Pandas
- **Description**: A library for data manipulation and analysis, used to handle and preprocess the extracted incident data.

### 3. Matplotlib
- **Description**: A data visualization library used to create clustering plots, bar graphs, and pie charts.

### 4. Scikit-learn
- **Description**: A machine learning library used for clustering (DBSCAN/KMeans), dimensionality reduction (PCA), and encoding categorical data.

### 5. PyPDF
- **Description**: A library for PDF handling and parsing, used to extract text data from uploaded or fetched PDF files.

### 6. SQLite3
- **Description**: A lightweight database engine, used to store processed incident data for future use.

### 7. Logging
- **Description**: A built-in Python library for tracking and debugging errors during data extraction and processing.

### 8. Base64
- **Description**: A built-in Python library used to encode generated plots as Base64 strings for embedding in web templates.

### 9. IO
- **Description**: A built-in Python library used for in-memory buffer handling to store visualizations before encoding them.

### 10. RE (Regular Expressions)
- **Description**: A built-in Python library used to extract structured fields from unstructured text lines in the incident data.

### 11. URLLib
- **Description**: A built-in Python library used to fetch PDFs from provided URLs.


---

### Installation
To install the required libraries, use the following command:
```bash
pipenv install flask pandas matplotlib scikit-learn pypdf
```

## Test Cases:

### test_routes.py
#### 1. `test_fetch_pdf_real_url(client)`
- Tests the `/fetch` endpoint with a real URL to ensure the application fetches the PDF, processes it, and returns the expected visualizations. Verifies the response status and checks for the presence of clustering visualization in the HTML content.

---

### test_utils.py
#### 1. `test_split_line_regex()`
- Tests the `split_line_regex` function to ensure it correctly parses a line of text into structured fields.

#### 2. `test_fetch_incidents_real_pdf()`
- Tests the `fetch_incidents` function by downloading a real PDF from the provided URL. Verifies that the file is downloaded correctly and validates its content as a PDF.

#### 3. `test_extract_incidents_real_pdf()`
- Tests the `extract_incidents` function to ensure it can correctly parse data from a real PDF and populate a DataFrame with the expected columns.

#### 4. `test_preprocess_dataframe()`
- Tests the `preprocess_dataframe` function to ensure it processes the raw DataFrame correctly by:
  - Dropping invalid date rows.
  - Adding new columns like `time_of_day` and `date_time_encoded`.
  - Assigning correct time-of-day categories.


## Bugs and Assumptions

### Bugs: 
- If the downloaded PDF is empty or contains no valid data, the application may fail without a descriptive error message.

- DBSCAN's performance depends heavily on the `eps` and `min_samples` parameters. Poorly chosen values may lead to all points being classified as noise or one large cluster.

- The `split_line_regex` function assumes a specific pattern for splitting lines. If the input text deviates from this structure, it might skip valid data or return incorrect results.


### Assumptions:

- Assumes the PDF follows a consistent structure where lines contain specific fields separated by whitespace (e.g., date, incident number, location, nature, ORI).

- Assumes the extracted DataFrame always contains the columns `['date_time', 'incident_number', 'location', 'nature', 'incident_ori']`.

- Assumes all required fields (e.g., `date_time`) are present and valid for preprocessing.

- Assumes the provided URLs point to accessible and valid PDFs.



