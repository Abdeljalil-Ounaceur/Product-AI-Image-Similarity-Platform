from transformers import CLIPModel, CLIPProcessor

MODEL_ID = "openai/clip-vit-base-patch32"

print(f"Downloading model: {MODEL_ID}")
# This caches in the standard transformers cache directory
CLIPModel.from_pretrained(MODEL_ID)
CLIPProcessor.from_pretrained(MODEL_ID)
print("Model cached successfully")