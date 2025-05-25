FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy startup script and make it executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 11434

# Set default environment variables
ENV OLLAMA_MODEL=qwen2.5:1.5b
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Run the startup script
CMD ["/app/start.sh"]