.PHONY: help build run stop logs clean docker-build docker-run docker-stop docker-logs docker-clean compose-up compose-down compose-logs compose-build

# Variables
IMAGE_NAME=code-model-chat
IMAGE_TAG=latest
CONTAINER_NAME=code-model-chat
PORT=5000

help:
	@echo "Code Model Chat - Docker Commands"
	@echo "=================================="
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-build      - Build Docker image"
	@echo "  make docker-run        - Run Docker container"
	@echo "  make docker-stop       - Stop Docker container"
	@echo "  make docker-logs       - View Docker logs"
	@echo "  make docker-clean      - Remove Docker container and image"
	@echo ""
	@echo "Docker Compose Commands:"
	@echo "  make compose-up        - Start services with Docker Compose"
	@echo "  make compose-down      - Stop services with Docker Compose"
	@echo "  make compose-logs      - View Docker Compose logs"
	@echo "  make compose-build     - Build services with Docker Compose"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev               - Run development server"
	@echo "  make test              - Run tests"
	@echo "  make lint              - Run linter"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean             - Clean up temporary files"
	@echo "  make help              - Show this help message"

# Docker Commands
docker-build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "✓ Docker image built: $(IMAGE_NAME):$(IMAGE_TAG)"

docker-run:
	@echo "Running Docker container..."
	docker run -d -p $(PORT):5000 --name $(CONTAINER_NAME) $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✓ Container running at http://localhost:$(PORT)"

docker-stop:
	@echo "Stopping Docker container..."
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	@echo "✓ Container stopped"

docker-logs:
	@echo "Viewing Docker logs..."
	docker logs -f $(CONTAINER_NAME)

docker-clean: docker-stop
	@echo "Cleaning up Docker..."
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	@echo "✓ Docker cleaned up"

# Docker Compose Commands
compose-up:
	@echo "Starting Docker Compose services..."
	docker-compose up -d
	@echo "✓ Services started"
	@echo "✓ Open http://localhost:5000 in your browser"

compose-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down
	@echo "✓ Services stopped"

compose-logs:
	@echo "Viewing Docker Compose logs..."
	docker-compose logs -f

compose-build:
	@echo "Building Docker Compose services..."
	docker-compose build
	@echo "✓ Services built"

compose-prod-up:
	@echo "Starting production Docker Compose services..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✓ Production services started"

compose-prod-down:
	@echo "Stopping production Docker Compose services..."
	docker-compose -f docker-compose.prod.yml down
	@echo "✓ Production services stopped"

# Development Commands
dev:
	@echo "Starting development server..."
	python chat_ui.py

test:
	@echo "Running tests..."
	pytest tests/ -v

lint:
	@echo "Running linter..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Utility Commands
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete || true
	find . -type f -name "*.pyo" -delete || true
	find . -type f -name "*.pyd" -delete || true
	find . -type f -name ".DS_Store" -delete || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	find . -type d -name ".coverage" -exec rm -rf {} + || true
	@echo "✓ Cleaned up"

# Shortcuts
build: docker-build
run: docker-run
stop: docker-stop
logs: docker-logs
up: compose-up
down: compose-down
