from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from services.database import create_db_and_tables
from utils.get_env import get_app_data_directory_env

@asynccontextmanager
async def app_lifespan(_: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Initializes the application data directory and database.
    """
    app_data_dir = get_app_data_directory_env()
    if not app_data_dir:
        app_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app_data"))
        # print(f"APP_DATA_DIRECTORY not set, using default: {app_data_dir}")

    os.makedirs(app_data_dir, exist_ok=True)
    await create_db_and_tables()
    # Model availability check removed as we only use Gemini now.
    yield
