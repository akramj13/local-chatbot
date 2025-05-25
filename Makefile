.PHONY: help build up down logs clean dev dev-down dev-logs prod prod-down prod-logs add list

# Default target
help:
	@echo "Local Chatbot Docker Compose Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev        - Start development stack with hot reloading"
	@echo "  make dev-down   - Stop development stack"
	@echo "  make dev-logs   - View development logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod       - Build and start production stack"
	@echo "  make prod-down  - Stop production stack"
	@echo "  make prod-logs  - View production logs"
	@echo ""
	@echo "Model Management:"
	@echo "  make add MODEL=<name>  - Add a new Ollama model (e.g., make add MODEL=gemma3:1b)"
	@echo "  make list              - List all available models"
	@echo ""
	@echo "General:"
	@echo "  make build      - Build all images"
	@echo "  make clean      - Remove all containers, images, and volumes"
	@echo "  make logs       - View all logs"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - Docker and Docker Compose installed"
	@echo "  - Ollama running on host (port 11434)"
	@echo "  - Models 'gemma3:1b' and 'qwen3:1.7b' available in Ollama"
	@echo "  - Run './setup-env.sh' first to create environment file"

# Development commands
dev:
	@echo "🚀 Starting development stack..."
	docker-compose -f docker-compose.dev.yml up --build

dev-down:
	@echo "🛑 Stopping development stack..."
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	@echo "📋 Viewing development logs..."
	docker-compose -f docker-compose.dev.yml logs -f

# Production commands
prod:
	@echo "🏭 Starting production stack..."
	docker-compose up --build -d
	@echo "✅ Production stack started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

prod-down:
	@echo "🛑 Stopping production stack..."
	docker-compose down

prod-logs:
	@echo "📋 Viewing production logs..."
	docker-compose logs -f

# Model management commands
add:
	@if [ -z "$(MODEL)" ]; then \
		echo "❌ Error: MODEL parameter is required."; \
		echo "Usage: make add MODEL=<model-name>"; \
		echo ""; \
		echo "Examples:"; \
		echo "  make add MODEL=gemma3:1b"; \
		echo "  make add MODEL=llama3.2:3b"; \
		echo "  make add MODEL=mistral:7b"; \
		exit 1; \
	fi
	@echo "📥 Pulling model: $(MODEL)"
	@if ! docker ps | grep -q chatbot-api; then \
		echo "❌ Error: chatbot-api container is not running."; \
		echo "Please start the stack first with 'make prod' or 'make dev'"; \
		exit 1; \
	fi
	@docker exec chatbot-api ollama pull $(MODEL)
	@echo "✅ Model $(MODEL) pulled successfully!"

list:
	@echo "📋 Available models:"
	@if ! docker ps | grep -q chatbot-api; then \
		echo "❌ Error: chatbot-api container is not running."; \
		echo "Please start the stack first with 'make prod' or 'make dev'"; \
		exit 1; \
	fi
	@docker exec chatbot-api ollama list

# General commands
build:
	@echo "🔨 Building all images..."
	docker-compose build
	docker-compose -f docker-compose.dev.yml build

up:
	@echo "🚀 Starting production stack..."
	docker-compose up -d

down:
	@echo "🛑 Stopping all stacks..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

logs:
	@echo "📋 Viewing logs..."
	docker-compose logs -f

clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans
	docker system prune -f
	@echo "✅ Cleanup complete!"

# Health check
health:
	@echo "🏥 Checking service health..."
	@echo "API Health:"
	@curl -s http://localhost:8000/api/v1/health | jq . || echo "API not responding"
	@echo ""
	@echo "Frontend Health:"
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "Frontend not responding" 