import time

from src.crud import *

assets = {"Apple Inc.": "AAPL", "Microsoft Corp.": "MSFT", "Alphabet Inc.": "GOOGL", "Amazon.com Inc.": "AMZN", 
          "Meta Platforms Inc.": "META", "NVIDIA Corp.": "NVDA", "Tesla Inc.": "TSLA", 
          "JPMorgan Chase & Co.": "JPM", "Visa Inc.": "V", "Procter & Gamble Co.": "PG", "Johnson & Johnson": "JNJ",
          "Walmart Inc.": "WMT", "Mastercard Inc.": "MA", "Coca-Cola Co.": "KO", "Walt Disney Co.": "DIS", 
          "Advanced Micro Devices Inc.": "AMD", "Netflix Inc.": "NFLX", "Salesforce Inc.": "CRM", 
          "PayPal Holdings Inc.": "PYPL", "Uber Technologies Inc.": "UBER", "Adobe Inc.": "ADBE", 
          "Intel Corp.": "INTC", "Palantir Technologies Inc.": "PLTR", "Caterpillar Inc.": "CAT", "3M Co.": "MMM", 
          "Boeing Co.": "BA", "Chevron Corp.": "CVX", "SPDR S&P 500 ETF Trust": "SPY", "Invesco QQQ Trust": "QQQ", 
          "SPDR Dow Jones Industrial Average ETF Trust": "DIA", "iShares Russell 2000 ETF": "IWM", 
          "Financial Select Sector SPDR Fund": "XLF", "Technology Select Sector SPDR Fund": "XLK", 
          "Consumer Discretionary Select Sector SPDR Fund": "XLY", "Energy Select Sector SPDR Fund": "XLE", 
          "VanEck Semiconductor ETF": "SMH",
          "SPDR Gold Shares": "GLD", "iShares Silver Trust": "SLV","iShares 20+ Year Treasury Bond ETF": "TLT",}

def seed_and_sync_database():
    with SessionLocal() as db:
        print(f"🚀 Starting synchronization for {len(assets)} assets...")
        
        for name, ticker in assets.items():
            try:
                print(f"🔄 Syncing {name} ({ticker})...")
                
                sync_asset_prices(db, ticker)
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Critical error syncing {ticker}: {e}")
                continue
        
        print("🎯 Global synchronization complete!")

if __name__ == "__main__":
    seed_and_sync_database()