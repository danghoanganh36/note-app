/**
 * API Client Configuration
 * Auto-generated TypeScript client from FastAPI OpenAPI schema
 */

import { OpenAPI } from '../api-client';

// Configure the API client with base URL
OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Configure credentials for CORS requests
OpenAPI.WITH_CREDENTIALS = true;
OpenAPI.CREDENTIALS = 'include';

// Token will be set dynamically via api-config.ts
// after successful login/signup
OpenAPI.TOKEN = undefined;

export * from '../api-client';
