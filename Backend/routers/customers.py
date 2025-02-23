from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Customer, Appointment
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema for adding customers
class CustomerCreate(BaseModel):
    name: str
    phone: str

# Schema for booking an appointment
class AppointmentCreate(BaseModel):
    customer_id: int
    appointment_time: datetime

@router.post("/customers/create")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(Customer.phone == customer.phone).first()
    if existing_customer:
        return {"error": "Customer already exists"}

    new_customer = Customer(name=customer.name, phone=customer.phone)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer added", "customer": new_customer}

@router.get("/customers/search")
def search_customer(phone: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        return customer
    return {"error": "Customer not found"}

@router.post("/appointments/book")
def book_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == appointment.customer_id).first()
    if not customer:
        return {"error": "Customer not found"}

    new_appointment = Appointment(customer_id=appointment.customer_id, appointment_time=appointment.appointment_time)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message": "Appointment booked", "appointment": new_appointment}
