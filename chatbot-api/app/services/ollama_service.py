"""Service for interacting with Ollama API."""

import json
import logging
from typing import AsyncGenerator, Dict, Any, List, Optional
import httpx
from app.config import settings
from app.models import ChatMessage


logger = logging.getLogger(__name__)


class OllamaService:
    """Service class for handling Ollama API interactions."""
    
    def __init__(self, base_url: str = None, model: str = None):
        """Initialize the Ollama service.
        
        Args:
            base_url: Base URL for Ollama API
            model: Default model to use
        """
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.client = httpx.AsyncClient(timeout=120.0)
        
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    async def health_check(self) -> bool:
        """Check if Ollama service is healthy.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def list_models(self) -> List[str]:
        """List available models from Ollama.
        
        Returns:
            List of available model names
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def _build_prompt(self, message: str, conversation_history: List[ChatMessage]) -> str:
        """Build a prompt from the message and conversation history.
        
        Args:
            message: The current user message
            conversation_history: Previous messages in the conversation
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        # Add conversation history
        for msg in conversation_history:
            if msg.role == "user":
                prompt_parts.append(f"Human: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")
            elif msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
        
        # Add current message
        prompt_parts.append(f"Human: {message}")
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    async def generate_response(
        self,
        message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response from Ollama.
        
        Args:
            message: The user's message
            conversation_history: Previous messages in the conversation
            model: Model to use (defaults to configured model)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Yields:
            Response content chunks
        """
        try:
            # Use provided model or default
            selected_model = model or self.model
            conversation_history = conversation_history or []
            
            # Build the prompt
            prompt = self._build_prompt(message, conversation_history)
            
            # Prepare the request payload
            payload = {
                "model": selected_model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature
                }
            }
            
            if max_tokens:
                payload["options"]["num_predict"] = max_tokens
            
            logger.info(f"Generating response with model: {selected_model}")
            
            # Make the streaming request
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk_data = json.loads(line)
                            if "response" in chunk_data:
                                content = chunk_data["response"]
                                if content:  # Only yield non-empty content
                                    yield content
                                    
                                # Check if this is the final chunk
                                if chunk_data.get("done", False):
                                    break
                                    
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse chunk: {line}, error: {e}")
                            continue
                            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Ollama: {e.response.status_code} - {e.response.text}")
            yield f"Error: Failed to generate response (HTTP {e.response.status_code})"
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield f"Error: {str(e)}"
    
    async def generate_complete_response(
        self,
        message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate a complete (non-streaming) response from Ollama.
        
        Args:
            message: The user's message
            conversation_history: Previous messages in the conversation
            model: Model to use (defaults to configured model)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Complete response content
        """
        complete_response = ""
        async for chunk in self.generate_response(
            message, conversation_history, model, temperature, max_tokens
        ):
            complete_response += chunk
        return complete_response.strip() 