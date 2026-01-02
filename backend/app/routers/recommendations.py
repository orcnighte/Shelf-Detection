"""
Weekly recommendation engine endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from app.database import get_db
from app.models import Product, DailyCount
from app.schemas import RecommendationsResponse, RecommendationItem
from app.services.recommendation_service import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()


@router.get("/recommendations/weekly", response_model=RecommendationsResponse)
async def get_weekly_recommendations(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get weekly investment and restocking recommendations
    Analyzes 7 days of data and ranks products based on:
    - Demand growth
    - Consistency
    - Stock turnover proxy
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    # Get all products with sufficient data
    products = db.query(Product).all()
    product_data = []

    for product in products:
        counts = db.query(DailyCount).filter(
            DailyCount.product_id == product.id,
            DailyCount.date >= start_date,
            DailyCount.date <= end_date
        ).order_by(DailyCount.date).all()

        if len(counts) >= 3:  # Need at least 3 data points for meaningful analysis
            count_values = [c.count for c in counts]
            dates = [c.date for c in counts]
            
            product_data.append({
                "product": product,
                "counts": count_values,
                "dates": dates
            })

    # Generate recommendations
    recommendations = recommendation_service.generate_recommendations(
        product_data=product_data,
        start_date=start_date,
        end_date=end_date
    )

    return RecommendationsResponse(
        week_start=start_date,
        week_end=end_date,
        recommendations=recommendations,
        generated_at=datetime.now()
    )

