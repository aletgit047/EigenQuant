import os
from dotenv import load_dotenv
from src.database.models import *
from src.crud import get_or_create_asset
from src.crud import engine, SessionLocal


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def run_seed():
    # 1. Create tables if they don't exist
    print("🛠️ Synchronizing database schema...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Open a session
    db = SessionLocal()
    
    print("🌱 Seeding database...")
    test_assets = [
        {"name": "Apple Inc.", "ticker": "AAPL"},
        {"name": "Alphabet Inc.", "ticker": "GOOGL"},
        {"name": "The Coca-Cola Company", "ticker": "KO"}
    ]
    
    try:
        for item in test_assets:
            get_or_create_asset(db, item["name"], item["ticker"])
        print("✅ Seeding complete.")
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()