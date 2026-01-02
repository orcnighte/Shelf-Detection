"""
YOLO inference service for object detection
"""
import os
import numpy as np
from typing import List, Dict
import onnxruntime as ort
import cv2
from django.conf import settings


class InferenceService:
    """Service for running YOLO inference on images"""
    
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = getattr(settings, 'MODEL_PATH', 'models/yolov8_inventory.onnx')
        
        self.model_path = model_path
        self.session = None
        
        if os.path.exists(model_path):
            self._load_model()
        else:
            print(f"Warning: Model not found at {model_path}. Using mock inference.")
    
    def _load_model(self):
        """Load ONNX model"""
        try:
            self.session = ort.InferenceSession(self.model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.session = None
    
    def run_inference(self, image_path: str) -> List[Dict]:
        """Run inference on an image and return product counts"""
        if self.session is None:
            return self._mock_inference(image_path)
        
        # TODO: Implement actual YOLO inference
        # For now, return mock results
        return self._mock_inference(image_path)
    
    def _mock_inference(self, image_path: str) -> List[Dict]:
        """Mock inference for development/testing"""
        import random
        mock_products = [
            {"product_name": "Coca Cola", "count": 12, "confidence": 0.85},
            {"product_name": "Pepsi", "count": 8, "confidence": 0.82},
            {"product_name": "Water Bottle", "count": 15, "confidence": 0.90},
            {"product_name": "Chips", "count": 6, "confidence": 0.78},
        ]
        return random.sample(mock_products, k=random.randint(2, len(mock_products)))


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



