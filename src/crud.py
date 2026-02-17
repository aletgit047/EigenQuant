from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from requests import Session
from tiingo import TiingoClient
from src.database.models import *
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Provides a database session and ensures it closes after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_asset(db: Session, name: str, ticker: str):
    """
    Retrieve an asset from the database or create it if it doesn't exist.

    Args:
        db (Session): The SQLAlchemy database session.
        name (str): The official name of the company (e.g., 'Apple Inc.').
        ticker (str): The stock market symbol (e.g., 'AAPL').

    Returns:
        Assets: The SQLAlchemy model instance for the asset.
    """
    ticker_upper = ticker.upper().strip()
    
    # Try to find the asset first
    asset = db.query(Assets).filter(Assets.ticker == ticker_upper).first()
    
    if asset:
        print(f"Asset {ticker_upper} already exists. Skipping insertion.")
        return asset

    # Create new asset if it doesn't exist
    new_asset = Assets(name=name, ticker=ticker_upper)
    try:
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        print(f"Successfully saved: {name} ({ticker_upper})")
        return new_asset
    except Exception as e:
        db.rollback()
        print(f"Error saving asset {ticker_upper}: {e}")
        return None

def get_asset_by_ticker(db: Session, ticker: str) -> Assets | None:
    """
    Retrieves an asset from the database by ticker. 
    Returns the Asset object if found, otherwise None.
    
    Args:
        db (Session): The SQLAlchemy database session.
        ticker (str): The stock market symbol (e.g., 'AAPL').

    Returns:
        Assets: The SQLAlchemy model instance for the asset.
        or None if not found.
    """
    return db.query(Assets).filter(Assets.ticker == ticker.upper().strip()).first()

def sync_asset_prices(db: Session, ticker: str) -> None:
    """
    Syncs the daily price data for a given asset ticker. 
    It checks the last date of data in the database and fetches new data 
    from Tiingo starting from the next day.
    
    Args:
        db (Session): The SQLAlchemy database session.
        ticker (str): The stock market symbol (e.g., 'AAPL').
    """
    # 1. Get the Asset
    asset = get_asset_by_ticker(db, ticker)
    if not asset:
        print(f"Asset {ticker} not found in DB. Add it first.")
        return

    # 2. Find the last date in DB
    last_date = db.query(func.max(DailyPrice.date)).filter(
        DailyPrice.asset_id == asset.id
    ).scalar()

    # 3. Determine Start Date for Tiingo
    if last_date:
        # If last_date is a datetime object, we move to the next day
        start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"Fetching data for {ticker} starting from {start_date}...")
    else:
        start_date = None 
        print(f"No data found for {ticker}. Fetching full history...")

    # 4. Fetch from Tiingo
    client = TiingoClient({'api_key': os.getenv("TIINGO_API_KEY")})
    
    try:
        # We use Python's datetime for the current date
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        data = client.get_ticker_price(
            ticker,
            fmt='json',
            startDate=start_date,
            endDate=today_str,
            frequency='daily'
        )
        
        if not data:
            print(f"No new data found for {ticker} up to {today_str}.")
            return

        # 5. Bulk Save
        new_prices = [
            DailyPrice(
                asset_id=asset.id,
                date=item['date'],
                open=item['adjOpen'],
                high=item['adjHigh'],
                low=item['adjLow'],
                close=item['adjClose'],
                volume=item['adjVolume']
            ) for item in data
        ]
                
        db.add_all(new_prices)
        db.commit()
        print(f"✅ Successfully synced {len(new_prices)} days for {ticker}.")

    except Exception as e:
        db.rollback()
        print(f"❌ Failed to sync {ticker}: {e}")