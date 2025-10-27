import bentoml
from PIL.Image import Image
import numpy as np
from typing import Dict
from typing import List
from pydantic import Field

MODEL_ID = "openai/clip-vit-base-patch32"

runtime_image = bentoml.images.Image(
    python_version="3.11"
).requirements_file("requirements.txt")


def _resize_img(img: Image):
    return img.resize((224, 224))


@bentoml.service(
    image=runtime_image,
    resources={
        "memory" : "2Gi"
    }
)
class CLIP:

    hf_model = bentoml.models.HuggingFaceModel(MODEL_ID)
    
    def __init__(self) -> None:
        import torch
        from transformers import CLIPModel, CLIPProcessor
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(self.hf_model).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.hf_model)
        self.logit_scale = self.model.logit_scale.item() if self.model.logit_scale.item() else 4.60517
        print("Model clip loaded", "device:", self.device)

    @bentoml.api(batchable=True)
    async def encode_image(self, items: List[Image]) -> np.ndarray:
        '''
        generate the 512-d embeddings of the images
        '''
        items = [_resize_img(item) for item in items]
        inputs = self.processor(images=items, return_tensors="pt", padding=True).to(self.device)
        image_embeddings = self.model.get_image_features(**inputs)
        return image_embeddings.cpu().detach().numpy()
    

    @bentoml.api(batchable=True)
    async def encode_text(self, items: List[str]) -> np.ndarray:
        '''
        generate the 512-d embeddings of the texts
        '''
        inputs = self.processor(text=items, return_tensors="pt", padding=True).to(self.device)
        text_embeddings = self.model.get_text_features(**inputs)
        return text_embeddings.cpu().detach().numpy()
