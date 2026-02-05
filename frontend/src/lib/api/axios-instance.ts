/**
 * Axios instance with automatic token refresh interceptor
 */

import axios from 'axios';
import { setupAxiosInterceptor } from '../api-client/core/refreshToken';

// Create axios instance
export const apiAxios = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
});

// Setup automatic token refresh
setupAxiosInterceptor(apiAxios);
