.PHONY: help setup test docker-up docker-down clean

help:  ## Show this help
	@echo "Marketing IQ - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup:  ## Set up local development environment
	@echo "Setting up local environment..."
	python -m venv venv
	@echo "Activate venv with: .\venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)"
	@echo "Then run: pip install -r backend/requirements.txt"

docker-up:  ## Start local services (Postgres, Redis, MinIO)
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "Services ready!"
	@echo "Postgres: localhost:5432"
	@echo "App DB: localhost:5433"
	@echo "Redis: localhost:6379"
	@echo "MinIO: http://localhost:9001"

docker-down:  ## Stop local services
	docker-compose down

docker-logs:  ## View logs from local services
	docker-compose logs -f

test:  ## Run all tests
	cd backend && pytest tests/ -v

test-unit:  ## Run unit tests only
	cd backend && pytest tests/unit -v

test-integration:  ## Run integration tests only
	cd backend && pytest tests/integration -v

api-local:  ## Run API locally
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:  ## Clean up Python cache and test artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov
