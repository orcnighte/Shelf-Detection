# Inventory Management System

An Android application with backend API that automatically captures shelf images, detects and counts products using YOLO object detection, stores historical data, and provides analytics and recommendations.

## Project Structure

```
inventory/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── database.py  # Database configuration
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── schemas.py   # Pydantic schemas
│   │   ├── routers/     # API endpoints
│   │   └── services/    # Business logic services
│   └── requirements.txt
├── android/              # Android application
│   └── app/
│       └── src/main/
│           ├── java/com/inventory/app/
│           └── res/
├── model/                # YOLO model training
│   ├── train_yolo.py
│   └── prepare_dataset.py
└── docker-compose.yml    # Docker orchestration
```

## Features

### Android App
- **Camera Integration**: Uses CameraX to capture shelf images
- **Daily Automation**: WorkManager schedules daily image capture
- **Manual Capture**: Users can manually capture images
- **Analytics Dashboard**: View weekly analytics with charts
- **Recommendations**: Get weekly investment and restocking recommendations

### Backend API
- **Image Processing**: Receives images and runs YOLO inference
- **Product Detection**: Detects and counts products in images
- **Data Storage**: PostgreSQL database for historical data
- **Analytics Engine**: Calculates demand, growth, and consistency metrics
- **Recommendation Engine**: Generates data-driven recommendations

### AI Model
- **YOLOv8**: Object detection model for product recognition
- **ONNX Runtime**: Optimized inference engine
- **Training Scripts**: Utilities for model training and dataset preparation

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Android Studio (for Android development)
- Docker and Docker Compose (for deployment)
- PyTorch (for model training)

## Setup Instructions

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventory_db
   STORAGE_TYPE=local
   LOCAL_STORAGE_PATH=storage/images
   MODEL_PATH=models/yolov8_inventory.onnx
   ```

3. **Initialize database:**
   ```bash
   # The database tables will be created automatically on first run
   ```

4. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **Check logs:**
   ```bash
   docker-compose logs -f backend
   ```

3. **Access API:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Model Training

1. **Prepare dataset:**
   ```bash
   cd model
   python prepare_dataset.py --base-path dataset --create-yaml
   ```

2. **Add your images and labels:**
   - Place training images in `dataset/images/train/`
   - Place corresponding YOLO format labels in `dataset/labels/train/`
   - Place validation images in `dataset/images/val/`
   - Place validation labels in `dataset/labels/val/`

3. **Train the model:**
   ```bash
   python train_yolo.py --data data.yaml --epochs 100 --batch 16
   ```

4. **Export to ONNX:**
   The training script automatically exports the model to ONNX format.

### Android App Setup

1. **Open project in Android Studio:**
   - Open the `android` directory in Android Studio

2. **Update API endpoint:**
   - In `InventoryRepository.kt`, update the `baseUrl`:
     - For emulator: `http://10.0.2.2:8000/`
     - For physical device: `http://YOUR_COMPUTER_IP:8000/`

3. **Build and run:**
   - Sync Gradle files
   - Build the project
   - Run on device or emulator

## API Endpoints

### Images
- `POST /api/v1/images/upload` - Upload and process image
- `GET /api/v1/images` - Get recent images

### Products
- `GET /api/v1/products` - Get all products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products/{id}/counts` - Get product counts

### Analytics
- `GET /api/v1/analytics/weekly` - Get weekly analytics
- `GET /api/v1/analytics/daily` - Get daily summary

### Recommendations
- `GET /api/v1/recommendations/weekly` - Get weekly recommendations

## Database Schema

### Products
- `id` (Integer, Primary Key)
- `name` (String)
- `category` (String, Optional)

### Daily Counts
- `id` (Integer, Primary Key)
- `product_id` (Integer, Foreign Key)
- `date` (Date)
- `count` (Integer)

### Images
- `image_id` (Integer, Primary Key)
- `date` (DateTime)
- `path` (String)
- `confidence_summary` (String, Optional)

## Analytics Metrics

- **Average Daily Demand**: Mean count over the period
- **Growth Rate**: Percentage change in demand (linear regression)
- **Demand Consistency**: Coefficient of variation (lower = more consistent)

## Recommendation Scoring

Products are ranked based on:
- **Growth Rate** (30% weight): Positive growth indicates increasing demand
- **Consistency** (30% weight): Lower variation indicates stable demand
- **Stock Turnover Proxy** (40% weight): Ratio of average demand to max count

## Development Notes

### Mock Inference
The inference service includes a mock mode for development when no trained model is available. Replace with actual YOLO model for production.

### Background Tasks
The Android app uses WorkManager for daily image capture. Note that background camera access requires additional permissions and setup.

### Storage
Currently configured for local storage. Update `StorageService` to use S3 or Google Cloud Storage for production.

## License

This project is provided as-is for development purposes.




