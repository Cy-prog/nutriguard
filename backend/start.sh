#!/bin/bash
set -e
echo "=== NutriGuard Production Startup ==="
echo "Running migrations and seed..."
python migrate_and_seed.py
echo "Starting Uvicorn server on 0.0.0.0:${PORT:-8000}..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
