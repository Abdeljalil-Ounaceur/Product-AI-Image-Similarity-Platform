FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download to transformers cache
RUN python download_model.py

# Build the Bento
RUN bentoml build

FROM python:3.11-slim

WORKDIR /app

# Copy both BentoML store AND transformers cache
COPY --from=builder /root/bentoml /root/bentoml
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

RUN pip install --no-cache-dir bentoml torch torchvision transformers Pillow

EXPOSE 3000

CMD ["bentoml", "serve", "CLIP:latest", "--host", "0.0.0.0", "--port", "3000"]