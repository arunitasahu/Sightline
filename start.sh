#!/bin/bash

# Memory optimization environment variables
export TF_CPP_MIN_LOG_LEVEL=3
export TF_ENABLE_ONEDNN_OPTS=0
export OMP_NUM_THREADS=1
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1

# Limit Python memory usage
export PYTHONHASHSEED=random
export PYTHONUNBUFFERED=1

# Set maximum memory for the process (in MB)
ulimit -v 524288  # 512MB virtual memory limit

# Start the application with memory-efficient settings
exec gunicorn src.main:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --worker-connections 10 \
    --max-requests 100 \
    --max-requests-jitter 10 \
    --timeout 30 \
    --keep-alive 2 \
    --preload
