import boto3
from botocore.exceptions import ClientError
import json
import os

if __name__ == "__main__":
    ENDPOINT_URL = os.environ.get("MINIO_ENDPOINT", "http://localhost:9000")
    ACCESS_KEY   = os.environ.get("MINIO_ROOT_USER", "minioadmin")
    SECRET_KEY   = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
    UPLOADS_BUCKET_NAME  = os.environ.get("MINIO_UPLOADS_BUCKET", "uploads")
    PRODUCTS_BUCKET_NAME  = os.environ.get("MINIO_PRODUCTS_BUCKET", "products")

    s3_client = boto3.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-east-1'
    )

    for bucket_name in (UPLOADS_BUCKET_NAME, PRODUCTS_BUCKET_NAME):
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                raise

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(policy)
        )

    print("The buckets setup finiched successfully!")