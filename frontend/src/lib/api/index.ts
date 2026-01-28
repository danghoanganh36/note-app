/**
 * API Client Configuration
 * Auto-generated TypeScript client from FastAPI OpenAPI schema
 */

import { OpenAPI } from './api-client';

// Configure the API client with base URL
OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Optional: Add authentication token interceptor
OpenAPI.TOKEN = async () => {
  // Add your auth token logic here
  // Example: return localStorage.getItem('token') || '';
  return '';
};

// Optional: Add request/response interceptors
OpenAPI.interceptors = {
  request: async (options) => {
    // Modify request before it's sent
    return options;
  },
  response: async (response) => {
    // Process response
    return response;
  },
};

export * from './api-client';
