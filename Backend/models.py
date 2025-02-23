from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    credit_card = Column(String, nullable=True)  # Will be used later for checkout

    appointments = relationship("Appointment", back_populates="customer")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    appointment_time = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="appointments")
