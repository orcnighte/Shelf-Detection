"""
Image upload and processing endpoints
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os
from app.database import get_db
from app.models import Image, Product, DailyCount
from app.schemas import ImageUploadResponse, DetectionResult
from app.services.inference_service import InferenceService
from app.services.storage_service import StorageService
from typing import List

router = APIRouter()

# Initialize services
inference_service = InferenceService()
storage_service = StorageService()


@router.post("/images/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a shelf image, run YOLO inference, and store results
    """
    try:
        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Run inference
            import time
            start_time = time.time()
            detections = await inference_service.run_inference(tmp_path)
            processing_time = time.time() - start_time

            # Upload to storage (S3 or local)
            storage_path = await storage_service.upload_file(tmp_path, file.filename)

            # Save image metadata
            confidence_summary = str({d["product_name"]: d["confidence"] for d in detections})
            db_image = Image(
                date=datetime.now(),
                path=storage_path,
                confidence_summary=confidence_summary
            )
            db.add(db_image)
            db.flush()

            # Update daily counts
            today = datetime.now().date()
            detection_results = []
            total_products = 0

            for detection in detections:
                product_name = detection["product_name"]
                count = detection["count"]
                confidence = detection["confidence"]

                # Get or create product
                product = db.query(Product).filter(Product.name == product_name).first()
                if not product:
                    product = Product(name=product_name, category=None)
                    db.add(product)
                    db.flush()

                # Update or create daily count
                daily_count = db.query(DailyCount).filter(
                    DailyCount.product_id == product.id,
                    DailyCount.date == today
                ).first()

                if daily_count:
                    daily_count.count = count
                else:
                    daily_count = DailyCount(
                        product_id=product.id,
                        date=today,
                        count=count
                    )
                    db.add(daily_count)

                detection_results.append(DetectionResult(
                    product_name=product_name,
                    count=count,
                    confidence=confidence
                ))
                total_products += count

            db.commit()

            return ImageUploadResponse(
                image_id=db_image.image_id,
                detections=detection_results,
                total_products=total_products,
                processing_time=processing_time
            )

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@router.get("/images")
async def get_images(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent images"""
    images = db.query(Image).order_by(Image.date.desc()).limit(limit).all()
    return images




