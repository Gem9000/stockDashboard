import os
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

API_KEY = os.getenv('POLYGON_API_KEY')

if not API_KEY:
    raise ValueError("No API key provided. Set the POLYGON_API_KEY environment variable.")

indices = {
    "DOW": "DIA",
    "S&P 500": "SPY",
    "NASDAQ-100": "QQQ"
}

def get_open_close(ticker):
    url = f"https://api.polygon.io/v1/open-close/{ticker}/2024-06-20?apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data for {ticker}: {response.text}")
    return response.json()

@app.route('/data')
def data():
    result = {}
    for index, ticker in indices.items():
        try:
            data = get_open_close(ticker)
            result[index] = {
                "ticker": ticker,
                "date": data['from'],
                "open": data['open'],
                "close": data['close']
            }
        except Exception as e:
            result[index] = {"error": str(e)}
    return jsonify(result)

'''
@app.route('/')
def index():
    return render_template('index.html')
'''

if __name__ == "__main__":
    app.run(debug=True)