#!/usr/bin/env sh
set -eu

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WEB_CONCURRENCY:-2}"

echo "Starting CyberSec Alert SaaS on ${HOST}:${PORT} (workers=${WORKERS})"

exec gunicorn backend.main:app \
	-k uvicorn.workers.UvicornWorker \
	--bind "${HOST}:${PORT}" \
	--workers "${WORKERS}" \
	--timeout 120
