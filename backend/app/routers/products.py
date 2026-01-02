"""
Product management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product, DailyCount
from app.schemas import ProductResponse, ProductCreate, DailyCountResponse
from datetime import date, timedelta

router = APIRouter()


@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(Product).all()
    return products


@router.post("/products", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products/{product_id}/counts", response_model=List[DailyCountResponse])
async def get_product_counts(
    product_id: int,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get daily counts for a specific product"""
    start_date = date.today() - timedelta(days=days)
    counts = db.query(DailyCount).filter(
        DailyCount.product_id == product_id,
        DailyCount.date >= start_date
    ).order_by(DailyCount.date).all()
    
    if not counts:
        raise HTTPException(status_code=404, detail="Product not found or no counts available")
    
    return counts




