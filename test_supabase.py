import os
from tiingo import TiingoClient
from dotenv import load_dotenv

load_dotenv()
config = {
    'api_key': os.getenv("TIINGO_API_KEY"),
    'session': True
}

client = TiingoClient(config)

historical_data = client.get_ticker_price(
    "AAPL",
    fmt='json',
    startDate='2023-01-01',
    endDate='2023-12-31',
    frequency='daily'
)

for day in historical_data:
    print(day)