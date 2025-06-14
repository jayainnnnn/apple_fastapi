from sqlalchemy import Column,String,Integer,Date,ForeignKey
from database import Base

class Login(Base):
    __tablename__ = "login_details"
    gmail = Column(String, primary_key=True)
    password = Column(String, nullable=False)

class Signup(Base):
    __tablename__ = "signup_details"
    name = Column(String, nullable=False)
    gmail = Column(String, primary_key=True)
    password = Column(String, nullable=False)


class macbook_prices(Base):
    __tablename__ = "macbook prices"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    PRODUCT_NAME = Column(String, nullable=False)
    PRODUCT_PRICE = Column(Integer, nullable=False)
    DATE = Column(Date, nullable=False)
    SOURCE = Column(String,nullable=False)
