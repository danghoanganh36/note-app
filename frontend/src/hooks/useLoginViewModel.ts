/**
 * Login ViewModel
 * Manages authentication state and business logic
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthenticationService } from '@/lib/api-client/services/AuthenticationService';
import type { LoginRequest, UserCreate } from '@/lib/api-client';
import { ApiError } from '@/lib/api-client/core/ApiError';
import { configureApiClient, setApiToken } from '@/lib/api-config';
import type { 
  LoginFormData, 
  SignupFormData, 
  AuthMode, 
  AuthError 
} from '@/models/auth.model';

interface UseLoginViewModelReturn {
  // State
  mode: AuthMode;
  email: string;
  password: string;
  displayName: string;
  isLoading: boolean;
  error: AuthError | null;
  
  // Actions
  setMode: (mode: AuthMode) => void;
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  setDisplayName: (name: string) => void;
  toggleMode: () => void;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
}

export function useLoginViewModel(): UseLoginViewModelReturn {
  const router = useRouter();
  
  // State
  const [mode, setMode] = useState<AuthMode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<AuthError | null>(null);

  // Initialize API client
  useEffect(() => {
    configureApiClient();
  }, []);

  // Toggle between login and signup
  const toggleMode = () => {
    setMode(mode === 'login' ? 'signup' : 'login');
    setError(null);
  };

  // Store tokens and redirect
  const handleAuthSuccess = (accessToken: string, refreshToken: string) => {
    setApiToken(accessToken, refreshToken);
    router.push('/dashboard');
  };

  // Login flow
  const handleLogin = async (data: LoginFormData) => {
    const loginData: LoginRequest = {
      email: data.email,
      password: data.password,
    };
    
    const response = await AuthenticationService.signinApiV1AuthSigninPost(loginData);
    handleAuthSuccess(response.access_token, response.refresh_token);
  };

  // Signup flow
  const handleSignup = async (data: SignupFormData) => {
    const signupData: UserCreate = {
      email: data.email,
      password: data.password,
      display_name: data.displayName || null,
    };
    
    // Create user
    await AuthenticationService.signupApiV1AuthSignupPost(signupData);
    
    // Auto-login after signup
    const loginData: LoginRequest = {
      email: data.email,
      password: data.password,
    };
    
    const response = await AuthenticationService.signinApiV1AuthSigninPost(loginData);
    handleAuthSuccess(response.access_token, response.refresh_token);
  };

  // Form submission handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      if (mode === 'login') {
        await handleLogin({ email, password });
      } else {
        await handleSignup({ email, password, displayName: displayName || null });
      }
    } catch (err: unknown) {
      console.error('Authentication error:', err);
      const errorMessage = err instanceof ApiError 
        ? err.body?.detail || err.message
        : 'Authentication failed. Please try again.';
      
      setError({
        message: errorMessage,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return {
    // State
    mode,
    email,
    password,
    displayName,
    isLoading,
    error,
    
    // Actions
    setMode,
    setEmail,
    setPassword,
    setDisplayName,
    toggleMode,
    handleSubmit,
  };
}
