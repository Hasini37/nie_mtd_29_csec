from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Ecommerce customer support system"}
           
db = {
    1:{"id":1,"title":"Order not recieved","description":"I have not recieved my order yet ","status":"new"},
    2:{"id":2,"title":"wrong item received","description":"The product I received is not the one I ordered","status":"new"},
    3:{"id":3,"title":"Damaged item","description":"The item I received is damaged ","status":"new"}
}
#schema
class TicketCreate(BaseModel):
    title: str
    description: str
    status: str
    
#inheritance
class TicketResponse(TicketCreate):
    id: int
    
#APIs
@app.get("/tickets")
def ticket_read_all():
    return list(db.values())

@app.get("/tickets/{id}")
def ticket_read_by_id(id:int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db[id]

@app.post("/tickets",status_code=201, response_model=TicketResponse)
def ticket_create(ticket_payload: TicketCreate):
    new_id = max(db.keys(), default=0) + 1
    db[new_id] = {"id": new_id, **ticket_payload.model_dump()}
    return db[new_id]

@app.put("/tickets/{id}", response_model=TicketResponse)
def ticket_update(id:int, ticket_payload: TicketCreate):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db[id].update({"id": id, **ticket_payload.model_dump()})
    return db[id]

@app.delete("/tickets/{id}")
def ticket_delete(id:int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    del db[id]
    return {"message": "Ticket deleted successfully"}