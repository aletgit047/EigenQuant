from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Assets(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ticker = Column(String, unique=True, nullable=False)
    prices = relationship("DailyPrice", back_populates="asset")
    
class DailyPrice(Base):
    __tablename__ = 'daily_prices'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    
    date = Column(DateTime, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    
    asset = relationship("Assets", back_populates="prices")