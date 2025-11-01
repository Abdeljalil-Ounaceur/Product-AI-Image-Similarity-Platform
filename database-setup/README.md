# Product Similarity Platform Database Service

This microservice is for data storage and vector similarity indexes.

It uses an Oracle database to store product information and image embeddings.

The database is automatically provisioned and set up when running the platform with Docker Compose.

To populate the database with sample data, run the `populate_products.py` script in this directory after starting the services with `docker-compose up -d`.
