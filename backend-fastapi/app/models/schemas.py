from pydantic import BaseModel
from typing import Optional


class UploadResponse(BaseModel):
    """Response after uploading an image"""
    image_id: str
    message: Optional[str] = "Image uploaded successfully"
    filename: Optional[str] = None


class SimilarImage(BaseModel):
    """Single similar image result"""
    id: str
    url: str
    thumbnail: Optional[str] = None
    similarity: float  # 0.0 to 1.0
    name: Optional[str] = None


class SimilarImagesResponse(BaseModel):
    """Response containing list of similar images"""
    similar_images: list[SimilarImage]
