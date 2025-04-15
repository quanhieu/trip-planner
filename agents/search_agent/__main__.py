import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from .a2a_server import SearchA2AServer
from common.config import settings
import logging

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Search Agent", description="Travel search agent with A2A and ADK capabilities")

# Initialize A2A server
a2a_server = SearchA2AServer()

class SearchRequest(BaseModel):
    """Search request model."""
    type: str
    query: str
    filters: Optional[Dict[str, Any]] = None

@app.post("/run")
async def run_search(request: SearchRequest):
    """Execute search request."""
    try:
        # Create A2A message from request
        message = a2a_server.create_message(
            content_type="text",
            text=request.json(),
            role="user"
        )
        
        # Process message through A2A server
        response = await a2a_server.handle_message(message)
        
        return response.content.to_dict()
    except Exception as e:
        logger.error(f"Search request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/capabilities")
async def get_capabilities():
    """Get agent capabilities."""
    return a2a_server.get_capabilities()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.AGENT_PORTS["search"],
        log_level=settings.LOG_LEVEL.lower()
    )
