import random
from typing import List
from app.models.schemas import SimilarImage


# Mock data - using reliable placeholder images
MOCK_IMAGES = [
    {
        "id": "img_001",
        "url": "https://picsum.photos/id/237/400/400",  # Dog
        "thumbnail": "https://picsum.photos/id/237/120/120",
        "similarity": 0.95,
        "name": "similar_product_001.jpg"
    },
    {
        "id": "img_002",
        "url": "https://picsum.photos/id/10/400/400",  # Forest
        "thumbnail": "https://picsum.photos/id/10/120/120",
        "similarity": 0.89,
        "name": "similar_product_002.jpg"
    },
    {
        "id": "img_003",
        "url": "https://picsum.photos/id/20/400/400",  # Mountain
        "thumbnail": "https://picsum.photos/id/20/120/120",
        "similarity": 0.84,
        "name": "similar_product_003.jpg"
    },
    {
        "id": "img_004",
        "url": "https://picsum.photos/id/30/400/400",  # Workspace
        "thumbnail": "https://picsum.photos/id/30/120/120",
        "similarity": 0.78,
        "name": "similar_product_004.jpg"
    },
    {
        "id": "img_005",
        "url": "https://picsum.photos/id/40/400/400",  # Cat
        "thumbnail": "https://picsum.photos/id/40/120/120",
        "similarity": 0.72,
        "name": "similar_product_005.jpg"
    }
]


class ImageService:
    """Service layer for image operations - currently using mock data"""
    
    def save_uploaded_image(self, file, filename: str) -> str:
        """
        Save uploaded image and return image_id
        
        MOCK: Just generates a fake ID without actually saving
        REAL: Will save to storage (MinIO/S3) and return the storage key
        """
        # Mock implementation
        image_id = f"mock_{random.randint(1000, 9999)}"
        print(f"[MOCK] Saved image: {filename} with ID: {image_id}")
        return image_id
    
    def find_similar_images(self, image_id: str) -> List[SimilarImage]:
        """
        Find similar images for the given image_id
        
        MOCK: Returns shuffled mock data
        REAL: Will:
          1. Load image from storage using image_id
          2. Generate embeddings using ML model
          3. Search vector database for similar embeddings
          4. Return top N similar images with scores
        """
        # Mock implementation - shuffle and return
        shuffled = random.sample(MOCK_IMAGES, len(MOCK_IMAGES))
        similar_images = [SimilarImage(**img) for img in shuffled]
        
        print(f"[MOCK] Found {len(similar_images)} similar images for: {image_id}")
        return similar_images


# Singleton instance
image_service = ImageService()
