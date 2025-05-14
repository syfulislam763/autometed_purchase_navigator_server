from fastapi import FastAPI, Depends, HTTPException
from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy import text
from pprint import pprint
import re
from .database import get_db, create_new_user, get_user, create_session,get_current_user
from .generic_helper import add_ongoing_order, get_avaiable_menu,remove_ongoing_order,complete_order, order_tracking
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from pydantic import BaseModel
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse


load_dotenv()

current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

json_file_path = f"{current_directory}/dialogflow_config.json"


app = FastAPI(
    title="Food Order Assistant",
    description=""" "Food Order Assistant" is only responsible for the customer's order placement.\n\nUsage:\n- Signin if you have account otherwise create an account then signin for order placement. \n- After signin a session id will be provided that needs to use in every request. If the session is expired you have to login again. \n- You may start the conversation with any greeting words. \n\nApplication Features: \n- Submit an order \n- Track order status by id \n- Shows available items \n\n Technologies: \n- FastAPI, Python \n- Google DialogFlow \n- MySQL database""",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "API",
            "description": "All operations"
        }
    ]
)


DIALOGFLOW_PROJECT_ID = os.getenv("PROJECT_ID")
DIALOGFLOW_LANGUAGE_CODE = os.getenv("LANGUAGE_CODE")

dialogflow_config = {
    "type": os.getenv("TYPE") ,
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id":os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email":os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}



SERVICE_ACCOUNT_FILE = json_file_path

# Initialize Dialogflow session client
SESSION_CLIENT = dialogflow.SessionsClient.from_service_account_json(SERVICE_ACCOUNT_FILE)


# Request model from the frontend
class ChatRequest(BaseModel):
    message: str

class LoginUser(BaseModel):
    email:str
    password:str

class CreateUser(BaseModel):
    email: str
    username: str
    password: str


in_process_order = {

}

@app.get("/", include_in_schema=False, tags=["API"])
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/login", name="signin", tags=["API"])
async def login(user:LoginUser, db:Session=Depends(get_db)):
    logged_in_user = get_user(dict(user), db)
    if logged_in_user:
        user_id = logged_in_user[0]
        session_id = create_session(user_id, db)
        email = logged_in_user[1]
        username = logged_in_user[2]
        
        if not session_id:
            return{"message": "Login was not successful, Your password or username invalid"}
        
        return {"message": "Login successful", "session_id": session_id, "user_id":user_id, "email":email, "username": username}
    else:
        return{"message": "Login was not successful, Your password or username invalid!"}


@app.post("/create_user/", name="signup", tags=["API"])
async def create_user(user:CreateUser, db:Session=Depends(get_db)):
    try:
        
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        if not email_regex.match(user.email):
            return {"message": "Invalid email"}

        temp_user = dict(user)
        
        resutl = create_new_user(temp_user, db)
        if resutl:
            return {"message": "This username already exist"}
        else:
            return {"message": "Account created successfully!"}
    except Exception as e:
        pprint({"create user error": e})

@app.post("/chatbot/", name="start conversation", tags=["API"])
async def chatbot_interaction(request: ChatRequest, current_user:dict = Depends(get_current_user), db:Session=Depends(get_db)):
    try:
        session_id = current_user['session_id']
        
        session = SESSION_CLIENT.session_path(DIALOGFLOW_PROJECT_ID, session_id)

        # Prepare the text input for Dialogflow
        text_input = dialogflow.types.TextInput(text=request.message, language_code=DIALOGFLOW_LANGUAGE_CODE)

        query_input = dialogflow.types.QueryInput(text=text_input)

        # Send the input to Dialogflow
        response = SESSION_CLIENT.detect_intent(session=session, query_input=query_input)

        
        parameters = dict(response.query_result.parameters)
        intent = str(response.query_result.intent.display_name)
        
        intent_task_handler = {
            "order.add: ongoing-context": add_ongoing_order,
            "menu.show": get_avaiable_menu,
            "oder.remove: onegoing-context": remove_ongoing_order,
            "order.complete: ongoing-order": complete_order,
            "track.oder : ongoing-tracking": order_tracking
        }


        if not current_user['user_id']:
            response.query_result.fulfillment_text = f"Can't identify you. plase login again!"
            return {"mama": response.query_result.fulfillment_text}

        if intent not in intent_task_handler.keys():
            return {"mama": response.query_result.fulfillment_text}

        user_id = current_user['user_id']
        response.query_result.fulfillment_text = intent_task_handler[intent](in_process_order, parameters, user_id , db)

        return {"mama": response.query_result.fulfillment_text}
    except Exception as e:
        print("error")
        return {"message": e}



@app.get("/foodItems", name="All food items", tags=["API"])
async def home (current_user:dict = Depends(get_current_user), db:Session = Depends(get_db)):
    try:

        if not current_user['user_id']:
            return {"message": "No data found!"}
        
        # query = text(f"SELECT * FROM Orders")
        # query = text(f"SELECT * FROM foodItems where Category = 'Starter'")
        query = text(f"SELECT * FROM foodItems")
        result = db.execute(query)
        # keys = ("OrderID", "ItemID", "Quantity", "TotalPrice")
        keys = ("ID", "FoodName", "Category", "Description", "Price")
        order = result.fetchall()

        res = []
        for tup in order:
            res.append(dict(zip(keys, tup)))


        return res
    
    except Exception as e:
        return {"message": "No data found!"}






