# OpenAPI Code Generation Workflow

Automated TypeScript client generation from FastAPI OpenAPI schema.

## Overview

The frontend uses auto-generated TypeScript code to call backend APIs, ensuring type safety and eliminating manual API client maintenance.

## Architecture

```
Backend (FastAPI)
    ↓ Generates
OpenAPI Schema (JSON)
    ↓ Downloaded by
Generation Script
    ↓ Creates
TypeScript Client
    ↓ Used by
Frontend (Next.js)
```

## Setup

### 1. Prerequisites

```bash
# Install openapi-typescript-codegen
cd frontend
npm install -D openapi-typescript-codegen
```

### 2. Configuration

The API client is configured in `frontend/src/lib/api/index.ts`:

```typescript
import { OpenAPI } from './api-client';

OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

## Usage

### Generate API Client

**Before generating**, ensure the backend is running:

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Generate client
cd frontend
npm run generate:api
```

### Use in Components

```typescript
import { DefaultService } from '@/lib/api';

// Type-safe API calls
const health = await DefaultService.healthCheckHealthGet();
const dbTest = await DefaultService.testDatabaseDbTestGet();
```

### With React Query

```typescript
import { useQuery } from '@tanstack/react-query';
import { DefaultService } from '@/lib/api';

function MyComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['health'],
    queryFn: () => DefaultService.healthCheckHealthGet(),
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>Status: {data.status}</div>;
}
```

## Development Workflow

### 1. Add New API Endpoint (Backend)

```python
# backend/app/api/endpoints/documents.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Document(BaseModel):
    id: int
    title: str
    content: str

@router.get("/documents", response_model=list[Document])
async def list_documents():
    return [{"id": 1, "title": "Test", "content": "Content"}]

# backend/app/main.py
from app.api.endpoints import documents
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
```

### 2. Regenerate Client

```bash
npm run generate:api
```

### 3. Use New Endpoint (Frontend)

```typescript
import { DocumentsService } from '@/lib/api';

const documents = await DocumentsService.listDocumentsDocumentsGet();
// TypeScript knows the exact return type!
```

## Benefits

✅ **Type Safety**: Full TypeScript types for requests and responses  
✅ **Auto-sync**: Backend changes automatically reflected in frontend  
✅ **No Manual Updates**: API changes don't require manual client updates  
✅ **IntelliSense**: IDE autocomplete for all API methods  
✅ **Validation**: Compile-time errors for incorrect API usage  
✅ **Documentation**: Generated from OpenAPI descriptions

## Generated Files

```
frontend/src/lib/api-client/
├── core/              # Core utilities (axios config, error handling)
├── models/            # TypeScript interfaces for data models
├── services/          # API service classes
└── index.ts           # Main export file
```

**⚠️ DO NOT EDIT**: These files are auto-generated and will be overwritten on regeneration.

## Gitignore

Generated client code is gitignored to avoid merge conflicts:

```gitignore
frontend/src/lib/api-client/
```

Each developer regenerates locally when needed.

## CI/CD Integration

### Option 1: Generate During Build

```json
// package.json
{
  "scripts": {
    "prebuild": "npm run generate:api",
    "build": "next build"
  }
}
```

### Option 2: Commit Generated Code

Remove from `.gitignore` and commit generated files. Useful for:
- Vercel deployments without backend access
- Teams without backend running locally

## Troubleshooting

### Backend not running

```
❌ Backend is not running!
```

**Solution**: Start backend first:
```bash
cd backend && uvicorn app.main:app
```

### Port conflicts

**Solution**: Update `NEXT_PUBLIC_API_URL`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001 npm run generate:api
```

### Generation fails

**Solution**: Check OpenAPI schema is valid:
```bash
curl http://localhost:8000/api/v1/openapi.json | jq
```

## Advanced Configuration

### Custom Client Settings

Edit `frontend/src/lib/api/index.ts`:

```typescript
import { OpenAPI } from './api-client';

// Add auth token
OpenAPI.TOKEN = async () => {
  const session = await getSession();
  return session?.accessToken || '';
};

// Add custom headers
OpenAPI.HEADERS = {
  'X-Custom-Header': 'value',
};

// Configure axios interceptors
OpenAPI.interceptors = {
  request: async (config) => {
    // Log all requests in development
    if (process.env.NODE_ENV === 'development') {
      console.log('API Request:', config);
    }
    return config;
  },
  response: async (response) => {
    // Handle errors globally
    if (response.status >= 400) {
      console.error('API Error:', response);
    }
    return response;
  },
};
```

### Alternative Generators

**openapi-typescript** (types only):
```bash
npm install -D openapi-typescript
npx openapi-typescript http://localhost:8000/api/v1/openapi.json -o src/lib/api-types.ts
```

**swagger-typescript-api** (full client):
```bash
npm install -D swagger-typescript-api
npx swagger-typescript-api -p http://localhost:8000/api/v1/openapi.json -o src/lib/api-client
```

## Best Practices

1. **Regenerate after backend changes**: Always run `npm run generate:api` after pulling backend updates
2. **Don't edit generated files**: All changes will be lost on regeneration
3. **Use custom wrappers**: Create wrapper functions in `src/lib/api/` for complex logic
4. **Version control**: Decide early whether to commit or gitignore generated code
5. **Error handling**: Use try-catch or React Query for proper error management

## Related Files

- `frontend/scripts/generate-api-client.js` - Generation script
- `frontend/src/lib/api/index.ts` - Client configuration
- `frontend/src/lib/api-client/` - Generated code (gitignored)
- `backend/app/main.py` - OpenAPI configuration

## Resources

- [FastAPI OpenAPI Docs](https://fastapi.tiangolo.com/tutorial/metadata/)
- [openapi-typescript-codegen](https://github.com/ferdikoomen/openapi-typescript-codegen)
- [OpenAPI Specification](https://swagger.io/specification/)
