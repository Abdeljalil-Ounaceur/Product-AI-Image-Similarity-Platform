import numpy as np
from PIL import Image
from typing import Optional
import requests
import io
import os

ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL", "http://localhost:3000")


class EmbeddingService:
    """Service for encoding images using BentoML CLIP service"""

    def __init__(self, ml_service_url: str = ML_SERVICE_URL):
        self.ml_service_url = ml_service_url

    def encode_image_from_url(self, image_url: str) -> Optional[np.ndarray]:
        """
        Download image from MinIO URL and encode it using CLIP model
        Returns 512-dimensional embedding vector
        """
        try:
            # Download image from MinIO
            response = requests.get(image_url)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))

            # Convert image to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()

            # Send as multipart form data directly to BentoML service
            files = {'items': ('image.png', img_bytes, 'image/png')}
            api_response = requests.post(
                f"{self.ml_service_url}/encode_image",
                files=files
            )
            api_response.raise_for_status()

            # BentoML returns the result as-is (numpy array)
            result = api_response.json()
            return np.array(result)

        except Exception as e:
            print(f"Error encoding image {image_url}: {e}")
            return None

   
# Singleton instance
embedding_service = EmbeddingService()
