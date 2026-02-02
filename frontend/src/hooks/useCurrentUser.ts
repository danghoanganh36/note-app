/**
 * Hook to fetch and manage current user data
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthenticationService } from '@/lib/api-client/services/AuthenticationService';
import type { UserResponse } from '@/lib/api-client';
import { ApiError } from '@/lib/api-client/core/ApiError';
import { getAccessToken, clearTokens } from '@/lib/utils/cookies';

interface UseCurrentUserReturn {
  user: UserResponse | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useCurrentUser(): UseCurrentUserReturn {
  const router = useRouter();
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUser = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const userData = await AuthenticationService.getMeApiV1AuthMeGet();
      setUser(userData);
    } catch (err: unknown) {
      console.error('Failed to fetch user:', err);
      
      if (err instanceof ApiError && err.status === 401) {
        // Unauthorized - redirect to login
        clearTokens();
        router.push('/login');
      } else {
        setError('Failed to load user data');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const accessToken = getAccessToken();
    
    if (!accessToken) {
      router.push('/login');
      return;
    }
    
    fetchUser();
  }, []);

  return {
    user,
    isLoading,
    error,
    refetch: fetchUser,
  };
}
