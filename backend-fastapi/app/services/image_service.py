import boto3
import random
import uuid
from typing import List
from app.models.schemas import SimilarImage
from app.services.embedding_service import embedding_service

MINIO_ENDPOINT_URL = "http://localhost:9000"

class ImageService:
    """Service layer for image operations using MinIO storage"""
    
    def __init__(self):
        # MinIO connection settings
        self.s3_client = boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT_URL,
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            region_name='us-east-1'
        )
        self.bucket_name = 'uploads'
        self.base_url = 'http://localhost:9000'
    
    def save_uploaded_image(self, file, filename: str) -> str:
        """
        Save uploaded image to MinIO and return image_id (the S3 key)
        """
        # Generate unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Upload to MinIO
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=unique_filename,
            Body=file,
            ContentType='image/jpeg'
        )
        
        print(f"[MinIO] Uploaded image: {unique_filename}")
        return unique_filename
    
    def find_similar_images(self, image_id: str) -> List[SimilarImage]:
        """
        Find similar images - currently returns random 5 from MinIO bucket
        
        Later: Will use ML model to find actually similar images
        """
        
        image_url = f"{self.base_url}/{self.bucket_name}/{image_id}"
        vector = embedding_service.encode_image_from_url(image_url)
        print(vector)

        # List all images in bucket
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        all_files = [obj['Key'] for obj in response.get('Contents', [])]
        
        # Get random 5 (or less if bucket has fewer images)
        random_files = random.sample(all_files, min(5, len(all_files)))
        
        # Build response with MinIO URLs
        similar_images = []
        for i, filename in enumerate(random_files):
            url = f"{self.base_url}/{self.bucket_name}/{filename}"
            similar_images.append(SimilarImage(
                id=filename,
                url=url,
                thumbnail=url,  # Same as URL for now
                similarity=round(0.95 - (i * 0.05), 2),  # Fake similarity scores
                name=filename
            ))
        
        print(f"[MinIO] Found {len(similar_images)} images for: {image_id}")
        return similar_images


# Singleton instance
image_service = ImageService()
