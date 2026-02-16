from requests import Session
from database.models import *


def get_asset_by_ticker(db, ticker):
    ticker_clean = ticker.strip().upper()
    
    try:
        return db.query(Assets).filter(Assets.ticker == ticker_clean).first()
    except Exception as e:
        print(f"Error querying the database for ticker {ticker_clean}: {e}")
        return None