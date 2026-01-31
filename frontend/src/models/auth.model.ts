/**
 * Authentication Domain Models
 * Represents business entities and validation rules for authentication
 */

export interface LoginFormData {
  email: string;
  password: string;
}

export interface SignupFormData {
  email: string;
  password: string;
  displayName: string | null;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface AuthError {
  message: string;
  field?: string;
}

export type AuthMode = 'login' | 'signup';

/**
 * Validation rules
 */
export const AUTH_VALIDATION = {
  email: {
    required: true,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: 'Please enter a valid email address',
  },
  password: {
    minLength: 8,
    required: true,
    message: 'Password must be at least 8 characters',
  },
  displayName: {
    minLength: 2,
    maxLength: 100,
    message: 'Name must be between 2-100 characters',
  },
} as const;
