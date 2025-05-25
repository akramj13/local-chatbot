#!/bin/bash
set -e

# Start Ollama service in background
echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 2
done

# Pull the default model
echo "Pulling model: ${OLLAMA_MODEL:-qwen3:1.7b}..."
ollama pull ${OLLAMA_MODEL:-qwen3:1.7b}

# Start FastAPI application
echo "Starting FastAPI application..."
exec python -m app.main 