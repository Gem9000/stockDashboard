'''
By: George Moraites
Date: 06/11/2024
Description: This project was made as a personal
project to consolidate stock information into a
personal dashboard.
'''

from flask import Flask, jsonify, request
import os
import requests

import matplotlib as plt
import webbrowser
import threading

app = Flask(__name__)

# Polygon.io base URL
POLYGON_URL = "https://api.polygon.io"

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    # Retrieve the API key from environment variables
    api_key = os.getenv('POLYGON_API_KEY')
    if not api_key:
        return jsonify({"error": "API key not found"}), 500

    # Get date range from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date query parameters are required"}), 400

    # Construct the endpoint
    endpoint = f"/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    url = f"{POLYGON_URL}{endpoint}"

    # Make the request to the Polygon.io API with the API key as a query string parameter
    response = requests.get(url, params={"apiKey": api_key})

    # Check if the request was successful
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Polygon.io", "status_code": response.status_code}), response.status_code

    # Parse the JSON response
    data = response.json()

    # Return the data as a JSON response
    return jsonify(data)

def plot_data():
    pass   

if __name__ == '__main__':
    app.run(debug=True)