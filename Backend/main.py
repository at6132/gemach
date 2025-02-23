from fastapi import FastAPI
from routers import inventory, reservations
from database import Base, engine


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers (for modular API design)
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])

@app.get("/")
def home():
    return {"message": "Welcome to the Gemach Item Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
