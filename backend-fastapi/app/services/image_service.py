import boto3
import uuid
import os
import io
from PIL import Image as PILImage
import pillow_avif
from fastapi import HTTPException
from typing import List
from app.models.schemas import SimilarImage
from app.services.embedding_service import embedding_service
from app.services.database_service import database_service

from botocore.client import Config
import base64
import requests
from requests_aws4auth import AWS4Auth

MINIO_ENDPOINT_URL = os.environ.get("MINIO_ENDPOINT_URL", "http://localhost:9000")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin")
REGION_NAME = os.environ.get("REGION_NAME", "us-east-1")

class ImageService:
    """Service layer for image operations using MinIO and Database"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
            config=Config(
                signature_version='s3v4',
                s3={
                    'addressing_style': 'path',
                    'payload_signing_enabled': False
                }
            )
        )
        self.uploads_bucket_name = 'uploads'
        self.products_bucket_name = 'products'
        self.base_url = MINIO_ENDPOINT_URL


    def _save_image_to_minio(self, file_body, unique_filename: str, bucket_name: str) -> str:
        """
        Save image object to Oracle Object Storage (S3-compatible) and return image_id (the S3 key)
        """
        try:
            # Read image data fully into memory
            file_body.seek(0)
            data = file_body.read()
            size = len(data)

            if size == 0:
                raise ValueError("File is empty")

            # Use direct HTTP request with explicit Content-Length
            url = f"{self.base_url}/{bucket_name}/{unique_filename}"
            
            auth = AWS4Auth(
                AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY,
                REGION_NAME,
                's3'
            )
            
            headers = {
                'Content-Type': 'image/jpeg',
                'Content-Length': str(size)
            }
            
            response = requests.put(
                url,
                data=data,
                headers=headers,
                auth=auth
            )
            
            if response.status_code not in [200, 201, 204]:
                raise Exception(f"Upload failed with status {response.status_code}: {response.text}")

            print(f"✅ Uploaded {unique_filename} ({size} bytes) to bucket '{bucket_name}'")
            return unique_filename

        except Exception as e:
            print(f"❌ Upload failed for {unique_filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to upload {unique_filename}: {e}")



    def _process_and_standardize_image(self, file_stream, original_filename: str):
        """
        Tries to open a file stream as an image, converts it to JPEG,
        and returns the image data and a new unique filename.
        Raises HTTPException if the file is not a valid image.
        """
        try:
            img = PILImage.open(file_stream)
            
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            buffer.seek(0)
            
            base_filename, _ = os.path.splitext(original_filename)
            unique_filename = f"{uuid.uuid4()}_{base_filename}.jpg"

            return buffer, unique_filename
        except Exception as e:
            print(f"Failed to process file as image: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid or unsupported image file: {original_filename}")

    def upload_image(self, file, filename: str) -> str:
        """
        Orchestrates the user image upload process:
        1. Converts the image to JPEG.
        2. Saves the standardized image file to MinIO storage.
        3. Generates an embedding for the image.
        4. Saves the image ID and its embedding to the database.
        """
        jpeg_buffer, image_id = self._process_and_standardize_image(file, filename)
        
        self._save_image_to_minio(jpeg_buffer, image_id, self.uploads_bucket_name)
        
        try:
            image_url = f"{self.base_url}/{self.uploads_bucket_name}/{image_id}"
            embedding = embedding_service.encode_image_from_url(image_url)

            if embedding is None:
                raise Exception("Failed to generate embedding for the image.")

            database_service.save_image_embedding(image_id, embedding)
            
            print(f"Successfully processed and stored image {image_id}")
            return image_id

        except Exception as e:
            print(f"Error during image processing for {image_id}. Rolling back MinIO upload.")
            self.s3_client.delete_object(Bucket=self.uploads_bucket_name, Key=image_id)
            print(f"Deleted {image_id} from MinIO.")
            raise e

    def upload_product_image(self, file, filename: str) -> str:
        """
        Orchestrates the product image upload process:
        1. Converts the image to JPEG.
        2. Saves the standardized image file to MinIO storage.
        3. Generates an embedding for the image.
        4. Saves the image ID and its embedding to the database.
        """
        jpeg_buffer, image_id = self._process_and_standardize_image(file, filename)

        self._save_image_to_minio(jpeg_buffer, image_id, self.products_bucket_name)
        
        try:
            image_url = f"{self.base_url}/{self.products_bucket_name}/{image_id}"
            embedding = embedding_service.encode_image_from_url(image_url)

            if embedding is None:
                raise Exception("Failed to generate embedding for the image.")

            database_service.save_product_image_embedding(image_id, embedding)
            
            print(f"Successfully processed and stored image {image_id}")
            return image_id

        except Exception as e:
            print(f"Error during image processing for {image_id}. Rolling back MinIO upload.")
            self.s3_client.delete_object(Bucket=self.products_bucket_name, Key=image_id)
            print(f"Deleted {image_id} from MinIO.")
            raise e

    def find_similar_images(self, image_id: str, top_k: int = 5) -> List[SimilarImage]:
        """
        Finds similar images by:
        1. Getting the embedding for the given image_id.
        2. Using the database service to find similar image vectors.
        3. Constructing the response with image URLs.
        """
        
        image_url = f"{self.base_url}/{self.uploads_bucket_name}/{image_id}"
        query_embedding = embedding_service.encode_image_from_url(image_url)
        
        if query_embedding is None:
            print(f"Could not generate embedding for image {image_id}")
            return []

        similar_results = database_service.find_similar_images(query_embedding, top_k=top_k + 1)
        
        similar_images = []
        for result in similar_results:
            found_image_id = result["id"]
            
            if found_image_id == image_id:
                continue

            url = f"{self.base_url}/{self.products_bucket_name}/{found_image_id}"
            similar_images.append(SimilarImage(
                id=found_image_id,
                url=url,
                thumbnail=url,
                similarity=result["similarity"],
                name=found_image_id
            ))

            if len(similar_images) == top_k:
                break
            
        print(f"Found {len(similar_images)} similar images for: {image_id}")
        return similar_images

# Singleton instance
image_service = ImageService()