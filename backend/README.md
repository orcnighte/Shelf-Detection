# Backend API Documentation

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Services

### Inference Service
- Handles YOLO model inference
- Supports ONNX runtime
- Falls back to mock inference if model not found

### Storage Service
- Supports local file storage
- Can be configured for S3 or Google Cloud Storage

### Analytics Service
- Calculates demand metrics
- Computes growth rates
- Analyzes consistency

### Recommendation Service
- Generates product recommendations
- Scores products based on multiple factors
- Provides explanations for recommendations

## Database Migrations

The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for migrations.

## Testing

```bash
# Run tests (when implemented)
pytest
```

## Deployment

See `docker-compose.yml` for containerized deployment.




