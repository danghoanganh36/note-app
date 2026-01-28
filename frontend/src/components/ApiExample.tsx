/**
 * Example API Usage Component
 * Demonstrates how to use the auto-generated API client
 */

'use client';

import { useState, useEffect } from 'react';
import { DefaultService } from '@/lib/api';

export default function ApiExample() {
  const [health, setHealth] = useState<any>(null);
  const [dbTest, setDbTest] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        
        // Call auto-generated API methods
        const healthData = await DefaultService.healthCheckHealthGet();
        setHealth(healthData);
        
        const dbData = await DefaultService.testDatabaseDbTestGet();
        setDbTest(dbData);
        
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded">
        <h3 className="text-red-800 font-semibold">Error</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="bg-green-50 border border-green-200 rounded p-4">
        <h3 className="font-semibold text-green-800">Health Check</h3>
        <pre className="mt-2 text-sm text-green-700">
          {JSON.stringify(health, null, 2)}
        </pre>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded p-4">
        <h3 className="font-semibold text-blue-800">Database Test</h3>
        <pre className="mt-2 text-sm text-blue-700">
          {JSON.stringify(dbTest, null, 2)}
        </pre>
      </div>
    </div>
  );
}
