import asyncio
import logging
from common.a2a_client import call_agent
from common.base_agent import BaseAgent
from google.adk.tools import google_search
from common.task_manager import TaskManager
from common.error_handler import ErrorHandler
from common.config import settings
from .model_selector import ModelSelector

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="orchestrator_agent",
            description="Agent điều phối kế hoạch chuyến đi",
            tools=[google_search.GoogleSearchTool()]
        )
        self.task_manager = TaskManager()
        self.model_selector = ModelSelector()

    async def _call_agent_with_retry(self, agent_type: str, payload: dict) -> dict:
        """Call an agent with the appropriate model configuration."""
        # Select appropriate model for the task
        model = self.model_selector.select_model(agent_type, payload)
        model_config = self.model_selector.get_model_config(model)
        
        # Add model configuration to payload
        agent_payload = {
            **payload,
            "model_config": model_config
        }
        
        # Get agent URL from settings based on agent type
        agent_url = getattr(settings, f"{agent_type.upper()}_AGENT_URL")
        
        try:
            return await call_agent(agent_url, agent_payload)
        except Exception as e:
            logger.error(f"Error calling {agent_type} agent: {str(e)}")
            raise

    async def execute(self, payload: dict) -> dict:
        task_id = payload.get("task_id")
        await self.task_manager.create_task(task_id, payload)
        
        try:
            # Gọi Search Agent với model được chọn
            search_result = await self._call_agent_with_retry("search", payload)
            
            # Gọi Entertainment Agent với model được chọn
            ent_payload = payload.copy()
            ent_payload.update({"attractions": search_result.get("attractions", [])})
            entertainment_result = await self._call_agent_with_retry("entertainment", ent_payload)
            
            # Gọi Meal Agent với model được chọn
            meal_payload = payload.copy()
            meal_payload.update({
                "restaurants": search_result.get("restaurants", []),
                "itinerary": entertainment_result.get("itinerary", [])
            })
            meal_result = await self._call_agent_with_retry("meal", meal_payload)
            
            # Gọi Stay Agent với model được chọn
            stay_payload = payload.copy()
            stay_payload.update({"hotels": search_result.get("hotels", [])})
            stay_result = await self._call_agent_with_retry("stay", stay_payload)
            
            # Tổng hợp kết quả từ các agent
            result = {
                "itinerary": entertainment_result.get("itinerary", []),
                "meals": meal_result.get("meals", []),
                "stays": stay_result.get("stays", {}),
                "models_used": {  # Track which models were used
                    "search": self.model_selector.select_model("search", payload),
                    "entertainment": self.model_selector.select_model("entertainment", ent_payload),
                    "meal": self.model_selector.select_model("meal", meal_payload),
                    "stay": self.model_selector.select_model("stay", stay_payload)
                }
            }
            
            await self.task_manager.update_task_status(task_id, "completed", result)
            return result
            
        except Exception as e:
            logger.error(f"Error executing orchestrator task: {str(e)}")
            await self.task_manager.update_task_status(task_id, "failed")
            return await ErrorHandler.handle_error(e)
