/**
 * Cookie management utilities
 */

import Cookies from 'js-cookie';

const TOKEN_KEYS = {
  ACCESS_TOKEN: 'accessToken',
  REFRESH_TOKEN: 'refreshToken',
} as const;

const COOKIE_OPTIONS = {
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict' as const,
  path: '/',
};

/**
 * Store tokens in cookies
 */
export function setTokens(accessToken: string, refreshToken: string) {
  // Access token expires in 30 minutes
  Cookies.set(TOKEN_KEYS.ACCESS_TOKEN, accessToken, {
    ...COOKIE_OPTIONS,
    expires: 1 / 48, // 30 minutes
  });
  
  // Refresh token expires in 7 days
  Cookies.set(TOKEN_KEYS.REFRESH_TOKEN, refreshToken, {
    ...COOKIE_OPTIONS,
    expires: 7,
  });
}

/**
 * Get access token from cookies
 */
export function getAccessToken(): string | undefined {
  return Cookies.get(TOKEN_KEYS.ACCESS_TOKEN);
}

/**
 * Get refresh token from cookies
 */
export function getRefreshToken(): string | undefined {
  return Cookies.get(TOKEN_KEYS.REFRESH_TOKEN);
}

/**
 * Remove all tokens from cookies
 */
export function clearTokens() {
  Cookies.remove(TOKEN_KEYS.ACCESS_TOKEN, { path: '/' });
  Cookies.remove(TOKEN_KEYS.REFRESH_TOKEN, { path: '/' });
}
