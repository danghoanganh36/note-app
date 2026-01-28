#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const OPENAPI_URL = `${BACKEND_URL}/api/v1/openapi.json`;
const SCHEMA_FILE = path.join(__dirname, '../openapi-schema.json');
const OUTPUT_DIR = path.join(__dirname, '../src/lib/api-client');

console.log('🔄 Generating API client from OpenAPI schema...');
console.log(`📡 Backend URL: ${BACKEND_URL}`);

// Check if backend is running
try {
  const healthCode = execSync(`curl -s -o /dev/null -w "%{http_code}" ${BACKEND_URL}/health`, { 
    stdio: 'pipe',
    encoding: 'utf-8'
  }).trim();
  
  if (healthCode !== '200') {
    throw new Error(`Backend returned status ${healthCode}`);
  }
} catch (error) {
  console.error('❌ Backend is not running!');
  console.error(`   Please start backend: cd backend && uvicorn app.main:app`);
  process.exit(1);
}

// Download OpenAPI schema
try {
  console.log('📥 Downloading OpenAPI schema...');
  execSync(`curl -s ${OPENAPI_URL} -o ${SCHEMA_FILE}`, { stdio: 'inherit' });
} catch (error) {
  console.error('❌ Failed to download OpenAPI schema');
  process.exit(1);
}

// Remove old generated code
if (fs.existsSync(OUTPUT_DIR)) {
  console.log('🗑️  Removing old generated code...');
  fs.rmSync(OUTPUT_DIR, { recursive: true, force: true });
}

// Generate new client
try {
  console.log('⚙️  Generating TypeScript client...');
  
  execSync(
    `npx openapi-typescript-codegen --input ${SCHEMA_FILE} --output ${OUTPUT_DIR} --client axios`,
    { stdio: 'inherit' }
  );
  
  // Clean up schema file
  fs.unlinkSync(SCHEMA_FILE);
  
  console.log('✅ API client generated successfully!');
  console.log(`📁 Location: ${OUTPUT_DIR}`);
  
} catch (error) {
  console.error('❌ Failed to generate API client');
  console.error(error.message);
  if (fs.existsSync(SCHEMA_FILE)) {
    fs.unlinkSync(SCHEMA_FILE);
  }
  process.exit(1);
}
