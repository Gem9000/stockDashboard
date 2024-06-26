import os
import requests

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

def get_open_close(ticker,date):
    url = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data for {ticker}: {response.text}")
    return response.json()

def main(dates):
    for date in dates:
        print(f"Data for {date}")
        for index, ticker in indices.items():
            try:
                data = get_open_close(ticker, date)
                print(f"{index} ({ticker})")
                print(f"Date: {data['from']}")
                print(f"Open: {data['open']}")
                print(f"Close: {data['close']}\n")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    # List of dates you want to fetch data for
    dates_input = input("Enter the date you want (YYYY-MM-DD): ")
    dates = [date.strip() for date in dates_input.split(",") if date.strip()]

    if dates:
        main(dates)
    else:
        print("Error with handling the date.")