import bentoml
from PIL.Image import Image
import numpy as np
from typing import List

MODEL_ID = "openai/clip-vit-base-patch32"

runtime_image = bentoml.images.Image(
    python_version="3.11"
).requirements_file("requirements.txt")

def _resize_img(img: Image):
    return img.resize((224, 224))

@bentoml.service(
    image=runtime_image,
    resources={
        "memory": "2Gi"
    }
)
class CLIP:
    # Use HuggingFaceModel instead of bentoml.transformers
    model_path = bentoml.models.HuggingFaceModel(MODEL_ID)
    
    def __init__(self) -> None:
        import torch
        from transformers import CLIPModel, CLIPProcessor
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load from the HuggingFace model path
        self.model = CLIPModel.from_pretrained(self.model_path).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.model_path)
        
        self.logit_scale = self.model.logit_scale.item() if self.model.logit_scale.item() else 4.60517
        print("Model CLIP loaded", "device:", self.device)
    
    @bentoml.api(batchable=True)
    async def encode_image(self, items: List[Image]) -> np.ndarray:
        '''
        generate the 512-d embeddings of the images
        '''
        items = [_resize_img(item) for item in items]
        inputs = self.processor(images=items, return_tensors="pt", padding=True).to(self.device)
        image_embeddings = self.model.get_image_features(**inputs)
        return image_embeddings.cpu().detach().numpy()