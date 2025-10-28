import boto3
import uuid
from typing import List
from app.models.schemas import SimilarImage
from app.services.embedding_service import embedding_service
from app.services.database_service import database_service

MINIO_ENDPOINT_URL = "http://localhost:9000"

class ImageService:
    """Service layer for image operations using MinIO and Database"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT_URL,
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            region_name='us-east-1'
        )
        self.bucket_name = 'uploads'
        self.base_url = 'http://localhost:9000'
    
    def _save_image_to_minio(self, file, filename: str) -> str:
        """
        Save uploaded image to MinIO and return image_id (the S3 key)
        """
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=unique_filename,
            Body=file,
            ContentType='image/jpeg'
        )
        
        print(f"[MinIO] Uploaded image: {unique_filename}")
        return unique_filename

    def upload_image(self, file, filename: str) -> str:
        """
        Orchestrates the image upload process:
        1. Saves the image file to MinIO storage.
        2. Generates an embedding for the image.
        3. Saves the image ID and its embedding to the database.
        If any step fails, it attempts to roll back previous steps.
        Returns the unique image ID.
        """
        image_id = self._save_image_to_minio(file, filename)
        
        try:
            image_url = f"{self.base_url}/{self.bucket_name}/{image_id}"
            embedding = embedding_service.encode_image_from_url(image_url)

            if embedding is None:
                raise Exception("Failed to generate embedding for the image.")

            database_service.save_image_embedding(image_id, embedding)
            
            print(f"Successfully processed and stored image {image_id}")
            return image_id

        except Exception as e:
            print(f"Error during image processing for {image_id}. Rolling back MinIO upload.")
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=image_id)
            print(f"Deleted {image_id} from MinIO.")
            # Re-raise the exception to be handled by the FastAPI router
            raise e

    def find_similar_images(self, image_id: str, top_k: int = 5) -> List[SimilarImage]:
        """
        Finds similar images by:
        1. Getting the embedding for the given image_id.
        2. Using the database service to find similar image vectors.
        3. Constructing the response with image URLs.
        """
        
        image_url = f"{self.base_url}/{self.bucket_name}/{image_id}"
        query_embedding = embedding_service.encode_image_from_url(image_url)
        
        if query_embedding is None:
            print(f"Could not generate embedding for image {image_id}")
            return []

        # Ask for top_k + 1 results to exclude the query image itself
        similar_results = database_service.find_similar_images(query_embedding, top_k=top_k + 1)
        
        similar_images = []
        for result in similar_results:
            found_image_id = result["id"]
            
            if found_image_id == image_id:
                continue

            url = f"{self.base_url}/{self.bucket_name}/{found_image_id}"
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
