# Project Initialization Guide - Handbook/Compass Web App

**Tech Stack**: Next.js 15 (Frontend) + FastAPI (Backend) + PostgreSQL + Redis + Pinecone

**Date**: January 26, 2026  
**Target**: macOS/Linux Development Environment

---

## Prerequisites

### Required Tools

```bash
# Check versions
node --version    # Need 20+ LTS
python --version  # Need 3.11+
docker --version  # For PostgreSQL & Redis
git --version

# If missing, install:
brew install node python@3.11 docker git
```

### Accounts & API Keys Needed

| Service | Purpose | Sign Up |
|---------|---------|---------|
| **OpenAI** | LLM API for quiz generation | https://platform.openai.com |
| **Pinecone** | Vector database (Starter plan $12/mo) | https://pinecone.io |
| **Vercel** | Frontend hosting (optional) | https://vercel.com |

---

## Project Structure

```
note-app/
├── frontend/          # Next.js 15 application
│   ├── app/           # App Router
│   ├── components/    # React components
│   ├── lib/           # Utilities
│   ├── public/        # Static assets
│   └── package.json
│
├── backend/           # FastAPI Python application
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── models/    # SQLAlchemy models
│   │   ├── services/  # Business logic
│   │   ├── ml/        # AI/ML modules
│   │   └── main.py    # FastAPI entry
│   ├── requirements.txt
│   └── pyproject.toml
│
├── docker-compose.yml # PostgreSQL + Redis
├── .env.example       # Environment variables template
└── README.md
```

---

## Part 1: Initialize Project Root

### Step 1: Create Project Directory

```bash
# If not already in project directory
cd /Users/hoanganh/Private/note-app

# Create subdirectories
mkdir -p frontend backend docs scripts
```

### Step 2: Initialize Git

```bash
git init
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Build outputs
.next/
dist/
build/

# Database
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
EOF

git add .gitignore
git commit -m "chore: initial commit with gitignore"
```

---

## Part 2: Frontend Setup (Next.js 15)

### Step 1: Create Next.js App

```bash
cd frontend

# Initialize Next.js with TypeScript, Tailwind, App Router
npx create-next-app@latest . --typescript --tailwind --app --use-npm \
  --src-dir=false --import-alias="@/*"

# Answer prompts:
# ✔ Would you like to use ESLint? Yes
# ✔ Would you like to use Turbopack? No
# ✔ Would you like to customize the import alias? No
```

### Step 2: Install Core Dependencies

```bash
npm install \
  @tiptap/react \
  @tiptap/starter-kit \
  @tiptap/extension-collaboration \
  @tiptap/extension-collaboration-cursor \
  yjs \
  y-websocket \
  zustand \
  @tanstack/react-query \
  next-auth \
  axios \
  zod

npm install -D \
  @types/node \
  @types/react \
  @types/react-dom
```

### Step 3: Install Shadcn/ui

```bash
# Initialize shadcn/ui
npx shadcn@latest init

# Select options:
# Style: New York
# Color: Zinc
# CSS variables: Yes

# Install essential components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add textarea
npx shadcn@latest add toast
npx shadcn@latest add avatar
npx shadcn@latest add badge
```

### Step 4: Configure Environment Variables

```bash
cat > .env.local << 'EOF'
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here-generate-with-openssl

# OpenAI (for client-side features if needed)
NEXT_PUBLIC_OPENAI_API_KEY=sk-xxx
EOF

# Generate secure secret
openssl rand -base64 32
# Copy output to NEXTAUTH_SECRET
```

### Step 5: Setup Directory Structure

```bash
mkdir -p \
  app/api/auth \
  app/(dashboard) \
  app/(public) \
  components/editor \
  components/ui \
  lib/api \
  lib/hooks \
  lib/stores \
  lib/utils \
  types
```

### Step 6: Configure Next.js

Edit `next.config.ts`:

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '10mb',
    },
  },
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'http://localhost:8000/api/v1/:path*',
      },
    ];
  },
};

export default nextConfig;
```

### Step 7: Verify Frontend Setup

```bash
npm run dev
# Should start on http://localhost:3000
```

---

## Part 3: Backend Setup (FastAPI)

### Step 1: Initialize Python Environment

```bash
cd ../backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 2: Create Requirements File

