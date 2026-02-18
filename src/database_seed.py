import os
from dotenv import load_dotenv
from src.crud import engine, SessionLocal, Base
from src.database.models import Assets, DailyPrice # Importa i modelli per registrarli
from src.crud import sync_asset_prices

load_dotenv()

def initialize_and_seed():
    db = SessionLocal()
    try:
        result = db.query(DailyPrice).filter(
            DailyPrice.asset_id == 1,
            DailyPrice.date > '1980-01-01'
        ).all()
        print(f"Found {len(result)} records for asset_id=1 and date > 1980-01-01")
    finally:
        db.close()

if __name__ == "__main__":
    initialize_and_seed()