# Color definitions
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
MAGENTA := \033[35m
CYAN := \033[36m
WHITE := \033[37m
BOLD := \033[1m
RESET := \033[0m

.PHONY: help build up down logs clean dev dev-down dev-logs prod prod-down prod-logs add list

# Default target
help:
	@echo "$(BOLD)$(CYAN)Local Chatbot Docker Compose Commands:$(RESET)"
	@echo ""
	@echo "$(BOLD)$(GREEN)Development:$(RESET)"
	@echo "  $(YELLOW)make dev$(RESET)        - Start development stack with hot reloading"
	@echo "  $(YELLOW)make dev-down$(RESET)   - Stop development stack"
	@echo "  $(YELLOW)make dev-logs$(RESET)   - View development logs"
	@echo ""
	@echo "$(BOLD)$(GREEN)Production:$(RESET)"
	@echo "  $(YELLOW)make prod$(RESET)       - Build and start production stack"
	@echo "  $(YELLOW)make up$(RESET)         - Start production stack (without rebuilding)"
	@echo "  $(YELLOW)make prod-down$(RESET)  - Stop production stack"
	@echo "  $(YELLOW)make prod-logs$(RESET)  - View production logs"
	@echo ""
	@echo "$(BOLD)$(GREEN)Model Management:$(RESET)"
	@echo "  $(YELLOW)make add MODEL=<name>$(RESET)  - Add a new Ollama model (e.g., make add MODEL=gemma3:1b)"
	@echo "  $(YELLOW)make list$(RESET)              - List all available models"
	@echo ""
	@echo "$(BOLD)$(GREEN)General:$(RESET)"
	@echo "  $(YELLOW)make build$(RESET)      - Build all images"
	@echo "  $(YELLOW)make clean$(RESET)      - Remove all containers, images, and volumes"
	@echo "  $(YELLOW)make logs$(RESET)       - View all logs"
	@echo ""
	@echo "$(BOLD)$(MAGENTA)Prerequisites:$(RESET)"
	@echo "  - Docker and Docker Compose installed"
	@echo "  - Ollama running on host (port 11434)"
	@echo "  - Run './setup-env.sh' first to create environment file"

# Development commands
dev:
	@echo "$(GREEN)🚀 Starting development stack...$(RESET)"
	docker-compose -f docker-compose.dev.yml up --build

dev-down:
	@echo "$(RED)🛑 Stopping development stack...$(RESET)"
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	@echo "$(BLUE)📋 Viewing development logs...$(RESET)"
	docker-compose -f docker-compose.dev.yml logs -f

# Production commands
prod:
	@echo "$(GREEN)🏭 Starting production stack...$(RESET)"
	docker-compose up --build -d
	@echo "$(BOLD)$(GREEN)✅ Production stack started!$(RESET)"
	@echo "$(CYAN)Frontend: http://localhost:3000$(RESET)"
	@echo "$(CYAN)Backend API: http://localhost:8000$(RESET)"
	@echo "$(CYAN)API Docs: http://localhost:8000/docs$(RESET)"

prod-down:
	@echo "$(RED)🛑 Stopping production stack...$(RESET)"
	docker-compose down

prod-logs:
	@echo "$(BLUE)📋 Viewing production logs...$(RESET)"
	docker-compose logs -f

# Model management commands
add:
	@if [ -z "$(MODEL)" ]; then \
		echo "$(RED)❌ Error: MODEL parameter is required.$(RESET)"; \
		echo "$(YELLOW)Usage: make add MODEL=<model-name>$(RESET)"; \
		echo ""; \
		echo "$(BOLD)Examples:$(RESET)"; \
		echo "  $(CYAN)make add MODEL=gemma3:1b$(RESET)"; \
		echo "  $(CYAN)make add MODEL=llama3.2:3b$(RESET)"; \
		echo "  $(CYAN)make add MODEL=mistral:7b$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)📥 Pulling model: $(YELLOW)$(MODEL)$(RESET)"
	@if ! docker ps | grep -q chatbot-api; then \
		echo "$(RED)❌ Error: chatbot-api container is not running.$(RESET)"; \
		echo "$(YELLOW)Please start the stack first with 'make prod' or 'make dev'$(RESET)"; \
		exit 1; \
	fi
	@docker exec chatbot-api ollama pull $(MODEL)
	@echo "$(GREEN)✅ Model $(YELLOW)$(MODEL)$(GREEN) pulled successfully!$(RESET)"

list:
	@echo "$(BLUE)📋 Available models:$(RESET)"
	@if ! docker ps | grep -q chatbot-api; then \
		echo "$(RED)❌ Error: chatbot-api container is not running.$(RESET)"; \
		echo "$(YELLOW)Please start the stack first with 'make prod' or 'make dev'$(RESET)"; \
		exit 1; \
	fi
	@docker exec chatbot-api ollama list

# General commands
build:
	@echo "$(YELLOW)🔨 Building all images...$(RESET)"
	docker-compose build
	docker-compose -f docker-compose.dev.yml build

up:
	@echo "$(GREEN)🚀 Starting production stack (without rebuilding)...$(RESET)"
	docker-compose up -d
	@echo "$(BOLD)$(GREEN)✅ Production stack started!$(RESET)"
	@echo "$(CYAN)Frontend: http://localhost:3000$(RESET)"
	@echo "$(CYAN)Backend API: http://localhost:8000$(RESET)"
	@echo "$(CYAN)API Docs: http://localhost:8000/docs$(RESET)"
	open http://localhost:3000

down:
	@echo "$(RED)🛑 Stopping all stacks...$(RESET)"
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

logs:
	@echo "$(BLUE)📋 Viewing logs...$(RESET)"
	docker-compose logs -f

clean:
	@echo "$(MAGENTA)🧹 Cleaning up Docker resources...$(RESET)"
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)✅ Cleanup complete!$(RESET)"

# Health check
health:
	@echo "$(CYAN)🏥 Checking service health...$(RESET)"
	@echo "$(BOLD)API Health:$(RESET)"
	@curl -s http://localhost:8000/api/v1/health | jq . || echo "$(RED)API not responding$(RESET)"
	@echo ""
	@echo "$(BOLD)Frontend Health:$(RESET)"
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "$(RED)Frontend not responding$(RESET)" 