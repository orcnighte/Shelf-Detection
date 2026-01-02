"""
Analytics endpoints for data analysis
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models import Product, DailyCount
from app.schemas import WeeklyAnalyticsResponse, AnalyticsSummary
from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/analytics/weekly", response_model=WeeklyAnalyticsResponse)
async def get_weekly_analytics(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get weekly analytics for all products
    Calculates average daily demand, growth rate, and demand consistency
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    # Get all products with counts in the period
    products = db.query(Product).all()
    summaries = []

    for product in products:
        counts = db.query(DailyCount).filter(
            DailyCount.product_id == product.id,
            DailyCount.date >= start_date,
            DailyCount.date <= end_date
        ).order_by(DailyCount.date).all()

        if len(counts) >= 2:  # Need at least 2 data points
            count_values = [c.count for c in counts]
            
            summary = analytics_service.calculate_product_analytics(
                product_id=product.id,
                product_name=product.name,
                counts=count_values,
                dates=[c.date for c in counts]
            )
            summaries.append(summary)

    return WeeklyAnalyticsResponse(
        start_date=start_date,
        end_date=end_date,
        products=summaries
    )


@router.get("/analytics/daily")
async def get_daily_summary(
    target_date: date = None,
    db: Session = Depends(get_db)
):
    """Get daily summary for a specific date"""
    if target_date is None:
        target_date = date.today()

    counts = db.query(DailyCount).filter(DailyCount.date == target_date).all()
    
    return {
        "date": target_date,
        "total_products": len(counts),
        "total_items": sum(c.count for c in counts),
        "products": [
            {
                "product_id": c.product_id,
                "product_name": c.product.name,
                "count": c.count
            }
            for c in counts
        ]
    }