```bash
cat > requirements.txt << 'EOF'
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-multipart==0.0.12
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Database
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
alembic==1.14.0
asyncpg==0.30.0

# Redis
redis==5.2.0
aioredis==2.0.1

# AI/ML
langchain==0.3.13
langchain-openai==0.2.14
langchain-community==0.3.13
openai==1.59.6
sentence-transformers==3.3.1
pinecone-client==5.0.1

# Document Processing
pypdf==5.1.0
python-docx==1.1.2
openpyxl==3.1.5
python-magic==0.4.27

# Utilities
pydantic==2.10.3
pydantic-settings==2.6.1
python-dotenv==1.0.1
tenacity==9.0.0

# Testing
pytest==8.3.4
pytest-asyncio==0.24.0
httpx==0.28.1

# Development
black==24.10.0
ruff==0.8.4
mypy==1.13.0
EOF

pip install -r requirements.txt
```

### Step 3: Create Project Structure

```bash
mkdir -p \
  app/api/endpoints \
  app/core \
  app/models \
  app/schemas \
  app/services \
  app/ml \
  app/db \
  tests

touch app/__init__.py
touch app/api/__init__.py
touch app/api/endpoints/__init__.py
```

### Step 4: Create Core Configuration

Create `app/core/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Handbook Compass API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "handbook_compass"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # AI/ML
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str = "us-west1-gcp"
    PINECONE_INDEX_NAME: str = "handbook-vectors"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
```

### Step 5: Create Main Application

Create `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Handbook Compass API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers here later
# from app.api.endpoints import documents, auth, quiz
# app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
```

### Step 6: Create Environment File

```bash
cat > .env << 'EOF'
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=handbook_compass

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# AI/ML
OPENAI_API_KEY=sk-xxx
PINECONE_API_KEY=xxx
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=handbook-vectors

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
EOF

echo ".env" >> .gitignore
```

### Step 7: Verify Backend Setup

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# Visit http://localhost:8000/docs for API docs
```

---

## Part 4: Database Setup (Docker)

### Step 1: Create Docker Compose File

```bash
cd /Users/hoanganh/Private/note-app

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: handbook_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: handbook_compass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: handbook_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
EOF
```

### Step 2: Start Databases

```bash
# Start containers
docker-compose up -d

# Verify running
docker-compose ps

# Check logs
docker-compose logs postgres
docker-compose logs redis

# Test connections
psql -h localhost -U postgres -d handbook_compass -c "SELECT version();"
redis-cli ping
```

### Step 3: Initialize Database Schema

```bash
cd backend

# Create Alembic config
alembic init migrations

# Edit migrations/env.py to add:
# from app.core.config import settings
# config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Create first migration
alembic revision --autogenerate -m "initial tables"

# Apply migration
alembic upgrade head
```

---

## Part 5: Pinecone Vector Database Setup

### Step 1: Create Index

```bash
cd backend

# Create setup script
cat > scripts/setup_pinecone.py << 'EOF'
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "handbook-vectors"

# Check if index exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # sentence-transformers/all-MiniLM-L6-v2
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
        )
    )
    print(f"✅ Index '{index_name}' created successfully")
else:
    print(f"ℹ️  Index '{index_name}' already exists")

# Get index info
index = pc.Index(index_name)
print(f"📊 Index stats: {index.describe_index_stats()}")
EOF

# Run setup
python scripts/setup_pinecone.py
```

---

## Part 6: Development Scripts

### Create Helper Scripts

```bash
cd /Users/hoanganh/Private/note-app

# Start all services
cat > start-dev.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Starting Handbook Compass Development Environment"

# Start databases
echo "📦 Starting PostgreSQL & Redis..."
docker-compose up -d

# Wait for databases
echo "⏳ Waiting for databases..."
sleep 3

# Start backend
echo "🐍 Starting FastAPI backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "⚛️  Starting Next.js frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ All services started!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT
wait
EOF

chmod +x start-dev.sh

# Stop all services
cat > stop-dev.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping all services..."
pkill -f "uvicorn app.main:app"
pkill -f "next dev"
docker-compose down
echo "✅ All services stopped"
EOF

