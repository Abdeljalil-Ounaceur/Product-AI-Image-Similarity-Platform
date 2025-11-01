# Product Image Similarity Platform

This project provides a platform for finding products based on image similarity. It's built with a microservices architecture and is fully containerized with Docker for portability and ease of use.

## Architecture

The platform is composed of five services that work together:

-   **Frontend (React):** A single-page application that allows users to upload an image and view similar products.
-   **Backend (FastAPI):** A Python-based backend that handles API requests, communicates with other services, and serves the frontend.
-   **ML Model Service (BentoML):** A service that uses the OpenAI CLIP model to generate embeddings for images.
-   **Minio:** An object storage service for storing and retrieving product images.
-   **Database (Oracle):** An Oracle database for storing product information and image embeddings.

All services are containerized and can be orchestrated with Docker Compose.

## Getting Started

### Prerequisites

-   Docker and Docker Compose installed.
-   Python 3.11 or later.

### Running the Platform

1.  **Start the services:**

    ```bash
    docker-compose up -d
    ```

    This will start all the services in the background.

2.  **Populate the database:**

    Navigate to the `database-setup` directory and run the following command:

    ```bash
    # pip install requests python-dotenv
    python populate_products.py
    ```

    This will populate the database with sample product data.

3.  **Access the application:**

    Open your browser and go to `http://localhost:3000` to use the application.

## Milestones

-   Implemented 5 core services (Frontend, Backend, ML Model, Minio, Database).
-   Dockerized all services for containerization and orchestration.
-   Implemented GitHub Workflows for automated testing.

## Future Enhancements

-   Polish the frontend with a better UI and more meaningful look.
-   Use Kubernetes for scaling the application.
-   Add more comprehensive tests for all services.
