#!/bin/bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start services
uvicorn metric_simulator.main:app --reload &
uvicorn metric_benchmark.main:app --reload --port 8001
