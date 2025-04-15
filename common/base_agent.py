from python_a2a import A2AServer, Message, TextContent, MessageRole
from google.adk import Agent, Tool
from typing import Dict, Any, List, Optional
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

class BaseA2AAgent(A2AServer):
    """Base class for all agents combining A2A and ADK capabilities."""
    
    def __init__(self, name: str, description: str, capabilities: Dict[str, str]):
        super().__init__()
        self.name = name
        self.description = description
        self._capabilities = capabilities
        self.adk_agent = self._create_adk_agent()

    def _create_adk_agent(self) -> Agent:
        """Create ADK agent instance - should be overridden by subclasses."""
        return Agent(
            name=self.name,
            description=self.description,
            tools=[],  # Should be overridden by subclasses
            model=settings.DEFAULT_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )

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
            
            # Process the request
            response_data = await self._process_request(request)

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
            required_fields = ["type", "data"]
            if not all(field in request for field in required_fields):
                raise ValueError(f"Missing required fields. Required: {required_fields}")
            return request
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")

    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process the request - should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement _process_request")

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
        return self._capabilities

class BaseTool(Tool):
    """Base class for custom ADK tools."""
    
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)
        self.logger = logging.getLogger(f"{__name__}.{name}")

    async def _execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool - should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement _execute")

    def _validate_input(self, **kwargs) -> bool:
        """Validate input parameters - should be overridden by subclasses."""
        return True

    def _process_results(self, results: Any) -> Dict[str, Any]:
        """Process and structure the results - should be overridden by subclasses."""
        return {"results": results}

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Main execution method with error handling and logging."""
        try:
            if not self._validate_input(**kwargs):
                raise ValueError("Invalid input parameters")
            
            results = await self._execute(**kwargs)
            return self._process_results(results)
        except Exception as e:
            self.logger.error(f"Tool execution failed: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            } 