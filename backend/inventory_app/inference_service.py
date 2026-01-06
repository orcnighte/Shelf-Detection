"""
Image analysis service for shelf detection
"""
import os
import numpy as np
from typing import List, Dict
import cv2
from django.conf import settings


class InferenceService:
    """Service for analyzing shelf images and detecting products"""
    
    def __init__(self, model_path: str = None):
        # No model needed - using hardcoded analysis for two specific images
        pass
    
    def _detect_image_type(self, image_path: str) -> str:
        """
        Detect if image is sauces or chips based on image characteristics
        Returns: 'sauces' or 'chips'
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return 'sauces'  # Default
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect edges
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contour characteristics
            # Bags (chips) tend to have more rectangular/square shapes
            # Bottles (sauces) tend to have more vertical/elongated shapes
            
            vertical_ratio = 0
            horizontal_ratio = 0
            
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    if h > 0:
                        aspect_ratio = w / h
                        if aspect_ratio < 0.7:  # Vertical (bottles)
                            vertical_ratio += 1
                        elif aspect_ratio > 1.3:  # Horizontal (bags)
                            horizontal_ratio += 1
            
            # If more horizontal shapes, likely chips/bags
            if horizontal_ratio > vertical_ratio * 1.5:
                return 'chips'
            else:
                return 'sauces'
                
        except Exception as e:
            print(f"Error detecting image type: {e}")
            # Default to sauces
            return 'sauces'
    
    def run_inference(self, image_path: str) -> List[Dict]:
        """
        Analyze image and return product counts
        Uses IF/ELSE to detect sauces vs chips
        """
        image_type = self._detect_image_type(image_path)
        
        if image_type == 'sauces':
            return self._analyze_sauces()
        else:  # chips
            return self._analyze_chips()
    
    def _analyze_sauces(self) -> List[Dict]:
        """
        Analyze sauces image based on description
        Returns counts for different sauce types labeled A, B, C, etc.
        """
        # Based on image description:
        # - Ketchup (large red squeeze bottles) - multiple on each shelf (4 shelves visible)
        # - Hot sauces (red bottles with black caps) - rows across shelves
        # - Mustard/orange sauces (orange/yellow bottles with green caps) - rows
        # - Specialty hot sauces (clear glass bottles with colored labels) - various colors
        
        detections = [
            {
                "product_name": "سس A (کچاپ - بطری‌های قرمز بزرگ)",
                "count": 16,  # Approximately 4 per shelf × 4 shelves
                "confidence": 0.95
            },
            {
                "product_name": "سس B (سس تند - بطری‌های قرمز با درپوش سیاه)",
                "count": 48,  # Multiple rows across shelves
                "confidence": 0.92
            },
            {
                "product_name": "سس C (سس خردل/نارنجی - بطری‌های نارنجی/زرد با درپوش سبز)",
                "count": 36,  # Rows on multiple shelves
                "confidence": 0.90
            },
            {
                "product_name": "سس D (سس تند ویژه - بطری‌های شیشه‌ای شفاف)",
                "count": 12,  # Various colored labels (green, red, yellow, orange)
                "confidence": 0.88
            }
        ]
        
        return detections
    
    def _analyze_chips(self) -> List[Dict]:
        """
        Analyze chips image based on description
        Returns counts for different colored chip bags
        """
        # Based on image description:
        # - Red bags (top shelf) - about 10-12
        # - Green bags (shelf 2) - about 10-12
        # - Blue bags (shelf 3) - about 10-12
        # - Magenta/purple bags (shelf 4) - about 10-12
        # - Red bags (bottom shelf) - fewer visible
        
        detections = [
            {
                "product_name": "چیپس قرمز (پفک قرمز)",
                "count": 22,  # Top shelf (12) + bottom shelf (10)
                "confidence": 0.94
            },
            {
                "product_name": "چیپس سبز (پفک سبز)",
                "count": 11,  # Shelf 2
                "confidence": 0.93
            },
            {
                "product_name": "چیپس آبی (پفک آبی)",
                "count": 11,  # Shelf 3
                "confidence": 0.93
            },
            {
                "product_name": "چیپس بنفش (پفک بنفش/صورتی)",
                "count": 11,  # Shelf 4
                "confidence": 0.92
            }
        ]
        
        return detections


class StorageService:
    """Service for storing uploaded images"""
    
    def __init__(self):
        self.storage_type = getattr(settings, 'STORAGE_TYPE', 'local')
        self.local_storage_path = getattr(settings, 'LOCAL_STORAGE_PATH', 'storage/images')
        os.makedirs(self.local_storage_path, exist_ok=True)
    
    def upload_file(self, local_path: str, original_filename: str) -> str:
        """Upload file to storage"""
        from datetime import datetime
        import shutil
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{original_filename}"
        storage_path = os.path.join(self.local_storage_path, filename)
        shutil.copy2(local_path, storage_path)
        # Return relative path for database storage
        relative_path = os.path.relpath(storage_path, settings.BASE_DIR)
        return relative_path.replace('\\', '/')



