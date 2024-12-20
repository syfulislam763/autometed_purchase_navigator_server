from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy import text
from fastapi.responses import JSONResponse
import pprint
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json

load_dotenv()



# My hosted database information
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
dialogflow_config = os.getenv("DIALOGFLOW_CONFIG")

print(dialogflow_config)


DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"


SESSION_DURATION = timedelta(days=1)

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_user(user:dict, db:Session=Depends(get_db)):
    try:
        
        query = text(f"SELECT * FROM users WHERE email = :email and password = :password")
        result = db.execute(query, user)
        return result.fetchone()
    except Exception as e:
        pprint.pprint({"get user error", e})
        return None


async def get_current_user(session_id:str=Header(...), db:Session=Depends(get_db)):
    try:
        current_time = datetime.now()
        query = text(f"SELECT user_id FROM sessions WHERE session_id = :session_id AND expires_at > :current_time")
        temp = db.execute(query, {"session_id":session_id, "current_time":current_time})
        result = temp.fetchone()
        if not result:
            return {"session_id":session_id,"user_id": None, "username": None}

        user_id = result[0]
        try:
            userQuery = text(f"SELECT username FROM users WHERE user_id = :id")
            userResult = db.execute(userQuery, {"id":user_id})
            user = userResult.fetchone()
            return {"session_id":session_id,"user_id": user_id, "username": user[0]}
        except Exception as e:
            return {"session_id":session_id,"user_id": None, "username": None}

    except Exception as e:
        pprint.pprint({"get current user error": e})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your are unauthorized! login again")

def create_session(user_id: int, db:Session=Depends(get_db)):
    try:

        search_query = text(f"SELECT session_id FROM sessions WHERE user_id = :user_id AND expires_at > :current_time")
        current_time = datetime.now()

        result = db.execute(search_query, {"user_id":user_id,"current_time": current_time})
        old_session_id = result.fetchone()
        
        if old_session_id is not None:
            return str(old_session_id[0])


        session_id = str( uuid.uuid4() )
        expires_at = datetime.now() + SESSION_DURATION
        query = text(f"INSERT INTO sessions (session_id, user_id, expires_at) VALUES (:session_id, :user_id, :expires_at)")
        
        db.execute(query, {"session_id":session_id, "user_id":user_id, "expires_at": expires_at})
        db.commit()
        return session_id
    except Exception as e:
        pprint.pprint({"create session error": e})
        return 0
    

def create_new_user(user:dict, db:Session=Depends(get_db)):
    try:
        query = text(f"INSERT INTO users (email, username, password) VALUES (:email, :username, :password)")
        db.execute(query, user)
        db.commit()
        return 0
    except Exception as e:
        db.rollback()
        pprint.pprint({"create new urser error": e})
        return 1


def get_orders_by_id(order_id:int,user_id:int, db:Session=Depends(get_db)):
    try:
        query = text(f"SELECT FoodName, Quantity FROM Orders WHERE OrderID = :order_id AND user_id = :user_id")
        result = db.execute(query, {"order_id": order_id, "user_id":user_id})
        orders = result.fetchall()
        return orders
    except Exception as e:
        db.rollback()
        pprint.pprint({"get order error" : e})

def get_order_status(id:int, db:Session=Depends(get_db)):
    try:
        query = text(f"SELECT * FROM OrdersStatus where OrderID = :id")
        result = db.execute(query, {"id":id})
        order_status = result.fetchone()
        return order_status
    except Exception as e:
        db.rollback()
        pprint.pprint({"get status error": e})
        
    
    

def get_next_order_id(db:Session=Depends(get_db)):
    try:
        query = text("SELECT MAX(OrderID) FROM Orders")
        result = db.execute(query)
        next_order_id = result.fetchone()
        if not next_order_id[0]:
            return 1
        
        return next_order_id[0]+1
    except Exception as e:
        db.rollback()
        pprint.pprint({"id error": e})

def get_order_price_by_quantity(current_order:dict, db:Session=Depends(get_db)):
    temp = []
    for key, value in current_order.items():
        try:
            query = text(f"SELECT ID, Price FROM foodItems where FoodName = '{key}'")
            result = db.execute(query)
            item = result.fetchone()
            temp.append({"price": int(item[1] * int(value) ), "quantity": int(value), "id":  item[0], "food_name": key})
        except Exception as e:
            db.rollback()
            pprint.pprint({"price error": e})

    return temp


def insert_order(record:dict, db:Session=Depends(get_db)):
    try:
        query = text("INSERT INTO Orders (OrderID, ItemID, FoodName, Quantity, TotalPrice, user_id) VALUES (:OrderID, :ItemID, :FoodName, :Quantity, :TotalPrice, :user_id)")

        db.execute(query, record)
        db.commit()
        return 0
    except Exception as e:
        db.rollback()
        pprint.pprint({"order error": e})
        return 1

def insert_order_status(record:dict, db:Session=Depends(get_db)):
    try:
        query = text("INSERT INTO OrdersStatus (OrderID, OrderStatus, PayablePrice) VALUES (:OrderID, :OrderStatus, :PayablePrice)")
        db.execute(query, record)
        db.commit()
        return 0
    except Exception as e:
        db.rollback()
        pprint.pprint({"post status error": e})
        return 1




def get_all_foodItems(db:Session=Depends(get_db)):
    try:
        query = text("SELECT FoodName, Price FROM foodItems")
        result = db.execute(query)
        fooditems = result.fetchall()
        return fooditems
    except Exception as e:
        db.rollback()
        pprint.pprint({"get fooditem error": e})
