from common.base_agent import BaseA2AAgent
from .adk_integration import TripPlanningTool, OptimizationTool
from typing import Dict, Any, List, Optional
import logging
import json
from common.config import settings

logger = logging.getLogger(__name__)

class PlanningAgent(BaseA2AAgent):
    """Planning agent that handles trip planning requests."""
    
    def __init__(self):
        super().__init__(name="planning_agent")
        self.tools = {
            "trip_planning": TripPlanningTool(),
            "trip_optimization": OptimizationTool()
        }

    async def create_adk_agent(self) -> Any:
        """Create ADK agent instance with planning tools."""
        agent = await super().create_adk_agent()
        
        # Register tools with ADK agent
        for tool in self.tools.values():
            await agent.register_tool(tool)
            
        return agent

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming planning requests."""
        try:
            # Parse request
            request = self.parse_request(message)
            if not request:
                return self.create_error_response("Invalid request format")

            # Extract planning parameters
            params = await self._extract_planning_parameters(request)
            if "error" in params:
                return self.create_error_response(params["error"])

            # Generate initial plan
            plan = await self.tools["trip_planning"].execute(**params)
            if "error" in plan:
                return self.create_error_response(plan["error"])

            # Optimize plan if constraints provided
            if params.get("constraints"):
                optimized_plan = await self.tools["trip_optimization"].execute(
                    plan=plan,
                    constraints=params["constraints"]
                )
                if "error" not in optimized_plan:
                    plan = optimized_plan

            return self.create_success_response(plan)

        except Exception as e:
            logger.error(f"Error handling planning request: {str(e)}")
            return self.create_error_response(str(e))

    async def _extract_planning_parameters(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and validate planning parameters from request."""
        try:
            content = request.get("content", {})
            if not isinstance(content, dict):
                content = json.loads(content)

            required_fields = ["destination", "duration"]
            for field in required_fields:
                if field not in content:
                    return {"error": f"Missing required field: {field}"}

            params = {
                "destination": content["destination"],
                "duration": int(content["duration"]),
                "preferences": content.get("preferences", {}),
                "constraints": content.get("constraints", {})
            }

            return params

        except json.JSONDecodeError:
            return {"error": "Invalid JSON format in request content"}
        except ValueError as e:
            return {"error": f"Invalid parameter value: {str(e)}"}
        except Exception as e:
            return {"error": f"Error extracting parameters: {str(e)}"} 