chmod +x stop-dev.sh
```

---

## Part 7: Testing Setup

### Backend Tests

```bash
cd backend

# Create test config
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
EOF

# Create test example
mkdir -p tests
cat > tests/test_main.py << 'EOF'
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
EOF

# Run tests
pytest
```

---

## Part 8: Verification Checklist

### ✅ Complete Setup Checklist

```bash
# Run this verification script
cat > verify-setup.sh << 'EOF'
#!/bin/bash

echo "🔍 Verifying Handbook Compass Setup..."

# Frontend
if [ -f "frontend/package.json" ]; then
    echo "✅ Frontend: package.json exists"
else
    echo "❌ Frontend: package.json missing"
fi

# Backend
if [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend: requirements.txt exists"
else
    echo "❌ Backend: requirements.txt missing"
fi

# Docker
if docker-compose ps | grep -q "handbook_postgres"; then
    echo "✅ PostgreSQL: Running"
else
    echo "❌ PostgreSQL: Not running"
fi

if docker-compose ps | grep -q "handbook_redis"; then
    echo "✅ Redis: Running"
else
    echo "❌ Redis: Not running"
fi

# Test connections
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API: Responding"
else
    echo "❌ Backend API: Not responding"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend: Responding"
else
    echo "❌ Frontend: Not responding"
fi

echo ""
echo "📊 Setup Status Complete!"
EOF

chmod +x verify-setup.sh
./verify-setup.sh
```

---

## Part 9: Next Steps (Phase 1 Implementation)

### Recommended Implementation Order

1. **Authentication System** (Week 1)
   - NextAuth.js setup
   - JWT token flow
   - User registration/login
   - Password reset

2. **Document Editor** (Week 2)
   - TipTap integration
   - Markdown support
   - Auto-save functionality
   - Document CRUD API

3. **Permission System** (Week 3)
   - RBAC implementation
   - Document sharing
   - Access control middleware

4. **File Upload** (Week 4)
   - S3/CloudFlare R2 integration
   - PDF/DOCX parsing
   - Preview generation

5. **Real-time Collaboration** (Week 5-6)
   - Yjs setup
   - WebSocket server
   - Cursor tracking
   - Conflict resolution

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | `lsof -ti:3000 | xargs kill -9` (frontend) <br> `lsof -ti:8000 | xargs kill -9` (backend) |
| PostgreSQL connection refused | `docker-compose restart postgres` |
| Python module not found | `pip install -r requirements.txt` again |
| Next.js build errors | `rm -rf .next && npm run dev` |
| Pinecone API error | Check API key and environment region |

### Useful Commands

```bash
# View logs
docker-compose logs -f postgres
docker-compose logs -f redis

# Reset databases
docker-compose down -v
docker-compose up -d

# Backend hot reload
cd backend && uvicorn app.main:app --reload

# Frontend clear cache
cd frontend && rm -rf .next node_modules && npm install

# Check Python environment
which python
pip list
```

---

## Resources

- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **TipTap Editor**: https://tiptap.dev
- **Shadcn/ui**: https://ui.shadcn.com
- **LangChain**: https://python.langchain.com
- **Pinecone**: https://docs.pinecone.io

---

## Environment Variables Quick Reference

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=<generate-with-openssl-rand-base64-32>
```

### Backend (.env)
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=handbook_compass

REDIS_HOST=localhost
REDIS_PORT=6379

SECRET_KEY=<your-secret-key>
OPENAI_API_KEY=sk-xxx
PINECONE_API_KEY=xxx
PINECONE_INDEX_NAME=handbook-vectors
```

---

## Summary

**Setup Time**: ~30-45 minutes

**What You Have Now**:
- ✅ Next.js 15 frontend with TypeScript + Tailwind
- ✅ FastAPI backend with async PostgreSQL
- ✅ PostgreSQL & Redis in Docker
- ✅ Pinecone vector database
- ✅ Development scripts for easy startup
- ✅ Testing setup
- ✅ Hot reload for both frontend & backend

**Next**: Start implementing Phase 1 features (Authentication → Editor → Sharing)

**Questions?** Review the tech stack document for architecture decisions.
