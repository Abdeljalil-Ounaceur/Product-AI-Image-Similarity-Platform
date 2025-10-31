from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "Product Image Similarity API"
    app_version: str = "0.1.0"
    
    # CORS Settings
    cors_origins: list[str] = ["*"]
    
    # Future: Add settings for MinIO, ML model paths, etc.
    # minio_endpoint: str = "localhost:9000"
    # model_path: str = "./models/clip-model"


settings = Settings()
