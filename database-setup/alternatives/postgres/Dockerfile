FROM ankane/pgvector

ENV POSTGRES_USER=db_user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=freepdb1

# Add init script to image (will be executed automatically by Postgres entrypoint)
COPY init.sql /docker-entrypoint-initdb.d/