import bentoml
from transformers import CLIPModel, CLIPProcessor

MODEL_ID = "openai/clip-vit-base-patch32"

print(f"Downloading model: {MODEL_ID}")
# This caches in the standard transformers cache directory

bentoml.models.HuggingFaceModel(MODEL_ID).resolve()

print("Model cached successfully")