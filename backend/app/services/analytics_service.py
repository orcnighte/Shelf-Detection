"""
Analytics service for data analysis
"""
import numpy as np
import pandas as pd
from typing import List
from datetime import date
from app.schemas import AnalyticsSummary


class AnalyticsService:
    """Service for calculating analytics metrics"""
    
    def calculate_product_analytics(
        self,
        product_id: int,
        product_name: str,
        counts: List[int],
        dates: List[date]
    ) -> AnalyticsSummary:
        """
        Calculate analytics metrics for a product
        
        Args:
            product_id: Product ID
            product_name: Product name
            counts: List of daily counts
            dates: List of corresponding dates
            
        Returns:
            AnalyticsSummary with calculated metrics
        """
        counts_array = np.array(counts)
        
        # Average daily demand
        average_daily_demand = float(np.mean(counts_array))
        
        # Growth rate (linear regression slope / average)
        if len(counts) >= 2:
            x = np.arange(len(counts))
            slope = np.polyfit(x, counts_array, 1)[0]
            growth_rate = (slope / average_daily_demand) * 100 if average_daily_demand > 0 else 0
        else:
            growth_rate = 0.0
        
        # Demand consistency (coefficient of variation)
        std_dev = np.std(counts_array)
        demand_consistency = (std_dev / average_daily_demand) * 100 if average_daily_demand > 0 else 0
        
        # Total count
        total_count = int(np.sum(counts_array))
        
        return AnalyticsSummary(
            product_id=product_id,
            product_name=product_name,
            average_daily_demand=average_daily_demand,
            growth_rate=growth_rate,
            demand_consistency=demand_consistency,
            total_count=total_count,
            days_analyzed=len(counts)
        )
    
    def calculate_trend(self, counts: List[int]) -> str:
        """
        Determine trend direction
        
        Args:
            counts: List of daily counts
            
        Returns:
            Trend description: "increasing", "decreasing", or "stable"
        """
        if len(counts) < 2:
            return "stable"
        
        # Simple trend detection
        first_half = np.mean(counts[:len(counts)//2])
        second_half = np.mean(counts[len(counts)//2:])
        
        diff = second_half - first_half
        threshold = np.std(counts) * 0.5
        
        if diff > threshold:
            return "increasing"
        elif diff < -threshold:
            return "decreasing"
        else:
            return "stable"




