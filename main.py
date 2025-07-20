import logging
import uvicorn
import asyncio
import os
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.core import config
from src.core.logger import LOGGING
from src.api.v1 import user
from src.db.postgres import create_database

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logging.info("Starting up FastAPI application...")
    try:
        await create_database()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logging.info("Shutting down FastAPI application...")

app = FastAPI(
    title=config.PROJECT_NAME,
    description="A FastAPI boilerplate with PostgreSQL, SQLAlchemy, and JWT authentication",
    version="1.0.0",
    default_response_class=ORJSONResponse,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    user.get_router(), 
    prefix='/api/v1/users', 
    tags=['users']
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": config.PROJECT_NAME,
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Starter",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=int(config.PROJECT_PORT),
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
