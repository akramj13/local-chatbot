"""Data models for the chatbot API."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Represents a chat message with role and content."""
    
    role: str = Field(..., description="The role of the message sender (user, assistant, system)")
    content: str = Field(..., description="The content of the message")
    timestamp: Optional[str] = Field(None, description="Timestamp of the message")


class ChatRequest(BaseModel):
    """Request model for chat completion."""
    
    message: str = Field(..., description="The user's message")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=[], 
        description="Previous messages in the conversation"
    )
    model: Optional[str] = Field(None, description="Override the default model")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    stream: bool = Field(True, description="Whether to stream the response")


class ChatResponse(BaseModel):
    """Response model for chat completion."""
    
    message: str = Field(..., description="The assistant's response")
    role: str = Field(default="assistant", description="The role of the responder")
    model: str = Field(..., description="The model used for generation")
    conversation_id: Optional[str] = Field(None, description="Unique conversation identifier")


class StreamChunk(BaseModel):
    """Model for streaming response chunks."""
    
    content: str = Field(..., description="The content chunk")
    is_complete: bool = Field(default=False, description="Whether this is the final chunk")
    model: str = Field(..., description="The model used for generation")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    model: str = Field(..., description="Current Ollama model")
    timestamp: str = Field(..., description="Health check timestamp") 