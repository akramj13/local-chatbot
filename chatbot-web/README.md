# Local Chatbot Frontend

A modern React/Next.js frontend for the local chatbot API with streaming support and model selection.

## Features

- 🚀 **Streaming Responses**: Real-time streaming of chat responses
- 🤖 **Model Selection**: Choose from available Ollama models
- 🧠 **Thinking Models**: Special support for models with `<think>` tags
- 🌙 **Dark Mode**: Automatic dark/light mode support
- 📱 **Responsive**: Works on desktop and mobile devices
- ⚡ **Modern UI**: Built with Tailwind CSS and Lucide icons

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Running chatbot API (see `../chatbot-api/README.md`)

### Installation

1. Install dependencies:

```bash
npm install
```

2. Set up environment variables:

```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
```

3. Start the development server:

```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Configuration

### Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of the chatbot API (default: `http://localhost:8000/api/v1`)

## Usage

1. **Select a Model**: Choose from available Ollama models in the dropdown
2. **Start Chatting**: Type your message and press Enter or click Send
3. **Thinking Models**: Models with thinking capabilities will show a collapsible "thinking" section
4. **Clear Chat**: Use the Clear button to start a new conversation

## Features in Detail

### Streaming Support

The frontend uses Server-Sent Events (SSE) to stream responses in real-time, providing a smooth chat experience.

### Thinking Models

Models that use `<think>` tags (like reasoning models) get special treatment:

- Thinking content is displayed in a collapsible blue section
- Shows "Thinking..." indicator while the model is processing
- Separates thinking from the final response

### Model Selection

- Automatically loads available models from the API
- Shows model details like parameter size
- Indicates thinking models with a lightning bolt icon
- Remembers selected model during the session

## Project Structure

```
src/
├── app/                 # Next.js app router
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── ChatInterface.tsx    # Main chat interface
│   ├── ChatMessage.tsx      # Individual message component
│   ├── ModelSelector.tsx    # Model selection dropdown
│   └── ThinkingDisplay.tsx  # Thinking content display
├── types/              # TypeScript type definitions
│   └── chat.ts         # Chat-related types
└── utils/              # Utility functions
    ├── api.ts          # API client functions
    └── thinking.ts     # Thinking content parsing
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Fetch API with streaming support

## Troubleshooting

### API Connection Issues

1. Ensure the chatbot API is running on `http://localhost:8000`
2. Check the `NEXT_PUBLIC_API_URL` environment variable
3. Verify CORS is properly configured in the API

### Model Loading Issues

1. Ensure Ollama is running and has models installed
2. Check the API health endpoint: `http://localhost:8000/api/v1/health`
3. Verify the API can connect to Ollama

### Streaming Issues

1. Check browser console for WebSocket/SSE errors
2. Ensure the API streaming endpoint is working
3. Try refreshing the page to reset the connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the local-chatbot application.
