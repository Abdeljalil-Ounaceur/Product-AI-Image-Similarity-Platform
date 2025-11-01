#!/bin/sh

# MinIO server and client alias
MINIO_ALIAS="localminio"
MINIO_ENDPOINT=${MINIO_ENDPOINT:-"http://localhost:9000"}
MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY:-minioadmin}
MINIO_SECRET_KEY=${MINIO_SECRET_KEY:-minioadmin}
MINIO_UPLOADS_BUCKET=${MINIO_UPLOADS_BUCKET:-uploads}
MINIO_PRODUCTS_BUCKET=${MINIO_PRODUCTS_BUCKET:-products}

# Wait until MinIO server is ready
until mc alias set $MINIO_ALIAS $MINIO_ENDPOINT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY; do
  echo "Waiting for MinIO to be ready..."
  sleep 2
done

# Function to create bucket if it does not exist
create_bucket_if_not_exists() {
  BUCKET_NAME=$1
  if ! mc ls $MINIO_ALIAS/$BUCKET_NAME > /dev/null 2>&1; then
    echo "Creating bucket: $BUCKET_NAME"
    mc mb $MINIO_ALIAS/$BUCKET_NAME
  else
    echo "Bucket $BUCKET_NAME already exists"
  fi
}

# Create the desired buckets
create_bucket_if_not_exists $MINIO_UPLOADS_BUCKET
create_bucket_if_not_exists $MINIO_PRODUCTS_BUCKET

# Set public read policy for both buckets
echo "Setting public policy for bucket: $MINIO_UPLOADS_BUCKET"
mc anonymous set public $MINIO_ALIAS/$MINIO_UPLOADS_BUCKET

echo "Setting public policy for bucket: $MINIO_PRODUCTS_BUCKET"
mc anonymous set public $MINIO_ALIAS/$MINIO_PRODUCTS_BUCKET

echo "Bucket setup completed with public policies for both uploads and products."