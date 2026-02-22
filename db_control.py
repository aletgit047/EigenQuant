from src.crud import *
from src.database.models import *

from db_seed import *

def count_asset_daily_prices(db: Session, asset_id: int, ticker: str) -> None:
    """
    Counts records using the existing session passed as an argument.
    
    Args:
        db (Session): The SQLAlchemy database session.
        asset_id (int): The ID of the asset to count daily price records for.
        ticker (str): The stock market symbol (e.g., 'AAPL').
    """
    count = db.query(DailyPrice).filter(DailyPrice.asset_id == asset_id).count()
    print(f"📈 Asset {ticker.upper():<5} (ID: {asset_id:>3}) has {count:>5} daily price records.")

def check_all_inventory():
    """
    Checks the inventory of daily price records for all assets in the database.
    It retrieves all assets and counts the number of daily price records for each, printing the results.
    """
    with SessionLocal() as db:
        assets = db.query(Asset).all()
        print(f"🚀 Checking inventory for {len(assets)} assets...\n" + "-"*50)
        
        for asset in assets:
            count_asset_daily_prices(db, asset.id, asset.ticker)
            
        print("-"*50 + "\n🎯 Inventory check complete!")

if __name__ == "__main__":
    check_all_inventory()