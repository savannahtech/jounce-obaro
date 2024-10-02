# Run all migrations up to the latest
run-migrations:
	@echo "Running migrations..."
	alembic upgrade head

# Revert the latest migration
undo-migration:
	@echo "Reverting latest migration..."
	alembic downgrade -1

# Create a new migration
create-migration:
	@echo "Creating migrations..."
ifdef MANUAL
	# Manual migrations
	@echo "Manual migrations..."
	alembic revision -m "$(MSG)"
else
	# Autogenerate migrations
	@echo "Autogenerate migrations... $(MSG)"
	alembic revision --autogenerate -m "$(MSG)"
endif

# Install development packages
install-dev:
	@echo "Installing packages..."
	pip-compile requirements.in && pip-sync requirements.txt

# Install packages
install:
	@echo "Installing packages..."
	pip install -r requirements.txt

# Start the FastAPI app for metric simulator
start-simulator:
ifdef PORT
	@echo "Starting app on port ${PORT}..."
	uvicorn metric_simulator.main:app --reload --port ${PORT}
else
	@echo "Starting app on port 8000..."
	uvicorn metric_simulator.main:app --reload
endif

# Start the FastAPI app for metric becnhmark
start-benchmark:
ifdef PORT
	@echo "Starting app on port ${PORT}..."
	uvicorn metric_benchmark.main:app --reload --port ${PORT}
else
	@echo "Starting app on port 8000..."
	uvicorn metric_benchmark.main:app --reload --port 8001
endif

# Run tests
tests:
	@echo "Installing packages..."
	REDIS_HOST=localhost pytest metric_benchmark metric_simulator

start:
	chmod +x ./dev-deploy.sh && ./dev-deploy.sh

# Help command to display available commands
help:
	@echo "Available commands"
	@echo "  make run-migrations    - Run all migrations up to the latest"
	@echo "  make undo-migration    - Revert the latest migration"
	@echo "  make create-migration  - Create a new migration"
	@echo "  make install           - Install packages"
	@echo "  make install-dev       - Install development packages"
	@echo "  make start-simulator   - Start the Simulator FastAPI app"
	@echo "  make start-benchmark   - Start the Benchmark FastAPI app"
	@echo "  make tests   					- Run tests
	@echo "  make start   					- Start applications
	@echo "  make help              - Display this help message"
