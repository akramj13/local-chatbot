# Local Chatbot

A complete chatbot application with a FastAPI backend and Next.js frontend, designed to work with Ollama for local AI model inference.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Ollama        │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Local AI)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 11434   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Docker & Docker Compose** installed
2. **Ollama** running locally on port 11434
3. **Models** downloaded in Ollama:
   ```bash
   ollama pull gemma3:1b
   ollama pull qwen3:1.7b
   ```
4. **Environment Configuration**: Create a `.env` file in the `chatbot-api/` directory

### Setup Environment

Create a `.env` file in the `chatbot-api/` directory with the following content:

```bash
# chatbot-api/.env
OLLAMA_MODEL=qwen3:1.7b
OLLAMA_BASE_URL=http://host.docker.internal:11434
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Production Deployment

```bash
# Clone the repository
git clone <your-repo-url>
cd local-chatbot

# Create the environment file
cp chatbot-api/.env.example chatbot-api/.env
# Edit chatbot-api/.env with your settings

# Start the production stack
make prod

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Development Mode

```bash
# Start development stack with hot reloading
make dev

# View logs
make dev-logs

# Stop development stack
make dev-down
```

## 📋 Available Commands

Run `make help` to see all available commands:

```bash
make help          # Show help
make prod          # Start production stack
make dev           # Start development stack
make build         # Build all images
make logs          # View logs
make clean         # Clean up everything
make health        # Check service health
```

## 🔧 Configuration

### Environment Variables

The application uses environment variables defined in `chatbot-api/.env`:

**Backend Configuration (`chatbot-api/.env`):**

- `OLLAMA_BASE_URL`: Ollama server URL (default: `http://host.docker.internal:11434`)
- `OLLAMA_MODEL`: Default model (default: `qwen3:1.7b`)
- `API_HOST`: API host (default: `0.0.0.0`)
- `API_PORT`: API port (default: `8000`)
- `LOG_LEVEL`: Logging level (default: `INFO`, use `DEBUG` for development)

**Frontend Configuration:**

- `NEXT_PUBLIC_API_URL`: Backend API URL (configured in Docker Compose)

### Custom Configuration

Edit the `chatbot-api/.env` file to customize your setup:

```bash
# chatbot-api/.env
OLLAMA_BASE_URL=http://your-ollama-host:11434
OLLAMA_MODEL=your-preferred-model
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

## 🎯 Features

### Backend (FastAPI)

- ✅ **Streaming Chat**: Real-time response streaming
- ✅ **Model Selection**: Dynamic model switching
- ✅ **Health Checks**: Service monitoring
- ✅ **CORS Support**: Frontend integration
- ✅ **OpenAPI Docs**: Auto-generated documentation

### Frontend (Next.js)

- ✅ **Modern UI**: Clean, responsive design
- ✅ **Real-time Streaming**: Live response updates
- ✅ **Model Selector**: Choose from available models
- ✅ **Thinking Models**: Special support for `<think>` tags
- ✅ **Dark Mode**: Automatic theme switching
- ✅ **Mobile Friendly**: Responsive design

### Thinking Models Support

Models that use `<think>` tags get special treatment:

- Collapsible thinking sections
- Visual indicators (⚡ lightning bolt)
- Separate thinking from response content
- "Thinking..." animation during processing

## 🐳 Docker Services

### Production Stack (`docker-compose.yml`)

- **chatbot-api**: Production FastAPI backend
- **chatbot-web**: Production Next.js frontend
- **Health checks**: Automatic service monitoring
- **Networks**: Isolated container communication
- **Environment**: Uses `chatbot-api/.env` file

### Development Stack (`docker-compose.dev.yml`)

- **Hot reloading**: Live code updates
- **Volume mounts**: Direct file system access
- **Debug logging**: Enhanced development logs (LOG_LEVEL=DEBUG)
- **Environment**: Uses `chatbot-api/.env` file + debug overrides

## 📁 Project Structure

```
local-chatbot/
├── chatbot-api/              # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── services/        # Business logic
│   │   └── models.py        # Data models
│   ├── .env                 # Environment configuration
│   ├── Dockerfile
│   └── requirements.txt
├── chatbot-web/             # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app router
│   │   ├── components/     # React components
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml       # Production stack
├── docker-compose.dev.yml   # Development stack
├── Makefile                # Convenience commands
└── README.md               # This file
```

## 🔍 API Endpoints

### Health Check

```bash
GET /api/v1/health
```

### List Models

```bash
GET /api/v1/models
```

### Chat (Streaming)

```bash
POST /api/v1/chat/stream
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "model": "qwen3:1.7b",
  "conversation_history": []
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing .env file**

   ```bash
   # Create the environment file
   cp chatbot-api/.env.example chatbot-api/.env
   # Edit with your settings
   ```

2. **Ollama Connection Failed**

   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags

   # Start Ollama if needed
   ollama serve

   # Update OLLAMA_BASE_URL in chatbot-api/.env if needed
   ```

3. **Models Not Found**

   ```bash
   # List available models
   ollama list

   # Pull required models
   ollama pull gemma3:1b
   ollama pull qwen3:1.7b

   # Update OLLAMA_MODEL in chatbot-api/.env
   ```

4. **Port Conflicts**

   ```bash
   # Check what's using the ports
   lsof -i :3000
   lsof -i :8000

   # Update API_PORT in chatbot-api/.env or change ports in docker-compose.yml
   ```

5. **Docker Issues**

   ```bash
   # Clean up Docker resources
   make clean

   # Rebuild everything
   make build
   ```

### Health Checks

```bash
# Check service health
make health

# View logs
make logs

# Check individual services
curl http://localhost:8000/api/v1/health
curl http://localhost:3000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make dev`
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local AI model inference
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling
