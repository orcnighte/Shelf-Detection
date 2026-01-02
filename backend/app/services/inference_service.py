"""
YOLO inference service for object detection
"""
import os
import numpy as np
from typing import List, Dict
import onnxruntime as ort
import cv2
from pathlib import Path


class InferenceService:
    """Service for running YOLO inference on images"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize inference service
        
        Args:
            model_path: Path to ONNX model file. If None, looks for model in models/ directory
        """
        if model_path is None:
            # Default model path
            model_path = os.getenv("MODEL_PATH", "models/yolov8_inventory.onnx")
        
        self.model_path = model_path
        self.session = None
        self.input_name = None
        self.output_names = None
        
        # Load model if it exists
        if os.path.exists(model_path):
            self._load_model()
        else:
            print(f"Warning: Model not found at {model_path}. Using mock inference.")
    
    def _load_model(self):
        """Load ONNX model"""
        try:
            self.session = ort.InferenceSession(self.model_path)
            self.input_name = self.session.get_inputs()[0].name
            self.output_names = [output.name for output in self.session.get_outputs()]
        except Exception as e:
            print(f"Error loading model: {e}")
            self.session = None
    
    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for YOLO inference
        
        Args:
            image_path: Path to input image
            
        Returns:
            Preprocessed image array
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Resize to YOLO input size (640x640)
        img_resized = cv2.resize(img, (640, 640))
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1] and convert to float32
        img_normalized = img_rgb.astype(np.float32) / 255.0
        
        # Convert to NCHW format (batch, channels, height, width)
        img_transposed = np.transpose(img_normalized, (2, 0, 1))
        img_batch = np.expand_dims(img_transposed, axis=0)
        
        return img_batch
    
    def _postprocess_output(self, outputs: List[np.ndarray], conf_threshold: float = 0.25) -> List[Dict]:
        """
        Postprocess YOLO output to extract detections
        
        Args:
            outputs: Model output arrays
            conf_threshold: Confidence threshold for detections
            
        Returns:
            List of detections with class, confidence, and bbox
        """
        # YOLO output format: [batch, num_detections, 85] where 85 = [x, y, w, h, conf, class_probs...]
        # For simplicity, we'll use a mock implementation
        # In production, implement proper NMS and parsing
        
        detections = []
        
        # Mock detection for demonstration
        # In production, parse actual YOLO output
        if len(outputs) > 0:
            output = outputs[0]
            # This is a placeholder - actual implementation would parse YOLO format
            pass
        
        return detections
    
    async def run_inference(self, image_path: str) -> List[Dict]:
        """
        Run inference on an image and return product counts
        
        Args:
            image_path: Path to input image
            
        Returns:
            List of detection results with product_name, count, and confidence
        """
        if self.session is None:
            # Mock inference for development
            return self._mock_inference(image_path)
        
        try:
            # Preprocess
            input_array = self._preprocess_image(image_path)
            
            # Run inference
            outputs = self.session.run(self.output_names, {self.input_name: input_array})
            
            # Postprocess
            detections = self._postprocess_output(outputs)
            
            # Count by class/product
            product_counts = {}
            for det in detections:
                class_name = det.get("class_name", "unknown")
                confidence = det.get("confidence", 0.0)
                
                if class_name not in product_counts:
                    product_counts[class_name] = {"count": 0, "confidences": []}
                
                product_counts[class_name]["count"] += 1
                product_counts[class_name]["confidences"].append(confidence)
            
            # Format results
            results = []
            for product_name, data in product_counts.items():
                avg_confidence = np.mean(data["confidences"])
                results.append({
                    "product_name": product_name,
                    "count": data["count"],
                    "confidence": float(avg_confidence)
                })
            
            return results
            
        except Exception as e:
            print(f"Error during inference: {e}")
            # Fallback to mock inference
            return self._mock_inference(image_path)
    
    def _mock_inference(self, image_path: str) -> List[Dict]:
        """
        Mock inference for development/testing
        Returns sample detections
        """
        # Mock products for demonstration
        mock_products = [
            {"product_name": "Coca Cola", "count": 12, "confidence": 0.85},
            {"product_name": "Pepsi", "count": 8, "confidence": 0.82},
            {"product_name": "Water Bottle", "count": 15, "confidence": 0.90},
            {"product_name": "Chips", "count": 6, "confidence": 0.78},
        ]
        
        # Return random subset for variety
        import random
        return random.sample(mock_products, k=random.randint(2, len(mock_products)))




