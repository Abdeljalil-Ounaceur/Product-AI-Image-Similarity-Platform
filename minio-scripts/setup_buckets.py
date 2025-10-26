import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
import json
import sys


def setup_storage():
    """Setup storage buckets (works with MinIO or AWS S3)"""
    
    # Storage connection settings
    ENDPOINT_URL = "http://localhost:9000"  # Remove this line for AWS S3
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "uploads"
    
    print("🔧 Storage Setup Script (boto3)")
    print("=" * 50)
    
    try:
        # Initialize S3 client (works for both MinIO and S3)
        print(f"\n1️⃣ Connecting to storage at {ENDPOINT_URL}...")
        s3_client = boto3.client(
            's3',
            endpoint_url=ENDPOINT_URL,  # Remove for AWS S3
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name='us-east-1'
        )
        
        # Test connection by listing buckets
        print("2️⃣ Testing connection...")
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"✅ Storage is functional! Found {len(buckets)} existing bucket(s).")
        
        # Check if uploads bucket exists
        print(f"\n3️⃣ Checking if '{BUCKET_NAME}' bucket exists...")
        try:
            s3_client.head_bucket(Bucket=BUCKET_NAME)
            print(f"✅ Bucket '{BUCKET_NAME}' already exists.")
        except ClientError:
            print(f"📦 Creating bucket '{BUCKET_NAME}'...")
            s3_client.create_bucket(Bucket=BUCKET_NAME)
            print(f"✅ Bucket '{BUCKET_NAME}' created successfully!")
        
        # Set bucket policy to public-read (for development)
        print(f"\n4️⃣ Setting public-read policy for '{BUCKET_NAME}'...")
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
                }
            ]
        }
        s3_client.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=json.dumps(policy)
        )
        print("✅ Bucket policy set to public-read.")
        
        print("\n" + "=" * 50)
        print("✨ Storage setup completed successfully!")
        print(f"\n📍 Bucket URL: {ENDPOINT_URL}/{BUCKET_NAME}/")
        print("\n💡 You can now upload images to the 'uploads' bucket.")
        print("\n🔄 To migrate to AWS S3 later:")
        print("   - Remove 'endpoint_url' parameter")
        print("   - Update ACCESS_KEY and SECRET_KEY to AWS credentials")
        
    except EndpointConnectionError:
        print(f"\n❌ Connection Error: Cannot connect to {ENDPOINT_URL}")
        print("\n💡 Make sure MinIO is running:")
        print("   docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ':9001'")
        sys.exit(1)
    except ClientError as e:
        print(f"\n❌ Storage Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_storage()