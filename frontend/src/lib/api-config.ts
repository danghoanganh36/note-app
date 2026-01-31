import { OpenAPI } from './api-client/core/OpenAPI';

/**
 * Configure API client with base URL and auth token
 */
export function configureApiClient() {
  // Set base URL from environment or default to localhost
  OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  // Set token from localStorage if available
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('accessToken');
    if (token) {
      OpenAPI.TOKEN = token;
    }
  }
}

/**
 * Update API client token (call after login/signup)
 */
export function setApiToken(token: string) {
  OpenAPI.TOKEN = token;
}

/**
 * Clear API client token (call after logout)
 */
export function clearApiToken() {
  OpenAPI.TOKEN = undefined;
  if (typeof window !== 'undefined') {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
}
