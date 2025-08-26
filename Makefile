.PHONY: help install install-dev lint format test clean check-all

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install navspec in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements.txt

lint:  ## Run all linting tools
	@echo "Running flake8..."
	flake8 navspec/ tests/
	@echo "Running mypy..."
	mypy navspec/
	@echo "Running bandit..."
	bandit -r navspec/ -f json -o bandit-report.json || true
	@echo "Linting complete!"

format:  ## Format code with black and isort
	@echo "Formatting with black..."
	black navspec/ tests/
	@echo "Sorting imports with isort..."
	isort navspec/ tests/
	@echo "Formatting complete!"

format-check:  ## Check if code is properly formatted
	@echo "Checking black formatting..."
	black --check navspec/ tests/
	@echo "Checking isort..."
	isort --check-only navspec/ tests/
	@echo "Format check complete!"

test:  ## Run tests
	pytest tests/ -v

test-coverage:  ## Run tests with coverage
	pytest tests/ --cov=navspec --cov-report=html --cov-report=term

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage bandit-report.json

check-all: format-check lint test  ## Run all checks (format, lint, test)

pre-commit-install:  ## Install pre-commit hooks
	pre-commit install

pre-commit-update:  ## Update pre-commit hooks
	pre-commit autoupdate

dev-setup: install-dev pre-commit-install  ## Complete development setup
