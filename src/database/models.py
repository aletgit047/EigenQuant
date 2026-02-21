from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ticker = Column(String, unique=True, nullable=False, index=True)
    
    prices = relationship("DailyPrice", back_populates="asset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Asset(ticker='{self.ticker}', name='{self.name}')>"
    
class DailyPrice(Base):
    __tablename__ = 'daily_prices'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    
    date = Column(DateTime, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    
    asset = relationship("Asset", back_populates="prices")

    def __repr__(self):
        return f"<DailyPrice(asset_id={self.asset_id}, date='{self.date.date()}')>"