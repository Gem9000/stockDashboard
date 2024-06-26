'''
By: George Moraites
Date: 06/11/2024
Description: This project was made as a personal
project to consolidate stock information into a
personal dashboard.
'''
from flask import Flask, render_template, jsonify, request
import os
import requests

app = Flask(__name__)

# Polygon.io base URL
POLYGON_URL = "https://api.polygon.io"

# Get the API key from the environment variable
API_KEY = os.getenv('POLYGON_API_KEY')

if not API_KEY:
    raise ValueError("No API key provided. Set the POLYGON_API_KEY environment variable.")

# Define the indices and their respective tickers
indices = {
    "DOW": "DIA",      # SPDR Dow Jones Industrial Average ETF
    "S&P 500": "SPY",  # SPDR S&P 500 ETF
    "NASDAQ-100": "QQQ" # Invesco QQQ ETF
}

def get_open_close(ticker, date):
    url = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data for {ticker}: {response.text}")
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def api_data():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "date query parameter is required"}), 400

    results = {}
    for index, ticker in indices.items():
        try:
            data = get_open_close(ticker, date)
            results[index] = {
                "ticker": ticker,
                "date": data['from'],
                "open": data['open'],
                "close": data['close']
            }
        except Exception as e:
            results[index] = {"error": str(e)}

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)