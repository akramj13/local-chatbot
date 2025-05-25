.PHONY: help build up down restart logs test clean add list

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker-compose build

up: ## Start the API service
	docker-compose up -d

down: ## Stop the API service
	docker-compose down

restart: ## Restart the API service
	docker-compose restart

logs: ## View API logs
	docker-compose logs -f chatbot-api

test: ## Run API tests
	python test_api.py

clean: ## Remove containers and volumes
	docker-compose down -v
	docker system prune -f

dev: ## Start in development mode (with logs)
	docker-compose up

status: ## Show service status
	docker-compose ps

add: ## Pull a new Ollama model (usage: make add MODEL=gemma3:1b)
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL parameter is required. Usage: make add MODEL=qwen3:1.7b"; \
		exit 1; \
	fi
	@echo "Pulling model: $(MODEL)"
	@docker exec -it chatbot-api ollama pull $(MODEL)
	@echo "Model $(MODEL) pulled successfully!"

list: ## List all available models in Ollama
	@echo "Available models:"
	@docker exec -it chatbot-api ollama list 