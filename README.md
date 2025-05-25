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
2. **Internet connection** for downloading AI models

### Easy Setup (Recommended)

Use the automated setup script:

```bash
# Clone the repository
git clone <your-repo-url>
cd local-chatbot

# Run the setup script
./setup-env.sh

# Start the production stack
make prod
```

The setup script will:

- ✅ Create the required `.env` file
- ✅ Check Docker installation
- ✅ Provide next steps

### Manual Setup

If you prefer manual setup:

1. **Create environment file**:

   ```bash
   # Create chatbot-api/.env
   cat > chatbot-api/.env << 'EOF'
   OLLAMA_MODEL=qwen3:1.7b
   OLLAMA_BASE_URL=http://localhost:11434
   API_HOST=0.0.0.0
   API_PORT=8000
   LOG_LEVEL=INFO
   EOF
   ```

2. **Start the stack**:
   ```bash
   make prod
   ```

### First Run

⏳ **Note**: The first run will download the `qwen3:1.7b` model (~1.4GB). This may take several minutes depending on your internet connection.

### Access the Application

Once the containers are healthy:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

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

## 🤖 Model Management

### Adding New Models

You can add additional Ollama models using the `make add` command:

```bash
# Add a specific model (container must be running)
make add MODEL=gemma3:1b
make add MODEL=llama3.2:3b
make add MODEL=mistral:7b

# List all available models
make list
```

### Changing the Default Model

1. **Edit the environment file**:

   ```bash
   # Edit chatbot-api/.env
   OLLAMA_MODEL=your-preferred-model
   ```

2. **Restart the stack**:
   ```bash
   make prod-down
   make prod
   ```

### Popular Models to Try

| Model         | Size   | Description               |
| ------------- | ------ | ------------------------- |
| `qwen3:1.7b`  | ~1.4GB | Fast, efficient (default) |
| `gemma3:1b`   | ~1.1GB | Very fast, lightweight    |
| `llama3.2:3b` | ~2.0GB | Balanced performance      |
| `mistral:7b`  | ~4.1GB | High quality responses    |
| `llama3.1:8b` | ~4.7GB | Advanced reasoning        |

## 🔧 Configuration

### Environment Variables

The application uses environment variables defined in `chatbot-api/.env`:

**Backend Configuration (`chatbot-api/.env`):**

- `OLLAMA_MODEL`: Default model (default: `qwen3:1.7b`)
- `OLLAMA_BASE_URL`: Ollama server URL (default: `http://localhost:11434`)
- `API_HOST`: API host (default: `0.0.0.0`)
- `API_PORT`: API port (default: `8000`)
- `LOG_LEVEL`: Logging level (default: `INFO`, use `DEBUG` for development)

**Frontend Configuration:**

- `NEXT_PUBLIC_API_URL`: Backend API URL (configured in Docker Compose)

### Custom Configuration

Edit the `chatbot-api/.env` file to customize your setup:

```bash
# chatbot-api/.env
OLLAMA_BASE_URL=http://localhost:11434
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

- **chatbot-api**: Production FastAPI backend with Ollama
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
├── setup-env.sh            # Environment setup script
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
   # Use the setup script
   ./setup-env.sh

   # Or create manually
   cp chatbot-api/.env.example chatbot-api/.env
   ```

2. **Model download taking too long**

   ```bash
   # Check download progress
   docker-compose logs -f chatbot-api

   # Try a smaller model
   # Edit chatbot-api/.env and change OLLAMA_MODEL=gemma3:1b
   ```

3. **Container health check failing**

   ```bash
   # Check if model download is complete
   docker-compose logs chatbot-api

   # Wait for "FastAPI application started" message
   ```

4. **Port conflicts**

   ```bash
   # Check what's using the ports
   lsof -i :3000
   lsof -i :8000

   # Update API_PORT in chatbot-api/.env or change ports in docker-compose.yml
   ```

5. **Docker issues**

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

# List available models
make list
```

### Performance Tips

1. **Use smaller models for faster responses**:

   - `gemma3:1b` - Very fast, good for testing
   - `qwen3:1.7b` - Balanced (default)

2. **Use larger models for better quality**:

   - `llama3.2:3b` - Better reasoning
   - `mistral:7b` - High quality responses

3. **Monitor resource usage**:
   ```bash
   docker stats
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
