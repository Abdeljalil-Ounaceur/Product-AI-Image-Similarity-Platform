import oracledb
import os
from typing import List, Dict
import numpy as np
import array

class DatabaseService:
    def __init__(self):
        self.db_user = os.environ.get("DB_USER","db_user")
        self.db_password = os.environ.get("DB_PASSWORD","password")
        self.db_host = os.environ.get("DB_HOST","localhost")
        self.db_port = os.environ.get("DB_PORT","1521")
        self.db_service_name = os.environ.get("DB_SERVICE_NAME","freepdb1")
        self.dsn = f"{self.db_host}:{self.db_port}/{self.db_service_name}"
        self.pool = self._create_pool()

    def _create_pool(self):
        try:
            # Adjust pool parameters as needed for your application
            pool = oracledb.create_pool(
                user=self.db_user,
                password=self.db_password,
                dsn=self.dsn,
                min=2,
                max=5,
                increment=1,
                getmode=oracledb.SPOOL_ATTRVAL_WAIT
            )
            return pool
        except oracledb.DatabaseError as e:
            print(f"Error creating Oracle connection pool: {e}")
            return None

    def save_image_embedding(self, image_id: str, embedding: np.ndarray):
        if not self.pool:
            raise Exception("Database connection pool is not available.")

        embedding_array = array.array("f", embedding.flatten())
        
        with self.pool.acquire() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO USER_UPLOADED_IMAGE_EMBEDDINGS (image_id, embedding) VALUES (:1, :2)",
                        [image_id, embedding_array]
                    )
                    connection.commit()
                except oracledb.DatabaseError as e:
                    print(f"Database error during insert: {e}")
                    connection.rollback()
                    raise

    def save_product_image_embedding(self, image_id: str, embedding: np.ndarray):
        if not self.pool:
            raise Exception("Database connection pool is not available.")

        embedding_array = array.array("f", embedding.flatten())
        
        with self.pool.acquire() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO PRODUCT_IMAGE_EMBEDDINGS (image_id, embedding) VALUES (:1, :2)",
                        [image_id, embedding_array]
                    )
                    connection.commit()
                except oracledb.DatabaseError as e:
                    print(f"Database error during insert: {e}")
                    connection.rollback()
                    raise

    def find_similar_images(self, embedding: np.ndarray, top_k: int = 5) -> List[Dict]:
        if not self.pool:
            raise Exception("Database connection pool is not available.")

        embedding_array = array.array("f", embedding.flatten())

        with self.pool.acquire() as connection:
            with connection.cursor() as cursor:
                try:
                    # The distance is cosine distance. Similarity = 1 - distance.
                    cursor.execute(
                        '''
                        SELECT image_id, VECTOR_DISTANCE(embedding, :1, COSINE) as distance
                        FROM PRODUCT_IMAGE_EMBEDDINGS
                        ORDER BY distance
                        FETCH FIRST :2 ROWS ONLY
                        ''',
                        [embedding_array, top_k]
                    )
                    
                    results = []
                    for row in cursor:
                        image_id, distance = row
                        similarity = 1 - distance
                        results.append({"id": image_id, "similarity": round(similarity, 4)})
                    
                    return results
                except oracledb.DatabaseError as e:
                    print(f"Database error during similarity search: {e}")
                    return []

    def close_pool(self):
        if self.pool:
            self.pool.close()
            print("Database connection pool closed.")

# Singleton instance
database_service = DatabaseService()