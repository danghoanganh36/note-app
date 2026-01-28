# Project Initialization Guide - Handbook/Compass Web App

**Tech Stack**: Next.js 15 (Frontend) + FastAPI (Backend) + PostgreSQL + Redis + Qdrant

**Date**: January 26, 2026  
**Target**: macOS/Linux Development Environment

---

## Prerequisites

### Required Tools

```bash
# Check versions
node --version    # Need 20+ LTS
python3 --version # Need 3.10+
docker --version  # For PostgreSQL & Redis
git --version

# If missing, install:
brew install node python@3.12 docker git
```

### Accounts & API Keys Needed

| Service      | Purpose                               | Sign Up                     |
| ------------ | ------------------------------------- | --------------------------- |
| **OpenAI**   | LLM API for quiz generation           | https://platform.openai.com |
| **Qdrant**   | Vector database (Free 1GB cluster)    | https://cloud.qdrant.io     |
| **Vercel**   | Frontend hosting (optional)           | https://vercel.com          |

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
npx create-next-app@latest . --typescript --tailwind --app --use-npm \ --src-dir=false --import-alias="@/*"

# Answer prompts:
# ✔ Would you like to use ESLint? Yes
# ✔ Would you like to use Turbopack? No
# ✔ Would you like to customize the import alias? No
```

### Step 2: Install Core Dependencies

```bash
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-collaboration @tiptap/extension-collaboration-cursor yjs y-websocket zustand @tanstack/react-query next-auth axios zod

npm install -D @types/node @types/react @types/react-dom
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
  src/app/api/auth \
  src/app/(dashboard) \
  src/app/(public) \
  src/components/editor \
  src/components/ui \
  src/lib/api \
  src/lib/hooks \
  src/lib/stores \
  src/lib/utils \
  src/types
```

### Step 6: Configure Next.js

Edit `next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: "10mb",
    },
  },
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: "http://localhost:8000/api/v1/:path*",
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

# Create virtual environment with Python 3.13 (stable and compatible with all packages)
python3.13 -m venv venv

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
qdrant-client==1.12.1

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
    QDRANT_API_KEY: str
    QDRANT_CLUSTER_ENDPOINT: str
    QDRANT_COLLECTION_NAME: str = "handbook-vectors"

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
QDRANT_API_KEY=xxx
QDRANT_CLUSTER_ENDPOINT=https://xxx.cloud.qdrant.io
QDRANT_COLLECTION_NAME=handbook-vectors

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

# IMPORTANT: If you have local PostgreSQL installed, stop it first
# to avoid port conflicts (e.g., brew services stop postgresql@17)

# Test connections (inside Docker containers)
docker exec handbook_postgres psql -U postgres -c "SELECT version();"
docker exec handbook_redis redis-cli ping
```

### Step 3: Initialize Database Schema

```bash
cd backend

# Alembic is already initialized with migrations/ directory
# The env.py has been configured to use app.db.Base metadata

# Create first migration (empty for now, models will be added later)
alembic revision --autogenerate -m "initial tables"

# Apply migration
alembic upgrade head

# Verify migration applied
docker exec handbook_postgres psql -U postgres -d handbook_compass -c "\dt"
# Should show: alembic_version table
```

---

## Part 5: Qdrant Vector Database Setup

### Step 1: Create Index

```bash
cd backend

# Create setup script
cat > scripts/setup_qdrant.py << 'EOF'
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

# Initialize Qdrant client with cluster endpoint
client = QdrantClient(
    url=os.getenv("QDRANT_CLUSTER_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

collection_name = "handbook-vectors"

# Check if collection exists
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if collection_name not in collection_names:
    # Create collection with sentence-transformers/all-MiniLM-L6-v2 dimension
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,  # sentence-transformers/all-MiniLM-L6-v2
            distance=Distance.COSINE
        )
    )
    print(f"✅ Collection '{collection_name}' created successfully")
else:
    print(f"ℹ️  Collection '{collection_name}' already exists")

# Get collection info
collection_info = client.get_collection(collection_name)
print(f"📊 Collection stats:")
print(f"   - Vectors count: {collection_info.points_count}")
print(f"   - Vector size: {collection_info.config.params.vectors.size}")
print(f"   - Distance: {collection_info.config.params.vectors.distance}")
print(f"   - Status: {collection_info.status}")
EOF

# Run setup
python scripts/setup_qdrant.py
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

## Part 8: OpenAPI Code Generation

### Setup API Client Generator

```bash
cd frontend

# Install code generator
npm install -D openapi-typescript-codegen

# Add generation script
# (Already created at scripts/generate-api-client.js)

# Add to .gitignore
echo "frontend/src/lib/api-client/" >> ../.gitignore
```

### Generate TypeScript Client

```bash
# Make sure backend is running first!
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload --host localhost --port 8000 &

# Generate client (in new terminal)
cd ../frontend
npm run generate:api
```

Expected output:
```
✅ API client generated successfully!
📁 Location: /path/to/frontend/src/lib/api-client
```

### Test Generated Client

Create test component:

```typescript
// src/components/ApiExample.tsx
import { DefaultService } from '@/lib/api';

export default function ApiExample() {
  const [data, setData] = useState(null);

  useEffect(() => {
    DefaultService.healthCheckHealthGet().then(setData);
  }, []);

  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```

**📚 Full documentation**: See [OPENAPI-CODEGEN.md](./OPENAPI-CODEGEN.md)

---

## Part 9: Verification Checklist

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

## Part 10: Next Steps (Phase 1 Implementation)

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
| Port already in use | `lsof -ti:3000 \| xargs kill -9`(frontend) <br>`lsof -ti:8000 \| xargs kill -9` (backend) |
| PostgreSQL connection refused | Check Docker: `docker-compose ps`<br>Stop local PostgreSQL: `brew services stop postgresql@17`<br>Restart: `docker-compose restart postgres` |
| Python module not found | `pip install -r requirements.txt` again |
| Next.js build errors | `rm -rf .next && npm run dev` |
| Qdrant API error | Check API key and cluster endpoint |
| Alembic connection error | Ensure local PostgreSQL is stopped: `brew services list`<br>Use Docker PostgreSQL on port 5432 |

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

- **Project Docs**: [OpenAPI Code Generation](./OPENAPI-CODEGEN.md)
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **TipTap Editor**: https://tiptap.dev
- **Shadcn/ui**: https://ui.shadcn.com
- **LangChain**: https://python.langchain.com
- **Qdrant**: https://qdrant.tech/documentation

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
QDRANT_API_KEY=xxx
QDRANT_CLUSTER_ENDPOINT=https://xxx.cloud.qdrant.io
QDRANT_COLLECTION_NAME=handbook-vectors
```

---

## Summary

**Setup Time**: ~30-45 minutes

**What You Have Now**:

- ✅ Next.js 15 frontend with TypeScript + Tailwind
- ✅ FastAPI backend with async PostgreSQL
- ✅ PostgreSQL & Redis in Docker
- ✅ Qdrant vector database
- ✅ Development scripts for easy startup
- ✅ Testing setup
- ✅ Hot reload for both frontend & backend

**Next**: Start implementing Phase 1 features (Authentication → Editor → Sharing)

**Questions?** Review the tech stack document for architecture decisions.
