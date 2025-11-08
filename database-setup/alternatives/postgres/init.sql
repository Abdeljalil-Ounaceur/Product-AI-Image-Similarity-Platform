-- Enable pgvector 
CREATE EXTENSION IF NOT EXISTS vector;

-- Create user (if not exists, ignore errors)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'db_user') THEN
        CREATE USER db_user WITH PASSWORD 'password';
    END IF;
END
$$;

-- Grant privileges
GRANT CONNECT ON DATABASE freepdb1 TO db_user;

-- Create tables
CREATE TABLE IF NOT EXISTS product_image_embeddings (
    image_id VARCHAR(255) PRIMARY KEY,
    embedding vector(512)
);

CREATE TABLE IF NOT EXISTS user_uploaded_image_embeddings (
    image_id VARCHAR(255) PRIMARY KEY,
    embedding vector(512)
);

-- Create vector index (IVFFLAT is closest to Oracle IVF, cosine similarity)
CREATE INDEX IF NOT EXISTS product_image_embedding_ivf_index
ON product_image_embeddings USING ivfflat (embedding vector_cosine_ops);

-- Give db_user ownership (optional but recommended)
ALTER TABLE product_image_embeddings OWNER TO db_user;
ALTER TABLE user_uploaded_image_embeddings OWNER TO db_user;