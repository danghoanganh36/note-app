#!/bin/bash
# Render.com start script for FastAPI app

set -e  # Exit on error

echo "==> Installing critical dependencies..."
pip install greenlet email-validator dnspython

# Run database migrations
echo "==> Running database migrations..."
alembic upgrade head || echo "Warning: Migrations failed, continuing..."

# Start the FastAPI application
echo "==> Starting FastAPI server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
