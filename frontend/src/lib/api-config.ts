import { OpenAPI } from './api-client/core/OpenAPI';
import { getAccessToken, setTokens, clearTokens } from './utils/cookies';

/**
 * Configure API client with base URL and auth token
 */
export function configureApiClient() {
  // Set base URL from environment or default to localhost
  OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  // Set token from cookies if available
  if (typeof window !== 'undefined') {
    const token = getAccessToken();
    if (token) {
      OpenAPI.TOKEN = token;
    }
  }
}

/**
 * Update API client token and store in cookies (call after login/signup)
 */
export function setApiToken(accessToken: string, refreshToken: string) {
  OpenAPI.TOKEN = accessToken;
  setTokens(accessToken, refreshToken);
}

/**
 * Clear API client token and remove cookies (call after logout)
 */
export function clearApiToken() {
  OpenAPI.TOKEN = undefined;
  if (typeof window !== 'undefined') {
    clearTokens();
  }
}
