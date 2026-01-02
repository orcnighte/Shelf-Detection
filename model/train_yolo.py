"""
YOLOv8 training script for inventory product detection
"""
import os
from ultralytics import YOLO
import torch


def train_model(
    data_yaml: str = "data.yaml",
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    model_name: str = "yolov8n.pt"
):
    """
    Train YOLOv8 model for product detection
    
    Args:
        data_yaml: Path to dataset configuration YAML
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size
        model_name: Base model name (yolov8n.pt, yolov8s.pt, yolov8m.pt, etc.)
    """
    # Initialize model
    model = YOLO(model_name)
    
    # Train the model
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        name="inventory_detection",
        project="runs/detect",
        save=True,
        plots=True
    )
    
    # Export to ONNX
    model_path = f"runs/detect/inventory_detection/weights/best.pt"
    if os.path.exists(model_path):
        model_export = YOLO(model_path)
        onnx_path = model_export.export(format="onnx", imgsz=imgsz)
        print(f"Model exported to ONNX: {onnx_path}")
        
        # Copy to models directory
        import shutil
        os.makedirs("../backend/models", exist_ok=True)
        shutil.copy(onnx_path, "../backend/models/yolov8_inventory.onnx")
        print(f"Model copied to backend/models/yolov8_inventory.onnx")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train YOLOv8 model for inventory detection")
    parser.add_argument("--data", type=str, default="data.yaml", help="Path to data.yaml")
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Base model")
    
    args = parser.parse_args()
    
    train_model(
        data_yaml=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        model_name=args.model
    )




