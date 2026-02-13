import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

def check_connection():
    try:
        # 2. Create the connection engine
        engine = create_engine(db_url)
        
        # 3. Try to connect and execute a simple SQL command
        with engine.connect() as conn:
            # This just asks the database to return the number 1
            result = conn.execute(text("SELECT 1"))
            print("✅ Connection Successful!")
            print(f"Database Response: {result.fetchone()}")
            
    except Exception as e:
        print("❌ Connection Failed.")
        print(f"Error details: {e}")
        
if __name__ == "__main__":
    check_connection()