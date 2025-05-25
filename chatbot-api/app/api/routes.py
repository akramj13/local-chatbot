"""API routes for the chatbot service."""

import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.models import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse, 
    ErrorResponse,
    StreamChunk
)
from app.services.chat_service import ChatService
from app.config import settings


logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Global chat service instance
chat_service = ChatService()


@router.on_event("startup")
async def startup_event():
    """Initialize the chat service on startup."""
    await chat_service.__aenter__()


@router.on_event("shutdown")
async def shutdown_event():
    """Clean up the chat service on shutdown."""
    await chat_service.__aexit__(None, None, None)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify service status."""
    try:
        is_healthy = await chat_service.health_check()
        
        if not is_healthy:
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available"
            )
        
        return HealthResponse(
            status="healthy",
            version=settings.api_version,
            model=settings.ollama_model,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )


@router.get("/models")
async def list_models():
    """List available models from Ollama."""
    try:
        models = await chat_service.list_available_models()
        return {
            "models": models,
            "default_model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve models: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_complete(
    request: ChatRequest,
    conversation_id: Optional[str] = Query(None, description="Optional conversation ID")
):
    """Generate a complete (non-streaming) chat response."""
    try:
        # Process the chat request
        conv_id = await chat_service.process_chat_request(request, conversation_id)
        
        # Generate complete response
        response = await chat_service.generate_complete_response(request, conv_id)
        
        return response
        
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    conversation_id: Optional[str] = Query(None, description="Optional conversation ID")
):
    """Generate a streaming chat response."""
    try:
        # Process the chat request
        conv_id = await chat_service.process_chat_request(request, conversation_id)
        
        async def generate_stream():
            """Generate streaming response chunks."""
            try:
                async for chunk in chat_service.generate_streaming_response(request, conv_id):
                    # Format as Server-Sent Events
                    chunk_json = chunk.model_dump_json()
                    yield f"data: {chunk_json}\n\n"
                    
                    # Send final event when complete
                    if chunk.is_complete:
                        yield f"data: [DONE]\n\n"
                        break
                        
            except Exception as e:
                logger.error(f"Error in streaming response: {e}")
                error_chunk = StreamChunk(
                    content=f"Error: {str(e)}",
                    is_complete=True,
                    model=request.model or settings.ollama_model
                )
                yield f"data: {error_chunk.model_dump_json()}\n\n"
                yield f"data: [DONE]\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat streaming: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate streaming response: {str(e)}"
        )


@router.get("/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get conversation history by ID."""
    try:
        history = chat_service.get_conversation_history(conversation_id)
        return {
            "conversation_id": conversation_id,
            "message_count": len(history),
            "messages": history
        }
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversation: {str(e)}"
        )


@router.delete("/conversation/{conversation_id}")
async def clear_conversation_history(conversation_id: str):
    """Clear conversation history by ID."""
    try:
        success = chat_service.clear_conversation(conversation_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        
        return {
            "message": f"Conversation {conversation_id} cleared successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear conversation: {str(e)}"
        ) 