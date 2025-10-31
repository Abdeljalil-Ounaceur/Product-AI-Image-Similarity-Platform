import os
import requests
import glob
import mimetypes
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("BASE_URL","http://localhost:8000")
UPLOAD_URL = f"{BASE_URL}/api/upload-product-image"

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "seed_data", "images")

def populate_products():
    """
    Finds images in the seed_data/images directory and uploads them
    as product images using the API.
    """
    image_extensions = ["*.png", "*.jpg", "*.jpeg","*.webp","*.avif"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
    
    if not image_paths:
        print(f"No images found in {IMAGE_DIR}. Please add images to this directory.")
        return

    print(f"Found {len(image_paths)} images to upload.")

    for image_path in image_paths:
        filename = os.path.basename(image_path)
        content_type, _ = mimetypes.guess_type(image_path)
        if not content_type:
            content_type = "application/octet-stream"

        with open(image_path, "rb") as f:
            files = {"image": (filename, f, content_type)}
            try:
                response = requests.post(UPLOAD_URL, files=files)
                response.raise_for_status()
                result = response.json()
                print(f"Successfully uploaded {filename}. Image ID: {result.get('image_id')}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to upload {filename}. Error: {e}")

if __name__ == "__main__":
    populate_products()
