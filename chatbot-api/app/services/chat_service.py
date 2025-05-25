"""Chat service for managing conversations and generating responses."""

import uuid
import logging
from datetime import datetime
from typing import AsyncGenerator, Dict, List, Optional
from app.models import ChatMessage, ChatRequest, ChatResponse, StreamChunk
from app.services.ollama_service import OllamaService
from app.config import settings


logger = logging.getLogger(__name__)


class ChatService:
    """High-level service for managing chat conversations."""
    
    def __init__(self):
        """Initialize the chat service."""
        self.conversations: Dict[str, List[ChatMessage]] = {}
        self.ollama_service = OllamaService()
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.ollama_service.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.ollama_service.__aexit__(exc_type, exc_val, exc_tb)
    
    def _generate_conversation_id(self) -> str:
        """Generate a unique conversation ID.
        
        Returns:
            Unique conversation identifier
        """
        return str(uuid.uuid4())
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string.
        
        Returns:
            Current timestamp
        """
        return datetime.utcnow().isoformat()
    
    def get_conversation_history(self, conversation_id: str) -> List[ChatMessage]:
        """Get conversation history by ID.
        
        Args:
            conversation_id: Unique conversation identifier
            
        Returns:
            List of chat messages in the conversation
        """
        return self.conversations.get(conversation_id, [])
    
    def add_message_to_conversation(
        self, 
        conversation_id: str, 
        message: ChatMessage
    ) -> None:
        """Add a message to a conversation.
        
        Args:
            conversation_id: Unique conversation identifier
            message: Message to add to the conversation
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        # Set timestamp if not provided
        if not message.timestamp:
            message.timestamp = self._get_current_timestamp()
        
        self.conversations[conversation_id].append(message)
        
        # Keep only last 50 messages to prevent memory issues
        if len(self.conversations[conversation_id]) > 50:
            self.conversations[conversation_id] = self.conversations[conversation_id][-50:]
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation history.
        
        Args:
            conversation_id: Unique conversation identifier
            
        Returns:
            True if conversation was cleared, False if not found
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False
    
    async def process_chat_request(
        self, 
        request: ChatRequest,
        conversation_id: Optional[str] = None
    ) -> str:
        """Process a chat request and return the conversation ID.
        
        Args:
            request: Chat request containing message and parameters
            conversation_id: Optional existing conversation ID
            
        Returns:
            Conversation ID (new or existing)
        """
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = self._generate_conversation_id()
        
        # Add user message to conversation
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=self._get_current_timestamp()
        )
        self.add_message_to_conversation(conversation_id, user_message)
        
        return conversation_id
    
    async def generate_streaming_response(
        self,
        request: ChatRequest,
        conversation_id: str
    ) -> AsyncGenerator[StreamChunk, None]:
        """Generate a streaming chat response.
        
        Args:
            request: Chat request containing message and parameters
            conversation_id: Conversation identifier
            
        Yields:
            StreamChunk objects with response content
        """
        try:
            # Get conversation history (exclude the current user message we just added)
            history = self.get_conversation_history(conversation_id)[:-1]
            
            # Use conversation history from request if provided, otherwise use stored history
            conversation_history = request.conversation_history or history
            
            # Determine the model to use
            model = request.model or settings.ollama_model
            
            # Generate response using Ollama service
            complete_response = ""
            async for chunk in self.ollama_service.generate_response(
                message=request.message,
                conversation_history=conversation_history,
                model=model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                complete_response += chunk
                yield StreamChunk(
                    content=chunk,
                    is_complete=False,
                    model=model
                )
            
            # Send final chunk
            yield StreamChunk(
                content="",
                is_complete=True,
                model=model
            )
            
            # Add assistant response to conversation
            assistant_message = ChatMessage(
                role="assistant",
                content=complete_response.strip(),
                timestamp=self._get_current_timestamp()
            )
            self.add_message_to_conversation(conversation_id, assistant_message)
            
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield StreamChunk(
                content=f"Error: {str(e)}",
                is_complete=True,
                model=request.model or settings.ollama_model
            )
    
    async def generate_complete_response(
        self,
        request: ChatRequest,
        conversation_id: str
    ) -> ChatResponse:
        """Generate a complete (non-streaming) chat response.
        
        Args:
            request: Chat request containing message and parameters
            conversation_id: Conversation identifier
            
        Returns:
            Complete chat response
        """
        try:
            # Get conversation history (exclude the current user message we just added)
            history = self.get_conversation_history(conversation_id)[:-1]
            
            # Use conversation history from request if provided, otherwise use stored history
            conversation_history = request.conversation_history or history
            
            # Determine the model to use
            model = request.model or settings.ollama_model
            
            # Generate complete response using Ollama service
            response_content = await self.ollama_service.generate_complete_response(
                message=request.message,
                conversation_history=conversation_history,
                model=model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            # Add assistant response to conversation
            assistant_message = ChatMessage(
                role="assistant",
                content=response_content,
                timestamp=self._get_current_timestamp()
            )
            self.add_message_to_conversation(conversation_id, assistant_message)
            
            return ChatResponse(
                message=response_content,
                role="assistant",
                model=model,
                conversation_id=conversation_id
            )
            
        except Exception as e:
            logger.error(f"Error generating complete response: {e}")
            return ChatResponse(
                message=f"Error: {str(e)}",
                role="assistant",
                model=request.model or settings.ollama_model,
                conversation_id=conversation_id
            )
    
    async def health_check(self) -> bool:
        """Check if the chat service is healthy.
        
        Returns:
            True if service is healthy, False otherwise
        """
        return await self.ollama_service.health_check()
    
    async def list_available_models(self) -> List[str]:
        """List available models.
        
        Returns:
            List of available model names
        """
        return await self.ollama_service.list_models() 