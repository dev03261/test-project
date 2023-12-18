# FastAPI Project

This is a simple FastAPI project using FastAPI and Uvicorn.

## Installation

To run this project locally, follow these steps:

1. Install FastAPI and Uvicorn:

    ```bash
    pip install fastapi
    pip install uvicorn
    ```

2. Run the FastAPI app:

    ```bash
    uvicorn main:app --reload
    ```

The `--reload` flag enables automatic code reloading during development.

## Usage

Once the FastAPI app is running, you can access the API at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. You will also find the Swagger documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and the ReDoc documentation at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

## Additional Information

- The `main.py` file contains the FastAPI application code.
- You can customize the routes and functionality in the `main.py` file based on your project requirements.

