from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import get_db

# API metadata for better documentation
tags_metadata = [
    {
        "name": "Health",
        "description": "Health check and database connectivity endpoints",
    },
    {
        "name": "Documents",
        "description": "Document CRUD operations, version history, and organization",
    },
    {
        "name": "Folders",
        "description": "Folder management for organizing documents hierarchically",
    },
    {
        "name": "Authentication",
        "description": "User authentication and authorization endpoints",
    },
    {
        "name": "Sharing",
        "description": "Document sharing with users and public link management",
    },
    {
        "name": "Quizzes",
        "description": "AI-powered quiz generation and learning management",
    },
    {
        "name": "Chat",
        "description": "AI chat with documents using RAG (Retrieval Augmented Generation)",
    },
    {
        "name": "Comments",
        "description": "Commenting and discussion threads on documents",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
## Handbook/Compass API

Complete platform combining **collaborative documentation** + **AI-powered learning** + **knowledge sharing**.

### Features

* **📝 Document Management** - Create, edit, organize documents with version history
* **🤝 Real-time Collaboration** - Multi-user editing with live presence
* **🔐 Permission System** - Private, shared, and public access levels
* **🤖 AI Chat** - Ask questions about your documents using RAG
* **🎯 Quiz Generation** - AI-generated quizzes from document content
* **📚 Spaced Repetition** - Smart learning with Anki-style algorithm
* **🗂️ Folder Organization** - Hierarchical folder structure
* **💬 Comments & Threads** - Collaborative discussions on documents

### Tech Stack

* **Backend**: FastAPI + PostgreSQL + SQLAlchemy (Async)
* **AI**: Qdrant (Vector DB) + Ollama (Local LLM)
* **Real-time**: Yjs (CRDT for collaboration)
    """,
    summary="Document management with AI-powered learning and collaboration",
    contact={
        "name": "Handbook/Compass Team",
        "url": "https://github.com/yourusername/handbook-compass",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api.endpoints import documents, auth

# Authentication endpoints
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"]
)

# Document endpoints
app.include_router(
    documents.router,
    prefix=f"{settings.API_V1_STR}/documents",
    tags=["Documents"]
)

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - API information
    
    Returns basic API information and documentation links.
    """
    return {
        "message": "Handbook Compass API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Simple endpoint to verify the API is running.
    """
    return {"status": "healthy"}

@app.get("/db-test", tags=["Health"])
async def test_database(db: AsyncSession = Depends(get_db)):
    """
    Test database connection
    
    Verifies async PostgreSQL connection and returns database version.
    
    Returns:
    - **status**: Connection status
    - **database**: Database type
    - **version**: PostgreSQL version
    - **driver**: Database driver being used
    """
    result = await db.execute(text("SELECT version()"))
    version = result.scalar()
    return {
        "status": "connected",
        "database": "PostgreSQL",
        "version": version,
        "driver": "asyncpg"
    }