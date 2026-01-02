"""
Recommendation service for investment and restocking recommendations
"""
import numpy as np
from typing import List, Dict
from datetime import date
from app.schemas import RecommendationItem
from app.services.analytics_service import AnalyticsService


class RecommendationService:
    """Service for generating product recommendations"""
    
    def __init__(self):
        self.analytics_service = AnalyticsService()
    
    def generate_recommendations(
        self,
        product_data: List[Dict],
        start_date: date,
        end_date: date
    ) -> List[RecommendationItem]:
        """
        Generate weekly recommendations for products
        
        Args:
            product_data: List of dicts with product, counts, and dates
            start_date: Start of analysis period
            end_date: End of analysis period
            
        Returns:
            List of RecommendationItem sorted by score
        """
        recommendations = []
        
        for data in product_data:
            product = data["product"]
            counts = data["counts"]
            dates = data["dates"]
            
            # Calculate analytics
            analytics = self.analytics_service.calculate_product_analytics(
                product_id=product.id,
                product_name=product.name,
                counts=counts,
                dates=dates
            )
            
            # Calculate metrics for scoring
            growth_rate = analytics.growth_rate
            consistency = 100 - analytics.demand_consistency  # Invert: lower variation = higher consistency
            average_demand = analytics.average_daily_demand
            
            # Stock turnover proxy (average demand / max count)
            max_count = max(counts)
            turnover_proxy = (average_demand / max_count) * 100 if max_count > 0 else 0
            
            # Calculate composite score
            # Weighted combination of growth, consistency, and turnover
            growth_score = min(max(growth_rate, 0), 50) / 50 * 30  # 0-30 points
            consistency_score = min(max(consistency, 0), 100) / 100 * 30  # 0-30 points
            turnover_score = min(max(turnover_proxy, 0), 100) / 100 * 40  # 0-40 points
            
            total_score = growth_score + consistency_score + turnover_score
            
            # Generate explanation
            explanation = self._generate_explanation(
                product_name=product.name,
                growth_rate=growth_rate,
                consistency=consistency,
                turnover_proxy=turnover_proxy,
                average_demand=average_demand
            )
            
            recommendations.append(RecommendationItem(
                product_id=product.id,
                product_name=product.name,
                category=product.category,
                score=round(total_score, 2),
                explanation=explanation,
                metrics={
                    "growth_rate": round(growth_rate, 2),
                    "consistency": round(consistency, 2),
                    "turnover_proxy": round(turnover_proxy, 2),
                    "average_demand": round(average_demand, 2)
                }
            ))
        
        # Sort by score (descending)
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return recommendations
    
    def _generate_explanation(
        self,
        product_name: str,
        growth_rate: float,
        consistency: float,
        turnover_proxy: float,
        average_demand: float
    ) -> str:
        """Generate human-readable explanation for recommendation"""
        parts = []
        
        # Growth analysis
        if growth_rate > 10:
            parts.append(f"Strong demand growth ({growth_rate:.1f}% increase)")
        elif growth_rate > 0:
            parts.append(f"Moderate demand growth ({growth_rate:.1f}% increase)")
        elif growth_rate < -10:
            parts.append(f"Declining demand ({abs(growth_rate):.1f}% decrease)")
        else:
            parts.append("Stable demand")
        
        # Consistency analysis
        if consistency > 80:
            parts.append("highly consistent sales")
        elif consistency > 60:
            parts.append("moderately consistent sales")
        else:
            parts.append("variable sales patterns")
        
        # Turnover analysis
        if turnover_proxy > 70:
            parts.append("high stock turnover")
        elif turnover_proxy > 40:
            parts.append("moderate stock turnover")
        else:
            parts.append("low stock turnover")
        
        # Recommendation
        if growth_rate > 5 and consistency > 60:
            recommendation = "High investment value - consider increasing stock"
        elif growth_rate > 0 and turnover_proxy > 50:
            recommendation = "Good restocking candidate - maintain current levels"
        elif growth_rate < -5:
            recommendation = "Monitor closely - consider reducing inventory"
        else:
            recommendation = "Standard restocking - maintain baseline levels"
        
        explanation = f"{product_name} shows {', '.join(parts)}. {recommendation}."
        
        return explanation




