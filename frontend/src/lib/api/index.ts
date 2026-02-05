/**
 * API Client Configuration
 * Auto-generated TypeScript client from FastAPI OpenAPI schema
 * With automatic token refresh interceptor
 */

import { OpenAPI } from '../api-client';
import axios from 'axios';
import { setupAxiosInterceptor } from '../api-client/core/refreshToken';

// Create axios instance with interceptor
const apiAxios = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
});

// Setup automatic token refresh
setupAxiosInterceptor(apiAxios);

// Configure the API client with base URL
OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Configure credentials for CORS requests
OpenAPI.WITH_CREDENTIALS = true;
OpenAPI.CREDENTIALS = 'include';

// Token will be set dynamically via api-config.ts
// after successful login/signup
OpenAPI.TOKEN = undefined;

export * from '../api-client';
export { apiAxios };

