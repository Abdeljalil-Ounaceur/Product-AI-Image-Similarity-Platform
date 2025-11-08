import psycopg2
import os
from typing import List, Dict
import numpy as np
from pgvector.psycopg2 import register_vector
from pgvector import Vector


class DatabaseService:
    def __init__(self):
        self.db_user = os.environ.get("DB_USER", "db_user")
        self.db_password = os.environ.get("DB_PASSWORD", "password")
        self.db_host = os.environ.get("DB_HOST", "localhost")
        self.db_port = os.environ.get("DB_PORT", "5432")
        self.db_name = os.environ.get("DB_NAME", "freepdb1")
        self.conn = self._create_connection()

    # -------------------------------------------------------------------------
    def _create_connection(self):
        """Create a PostgreSQL connection and register pgvector type."""
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
            conn.autocommit = True
            register_vector(conn)  # <--- native pgvector adapter
            return conn
        except psycopg2.DatabaseError as e:
            print(f"Error creating PostgreSQL connection: {e}")
            return None

    def ensure_connection(self):
        """Reconnect automatically if connection dropped."""
        if not self.conn or self.conn.closed:
            print("Reconnecting to PostgreSQL...")
            self.conn = self._create_connection()
            if not self.conn:
                raise Exception("Database reconnection failed.")

    # -------------------------------------------------------------------------
    @staticmethod
    def _normalize(embedding: np.ndarray) -> np.ndarray:
        """Normalize to unit length for cosine correctness."""
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Embedding has zero norm.")
        return embedding / norm

    # -------------------------------------------------------------------------
    def save_image_embedding(self, image_id: str, embedding: np.ndarray):
        """Save or update user-uploaded image embedding."""
        self.ensure_connection()
        embedding = self._normalize(embedding)

        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO user_uploaded_image_embeddings (image_id, embedding)
                    VALUES (%s, %s)
                    ON CONFLICT (image_id) DO UPDATE SET embedding = EXCLUDED.embedding
                    """,
                    (image_id, Vector(embedding.flatten().tolist())),
                )
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")
                self.conn.rollback()
                raise

    def save_product_image_embedding(self, image_id: str, embedding: np.ndarray):
        """Save or update product image embedding."""
        self.ensure_connection()
        embedding = self._normalize(embedding)

        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO product_image_embeddings (image_id, embedding)
                    VALUES (%s, %s)
                    ON CONFLICT (image_id) DO UPDATE SET embedding = EXCLUDED.embedding
                    """,
                    (image_id, Vector(embedding.flatten().tolist())),
                )
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")
                self.conn.rollback()
                raise

    # -------------------------------------------------------------------------
    def find_similar_images(self, embedding: np.ndarray, top_k: int = 5) -> List[Dict]:
    	"""Find top_k most similar product images by cosine similarity."""
    	self.ensure_connection()
    	embedding = self._normalize(embedding)

    	with self.conn.cursor() as cursor:
        	try:
            		cursor.execute(
                		"""
                		SELECT image_id,
                       			1 - (embedding <#> %s::vector) AS similarity
                		FROM product_image_embeddings
                		ORDER BY embedding <#> %s::vector
                		LIMIT %s
                		""",
                		(embedding.flatten().tolist(), embedding.flatten().tolist(), top_k)
            		)
            		results = []
            		for image_id, similarity in cursor.fetchall():
                		# Ensure the similarity is clamped to [0,1] before converting to %
                		similarity_pct = round(similarity / 2, 2)
                		results.append({"id": image_id, "similarity": similarity_pct})
            		return results
        	except psycopg2.DatabaseError as e:
            		print(f"Database error during similarity search: {e}")
            		return []


# Singleton instance
database_service = DatabaseService()
