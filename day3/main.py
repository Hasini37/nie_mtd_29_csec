from pydoc import doc

from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from datetime import datetime, timedelta,timezone


#app
app = FastAPI()

#db config
URL =  "mongodb://127.0.0.1:27017/"
client = MongoClient(URL)
db = client["ecommerce_support_db"]
tickets_collection = db["tickets"]
user_collection = db["users"]

#security config
password_hash = PasswordHash.recommended()
SECRET_KEY = "EcommerceSupportSecretKey-ChangeThis"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
#pydantic schema
class TicketCreate(BaseModel):
    category: str
    description: str
    assignedAgent: str 
    status: str
    orderId: str
    
class TicketResponse(TicketCreate):
    id: str
    
class UserCreate(BaseModel):
    username: str
    password: str
    role: int 
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
#helper
def  ticket_helper(ticket_doc):
    return {
        "id": str(ticket_doc["_id"]),
        "category": ticket_doc["category"],
        "description": ticket_doc["description"],
        "assignedAgent": ticket_doc.get("assignedAgent"),
        "status": ticket_doc["status"],
        "orderId": ticket_doc["orderId"]
    }
    
def user_helper(user):   
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }
    
def create_token(username: str, role: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINS)
    payload = {"sub": username, "role": role, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role =  payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = user_collection.find_one({"username": username})
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
def require_role(*allowed_roles):
    def check_role(get_current_user=Depends(get_current_user)):
        if get_current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return get_current_user
    return check_role


#apis - CRUD - create, read, update, delete
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    queried_user = user_collection.find_one({"username" : user.username})
    if queried_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    hashed_pwd = password_hash.hash(user.password)
    user_data = {
        "username": user.username,
        "password": hashed_pwd,
        "role": user.role
    }
    result = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

@app.post("/login", response_model=TokenResponse)
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"username": form_data.username})
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not password_hash.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(user["username"], user["role"])
    return {"access_token" : token, "token_type" : "bearer"}
@app.post("/tickets", status_code=201, response_model=TicketResponse)
def ticket_create(ticket_payload: TicketCreate):
    ticket_dict = ticket_payload.model_dump()
    result = tickets_collection.insert_one(ticket_dict)
    new_ticket = tickets_collection.find_one({"_id": result.inserted_id})
    return ticket_helper(new_ticket)

@app.get("/tickets", response_model=list[TicketResponse])
def ticket_read_all():
    docs = tickets_collection.find()
    tickets = [ticket_helper(doc) for doc in docs]
    return tickets

@app.get("/tickets/{id}", response_model=TicketResponse)
def ticket_read_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid ticket ID", status_code=403)
    doc = tickets_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(detail="Ticket not found", status_code=404)
    return ticket_helper(doc)

@app.put("/tickets/{id}", response_model=TicketResponse)
def ticket_update(id: str, ticket_payload: TicketCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid ticket ID", status_code=403)
    ticket_dict = ticket_payload.model_dump()
    result = tickets_collection.update_one({"_id": ObjectId(id)}, {"$set": ticket_dict})
    if result.matched_count == 0:
        raise HTTPException(detail="Ticket not found", status_code=404)
    new_ticket = tickets_collection.find_one({"_id": ObjectId(id)})
    return ticket_helper(new_ticket) 

@app.delete("/tickets/{id}")
def ticket_delete(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid ticket ID", status_code=403)
    result = tickets_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(detail="Ticket not found", status_code=404)
    return {"message": "Ticket deleted successfully"}

