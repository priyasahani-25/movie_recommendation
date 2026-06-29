from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import router, init_models
from app.database import Database
from app.services.embedding_service import EmbeddingService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up FastAPI application...")
    
    # 1. Connect to MongoDB
    Database.connect()
    
    # 2. Load Embeddings into RAM
    await EmbeddingService.load_embeddings()
    
    # 3. Initialize AI Models
    init_models()
    
    yield
    
    # Shutdown
    print("Shutting down FastAPI application...")
    Database.disconnect()

app = FastAPI(
    title="Movie Recommendation API",
    description="End-to-End AI Pipeline for Movie Recommendation using Face Recognition",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

# Include routes
app.include_router(router)

# Mount the frontend directory to serve static files
import os
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
