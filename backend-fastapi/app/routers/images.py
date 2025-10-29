from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse, SimilarImagesResponse
from app.services.image_service import image_service

router = APIRouter(prefix="/api", tags=["images"])


@router.post("/upload", response_model=UploadResponse)
async def upload_image(image: UploadFile = File(...)):
    """
    Upload an image for similarity search
    
    - **image**: Image file (jpg, png, etc.)
    
    Returns the image_id to use for fetching similar images
    """
    # Validate file type
    # if not image.content_type.startswith("image/"):
    #     raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save image and get ID
    image_id = image_service.upload_image(
        file=image.file,
        filename=image.filename
    )
    
    return UploadResponse(
        image_id=image_id,
        filename=image.filename
    )


@router.post("/upload-product-image", response_model=UploadResponse)
async def upload_product_image(image: UploadFile = File(...)):
    """
    Upload a product image for storage and embedding storage
    
    - **image**: Image file (jpg, png, etc.)
    
    Returns the product image_id
    """
    
    # Save image and get ID
    image_id = image_service.upload_product_image(
        file=image.file,
        filename=image.filename
    )
    
    return UploadResponse(
        image_id=image_id,
        filename=image.filename
    )


@router.get("/similar/{image_id}", response_model=SimilarImagesResponse)
async def get_similar_images(image_id: str):
    """
    Get similar images for a given image_id
    
    - **image_id**: The ID returned from the upload endpoint
    
    Returns a list of similar images with similarity scores
    """
    similar_images = image_service.find_similar_images(image_id)
    
    return SimilarImagesResponse(similar_images=similar_images)
