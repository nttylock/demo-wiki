# Wikipedia Search Application

This application allows you to search a Wikipedia database using vector search and language filtering. It provides a web interface and API for convenient use.

## Installation

1. Make sure you have Python 3.7 or higher installed.

2. Clone the repository:
   ```
   git clone <your repository URL>
   cd <directory name>
   ```

3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # For Linux and macOS
   venv\Scripts\activate  # For Windows
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure you are in the project directory and the virtual environment is activated.

2. Run the application:
   ```
   python app.py
   ```

3. Open a web browser and go to `http://localhost:5000`.

## Using the Web Interface

1. On the main page, enter your search query in the text field.
2. Click the "Search" button or press Enter.
3. View the search results on the results page.

## Connecting External Projects (Using the API)

You can use this application's API in your external projects. To do this, send POST requests to the `/api/search` endpoint.

Example of using the API in Python:

import requests

url = "http://localhost:5000/api/search"
data = {
    "query": "artificial intelligence",
    "results_lang": "en",
    "num_results": 5
}

response = requests.post(url, json=data)
results = response.json()

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Language: {result['lang']}")
    print(f"Distance: {result['_additional']['distance']}")
    print("---")