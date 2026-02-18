import os
from dotenv import load_dotenv
from src.database.models import *
from src.crud import engine, SessionLocal
from src.crud import sync_asset_prices


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
db = SessionLocal()

try:
    # 2. Passa l'istanza 'db', non la classe 'SessionLocal'
    sync_asset_prices(db, "AAPL")
finally:
    # 3. Chiudi sempre la sessione per liberare la connessione a Supabase
    db.close()