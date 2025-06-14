from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,EmailStr
from datetime import date
from typing import Annotated,Optional,List
from sqlalchemy.orm import Session

from model import Base,macbook_prices,Login,Signup
from database import SessionLocal, engine
import uuid

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class login_data(BaseModel):
    gmail: Annotated[EmailStr, Field(..., description="Gmail ID")]
    password: Annotated[str, Field(..., description="Password")]

class signup_data(BaseModel):
    name: Annotated[str, Field(..., description="name of person", examples=["Jay"])]
    gmail : EmailStr
    password : Annotated[str, Field(..., description="Password")]

@app.post("/signup")
def signup(user: signup_data, db: Session = Depends(get_db)):
    if db.query(Signup).filter_by(gmail=user.gmail).first():
        raise HTTPException(status_code=400, detail="GMAIL ALREADY EXISTS")

    db.add(Login(gmail=user.gmail, password=user.password))
    db.add(Signup(
        name=user.name,
        gmail=user.gmail,
        password=user.password
    ))
    db.commit()

    return JSONResponse(status_code=201, content={"message": "SIGNUP SUCCESSFUL"})

@app.post("/login")
def login(user: login_data, db: Session = Depends(get_db)):
    user_login = db.query(Login).filter_by(gmail=user.gmail).first()
    if not user_login:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    if user_login.password != user.password:
        raise HTTPException(status_code=401, detail="INVALID PASSWORD")

    return JSONResponse(status_code=200, content={"message": "LOGIN SUCCESSFUL"})


class macbook_input(BaseModel):
    PRODUCT_NAME: Annotated[str, Field(..., description='name of the apple product', examples =["13-inch MacBook Air M3 256"])]
    DATE: Annotated[Optional[date], Field(None, description="Start date (optional)")]

class macbook_output(BaseModel):
    PRODUCT_NAME: str
    DATE: date
    PRODUCT_PRICE: int
    SOURCE: str


@app.post("/prices",response_model=List[macbook_output])
def mac_prices(product: macbook_input,db: Session = Depends(get_db)):
    query =  db.query(macbook_prices).filter_by(PRODUCT_NAME = product.PRODUCT_NAME)
    if not query:
        raise HTTPException(status_code=400,detail="PRODUCT DOESNOT EXIST")
    
    if product.DATE:
        query = query.filter(macbook_prices.DATE >= product.DATE)

    prices = query.order_by(macbook_prices.DATE.asc()).all()

    return prices


