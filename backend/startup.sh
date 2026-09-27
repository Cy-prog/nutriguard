#!/bin/sh
set -e

echo "=== NutriGuard Startup ==="
python migrate_and_seed.py

echo "Starting FastAPI on 0.0.0.0:${PORT:-8000}..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
