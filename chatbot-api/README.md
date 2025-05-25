# Chatbot API

A ChatGPT-like chatbot API powered by Ollama and FastAPI, featuring streaming responses and conversation management.

## Features

- 🚀 **FastAPI** - High-performance, modern Python web framework
- 🤖 **Ollama Integration** - Local LLM hosting with configurable models
- 📡 **Streaming Responses** - Real-time response streaming like ChatGPT
- 💬 **Conversation Management** - Multi-turn conversations with history
- 🏗️ **Object-Oriented Design** - Clean, maintainable architecture
- 🐳 **Containerized** - Complete Docker setup with Ollama
- 📚 **Auto-generated Docs** - OpenAPI/Swagger documentation

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Make utility (available on most Unix-like systems)

### Getting Started (Using Makefile)

All operations are simplified using the provided Makefile. No need to remember complex Docker commands!

1. **View available commands:**

   ```bash
   make help
   ```

2. **Build and start the API:**

   ```bash
   make build
   make up
   ```

3. **Access your API:**

   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/v1/health

4. **View logs (optional):**
   ```bash
   make logs
   ```

### Managing Models

The API comes with a default model configured in your `.env` file. You can easily add more models:

1. **Add a new model:**

   ```bash
   make add MODEL=gemma3:1b
   make add MODEL=llama3:8b
   make add MODEL=mistral:7b
   ```

2. **List available models:**

   ```bash
   make list
   ```

3. **Update your `.env` file** to change the default model:

   ```bash
   # Edit .env file to use your preferred model
   OLLAMA_MODEL=gemma3:1b
   ```

4. **Restart the service** to use the new default model:
   ```bash
   make restart
   ```

### Development Workflow

- **Start in development mode:** `make dev` (shows logs in foreground)
- **View service status:** `make status`
- **Restart service:** `make restart`
- **Stop service:** `make down`
- **Clean up (remove containers and volumes):** `make clean`
- **Run tests:** `make test`

## Configuration

The API is configured via the `.env` file in the project root. Key settings:

```bash
# Ollama Configuration
OLLAMA_MODEL=gemma3:4b           # Your preferred default model
OLLAMA_BASE_URL=http://localhost:11434

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_TITLE=Chatbot API
API_VERSION=1.0.0
API_DESCRIPTION=A ChatGPT-like chatbot API powered by Ollama

# Logging
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=["*"]
ALLOWED_CREDENTIALS=true
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
```

## API Endpoints

### Core Endpoints

- `GET /` - Service information
- `GET /api/v1/health` - Health check
- `GET /api/v1/models` - List available models

### Chat Endpoints

- `POST /api/v1/chat` - Complete chat response
- `POST /api/v1/chat/stream` - Streaming chat response

### Conversation Management

- `GET /api/v1/conversation/{id}` - Get conversation history
- `DELETE /api/v1/conversation/{id}` - Clear conversation

## Usage Examples

### Simple Chat Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you?",
    "temperature": 0.7
  }'
```

### Streaming Chat Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a short poem about AI",
    "stream": true
  }'
```

### Conversation with History

```bash
curl -X POST "http://localhost:8000/api/v1/chat?conversation_id=my-chat-123" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did we discuss earlier?",
    "conversation_history": [
      {"role": "user", "content": "Tell me about Python"},
      {"role": "assistant", "content": "Python is a programming language..."}
    ]
  }'
```

## Request/Response Models

### ChatRequest

```json
{
  "message": "Your message here",
  "conversation_history": [
    {
      "role": "user|assistant|system",
      "content": "Message content",
      "timestamp": "2024-01-01T00:00:00"
    }
  ],
  "model": "gemma3:4b",
  "max_tokens": 500,
  "temperature": 0.7,
  "stream": true
}
```

### ChatResponse

```json
{
  "message": "Assistant response",
  "role": "assistant",
  "model": "gemma3:4b",
  "conversation_id": "uuid-string"
}
```

### StreamChunk (for streaming)

```json
{
  "content": "Response chunk",
  "is_complete": false,
  "model": "gemma3:4b"
}
```

## Available Make Commands

Run `make help` to see all available commands:

```
add          Pull a new Ollama model (usage: make add MODEL=gemma3:1b)
build        Build the Docker image
clean        Remove containers and volumes
dev          Start in development mode (with logs)
down         Stop the API service
help         Show this help message
list         List all available models in Ollama
logs         View API logs
restart      Restart the API service
status       Show service status
test         Run API tests
up           Start the API service
```

## Architecture

The application follows Object-Oriented Design principles:

```
app/
├── __init__.py
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── models.py            # Pydantic data models
├── api/
│   ├── __init__.py
│   └── routes.py        # API route handlers
└── services/
    ├── __init__.py
    ├── ollama_service.py # Ollama API integration
    └── chat_service.py   # High-level chat management
```

### Key Classes

- **`Settings`** - Configuration management with validation
- **`OllamaService`** - Handles Ollama API interactions and streaming
- **`ChatService`** - Manages conversations and orchestrates responses
- **API Routes** - FastAPI endpoints with proper error handling

## Troubleshooting

### Common Issues

1. **Service won't start**: Run `make status` to check container status
2. **Model download fails**: Ensure internet connection and sufficient disk space
3. **Streaming not working**: Check if client supports Server-Sent Events
4. **Memory issues**: Larger models require more RAM (gemma3:4b ~3GB, llama3:8b ~5GB)

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Should return:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "gemma3:4b",
  "timestamp": "2024-01-01T00:00:00"
}
```

### View Logs

If something isn't working:

```bash
make logs  # View real-time logs
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make test`
5. Submit a pull request

## License

This project is open source and available under the MIT License.
