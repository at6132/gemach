from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
from Backend.models import Item
from pydantic import BaseModel
import shutil
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema for adding items
class ItemCreate(BaseModel):
    name: str
    description: str
    barcode: str
    inventory_count: int = 1

# Create "images" folder if it doesn't exist
IMAGE_DIR = "backend/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

@router.post("/add")
def add_item(
    item: ItemCreate, 
    db: Session = Depends(get_db)
):
    new_item = Item(
        name=item.name,
        description=item.description,
        barcode=item.barcode,
        inventory_count=item.inventory_count,
        available=True
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Item added", "item": new_item}

@router.post("/upload-image/{item_id}")
def upload_image(item_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"{IMAGE_DIR}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update item with image path
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        item.image_path = file_path
        db.commit()
        return {"message": "Image uploaded", "image_path": file_path}
    
    return {"error": "Item not found"}
