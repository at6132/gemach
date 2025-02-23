from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_reservations():
    return {"message": "List of all reservations"}

@router.post("/create")
def create_reservation():
    return {"message": "Reservation created"}
