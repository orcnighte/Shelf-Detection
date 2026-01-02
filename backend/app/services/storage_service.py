"""
Storage service for image uploads (S3 or local)
"""
import os
import boto3
from datetime import datetime
from typing import Optional
from botocore.exceptions import ClientError


class StorageService:
    """Service for storing uploaded images"""
    
    def __init__(self):
        """Initialize storage service"""
        self.storage_type = os.getenv("STORAGE_TYPE", "local")  # "local" or "s3"
        self.local_storage_path = os.getenv("LOCAL_STORAGE_PATH", "storage/images")
        self.s3_bucket = os.getenv("S3_BUCKET", None)
        self.s3_client = None
        
        # Create local storage directory if needed
        if self.storage_type == "local":
            os.makedirs(self.local_storage_path, exist_ok=True)
        
        # Initialize S3 client if using S3
        if self.storage_type == "s3" and self.s3_bucket:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
    
    async def upload_file(self, local_path: str, original_filename: str) -> str:
        """
        Upload file to storage
        
        Args:
            local_path: Local file path
            original_filename: Original filename
            
        Returns:
            Storage path (S3 key or local path)
        """
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = os.path.splitext(original_filename)[1]
        filename = f"{timestamp}_{original_filename}"
        
        if self.storage_type == "s3" and self.s3_client:
            # Upload to S3
            s3_key = f"images/{filename}"
            try:
                self.s3_client.upload_file(local_path, self.s3_bucket, s3_key)
                return f"s3://{self.s3_bucket}/{s3_key}"
            except ClientError as e:
                raise Exception(f"Failed to upload to S3: {e}")
        else:
            # Store locally
            storage_path = os.path.join(self.local_storage_path, filename)
            import shutil
            shutil.copy2(local_path, storage_path)
            return storage_path




