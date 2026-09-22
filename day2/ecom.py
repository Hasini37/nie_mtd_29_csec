from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Ecommerce customer support system"}


# ---------------- MONGODB ----------------

client = MongoClient("mongodb://localhost:27017/")

db = client["ecommerce_support"]

tickets_collection = db["tickets"]


# ---------------- SCHEMA ----------------

class TicketCreate(BaseModel):
    ticketId: str
    customerId: str
    orderId: str
    category: str
    description: str
    assignedAgent: str | None = None
    status: str


# inheritance
class TicketResponse(TicketCreate):
    id: str


# ---------------- APIs ----------------


# GET ALL TICKETS

@app.get("/tickets")
def ticket_read_all():

    tickets = list(tickets_collection.find())

    for ticket in tickets:
        ticket["id"] = str(ticket["_id"])
        del ticket["_id"]

    return tickets


# GET TICKET BY ID

@app.get("/tickets/{ticket_id}")
def ticket_read_by_id(ticket_id: str):

    ticket = tickets_collection.find_one(
        {"ticketId": ticket_id}
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket["id"] = str(ticket["_id"])
    del ticket["_id"]

    return ticket


# CREATE TICKET

@app.post(
    "/tickets",
    status_code=201,
    response_model=TicketResponse
)
def ticket_create(ticket_payload: TicketCreate):

    ticket = ticket_payload.model_dump()

    result = tickets_collection.insert_one(ticket)

    ticket["id"] = str(result.inserted_id)

    return ticket


# UPDATE TICKET

@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def ticket_update(
    ticket_id: str,
    ticket_payload: TicketCreate
):

    result = tickets_collection.update_one(
        {"ticketId": ticket_id},
        {
            "$set": ticket_payload.model_dump()
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket = tickets_collection.find_one(
        {"ticketId": ticket_id}
    )

    ticket["id"] = str(ticket["_id"])
    del ticket["_id"]

    return ticket


# DELETE TICKET

@app.delete("/tickets/{ticket_id}")
def ticket_delete(ticket_id: str):

    result = tickets_collection.delete_one(
        {"ticketId": ticket_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return {
        "message": "Ticket deleted successfully"
    }