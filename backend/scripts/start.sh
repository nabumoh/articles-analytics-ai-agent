#!/usr/bin/env sh
set -e

export PYTHONPATH=/app

python scripts/load_csv.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
