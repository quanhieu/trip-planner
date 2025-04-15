from python_a2a import A2AServer, Message, TextContent, MessageRole
from typing import Optional, Dict, Any
import json
import logging
from .adk_integration import SearchAgent
from .providers import SearchService
from common.config import settings

logger = logging.getLogger(__name__)

class SearchA2AServer(A2AServer):
    """A2A server implementation for the search agent."""
    
    def __init__(self):
        super().__init__()
        self.search_agent = SearchAgent()
        self.search_service = SearchService()
        self.capabilities = {
            "search_web": "Search the web for travel-related information",
            "search_places": "Search for specific places, attractions, and accommodations",
            "combine_results": "Combine and deduplicate results from multiple sources"
        }

    async def handle_message(self, message: Message) -> Message:
        """Handle incoming A2A messages."""
        try:
            if not isinstance(message.content, TextContent):
                return self._create_error_response(
                    "Unsupported content type",
                    message
                )

            # Parse the request
            request = self._parse_request(message.content.text)
            
            # Process based on request type
            if request["type"] == "web_search":
                response_data = await self._handle_web_search(request)
            elif request["type"] == "place_search":
                response_data = await self._handle_place_search(request)
            else:
                response_data = {
                    "error": f"Unsupported request type: {request['type']}"
                }

            # Create response message
            return Message(
                content=TextContent(text=json.dumps(response_data)),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return self._create_error_response(str(e), message)

    def _parse_request(self, text: str) -> Dict[str, Any]:
        """Parse the incoming request text."""
        try:
            request = json.loads(text)
            required_fields = ["type", "query"]
            if not all(field in request for field in required_fields):
                raise ValueError(f"Missing required fields. Required: {required_fields}")
            return request
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")

    async def _handle_web_search(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle web search requests using ADK."""
        try:
            # Use ADK search agent
            results = await self.search_agent.process_query(request["query"])
            return {
                "status": "success",
                "type": "web_search",
                "query": request["query"],
                "results": results
            }
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return {
                "status": "error",
                "type": "web_search",
                "error": str(e)
            }

    async def _handle_place_search(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle place search requests using providers."""
        try:
            # Use search service for place-specific searches
            destination = request["query"]
            attractions, restaurants, hotels = await self.search_service.search_all(
                destination
            )
            
            return {
                "status": "success",
                "type": "place_search",
                "query": destination,
                "results": {
                    "attractions": attractions,
                    "restaurants": restaurants,
                    "hotels": hotels
                }
            }
        except Exception as e:
            logger.error(f"Place search failed: {str(e)}")
            return {
                "status": "error",
                "type": "place_search",
                "error": str(e)
            }

    def _create_error_response(self, error_message: str, original_message: Message) -> Message:
        """Create an error response message."""
        return Message(
            content=TextContent(text=json.dumps({
                "status": "error",
                "error": error_message
            })),
            role=MessageRole.AGENT,
            parent_message_id=original_message.message_id,
            conversation_id=original_message.conversation_id
        )

    def get_capabilities(self) -> Dict[str, str]:
        """Return the agent's capabilities."""
        return self.capabilities 