#!/bin/bash

# Setup script for Local Chatbot environment

echo "🚀 Setting up Local Chatbot environment..."

# Create chatbot-api/.env file
ENV_FILE="chatbot-api/.env"

if [ -f "$ENV_FILE" ]; then
    echo "⚠️  $ENV_FILE already exists. Backing up to $ENV_FILE.backup"
    cp "$ENV_FILE" "$ENV_FILE.backup"
fi

echo "📝 Creating $ENV_FILE..."

cat > "$ENV_FILE" << 'EOF'
# Ollama Configuration
OLLAMA_MODEL=qwen3:1.7b
OLLAMA_BASE_URL=http://localhost:11434

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_TITLE=Chatbot API
API_VERSION=1.0.0
API_DESCRIPTION=A ChatGPT-like chatbot API powered by Ollama

# Logging
LOG_LEVEL=INFO

# CORS Configuration (for frontend integration)
ALLOWED_ORIGINS=["*"]
ALLOWED_CREDENTIALS=true
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
EOF

echo "✅ Created $ENV_FILE"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if models exist (this will be done inside the container)
echo "📋 Environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'make prod' to start the production stack"
echo "2. Or run 'make dev' to start the development stack"
echo "3. Access the frontend at http://localhost:3000"
echo "4. Access the API at http://localhost:8000"
echo ""
echo "Note: The first run will download the qwen3:1.7b model (~1.4GB)"
echo "This may take several minutes depending on your internet connection." 