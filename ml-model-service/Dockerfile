# Use a single, consistent environment
FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY service.py .
COPY download_model.py .

# Run the download script. This will download the model to the cache directory
# defined by the TRANSFORMERS_CACHE environment variable.
RUN python download_model.py

# Expose the port the service will run on
EXPOSE 3000

# Use bentoml to serve the service directly from your Python file.
# The format is <module_name>:<service_class_name>
CMD ["bentoml", "serve", "service:CLIP", "--host", "0.0.0.0", "--port", "3000"]
