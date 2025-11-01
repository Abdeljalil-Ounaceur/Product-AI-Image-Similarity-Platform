import bentoml
from transformers import CLIPModel, CLIPProcessor

MODEL_ID = "openai/clip-vit-base-patch32"

print(f"Downloading model: {MODEL_ID}")
# This caches in the standard transformers cache directory

model_path = bentoml.models.HuggingFaceModel(MODEL_ID)
model = CLIPModel.from_pretrained(model_path)
processor = CLIPProcessor.from_pretrained(model_path)

print("Model cached successfully")