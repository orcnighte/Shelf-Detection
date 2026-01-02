# YOLO Model Training

## Dataset Preparation

1. **Create dataset structure:**
   ```bash
   python prepare_dataset.py --base-path dataset --create-yaml
   ```

2. **Organize your images:**
   - Training images: `dataset/images/train/`
   - Validation images: `dataset/images/val/`
   - Test images: `dataset/images/test/`

3. **Create YOLO format labels:**
   - Each image needs a corresponding `.txt` file
   - Format: `class_id center_x center_y width height` (normalized 0-1)
   - Labels directory: `dataset/labels/train/`, `dataset/labels/val/`

4. **Update `data.yaml`:**
   - Set correct paths
   - Define your class names
   - Set number of classes

## Training

```bash
python train_yolo.py --data data.yaml --epochs 100 --batch 16 --model yolov8n.pt
```

### Parameters:
- `--data`: Path to data.yaml
- `--epochs`: Number of training epochs (default: 100)
- `--imgsz`: Image size (default: 640)
- `--batch`: Batch size (default: 16)
- `--model`: Base model (yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt)

## Model Export

The training script automatically exports the model to ONNX format. The exported model will be:
- `runs/detect/inventory_detection/weights/best.onnx`
- Copied to `../backend/models/yolov8_inventory.onnx`

## Labeling Tools

Recommended tools for creating YOLO format labels:
- [LabelImg](https://github.com/tzutalin/labelImg)
- [Roboflow](https://roboflow.com/)
- [CVAT](https://github.com/openvinotoolkit/cvat)

## Tips

- Start with a pre-trained YOLOv8 model (yolov8n.pt for faster training)
- Use data augmentation for better generalization
- Monitor validation metrics to avoid overfitting
- Export to ONNX for optimized inference




