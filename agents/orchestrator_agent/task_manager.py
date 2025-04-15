import asyncio
from common.a2a_client import call_agent

class OrchestratorAgent:
    async def execute(self, payload: dict) -> dict:
        # Gọi Search Agent (port 8001)
        search_url = "http://localhost:8001/run"
        search_result = await call_agent(search_url, payload)
        
        # Gọi Entertainment Agent (port 8002), truyền thêm danh sách attractions từ search
        entertainment_url = "http://localhost:8002/run"
        ent_payload = payload.copy()
        ent_payload.update({"attractions": search_result.get("attractions", [])})
        entertainment_result = await call_agent(entertainment_url, ent_payload)
        
        # Gọi Meal Agent (port 8003), truyền danh sách restaurants và itinerary đã có
        meal_url = "http://localhost:8003/run"
        meal_payload = payload.copy()
        meal_payload.update({
            "restaurants": search_result.get("restaurants", []),
            "itinerary": entertainment_result.get("itinerary", [])
        })
        meal_result = await call_agent(meal_url, meal_payload)
        
        # Gọi Stay Agent (port 8004), truyền danh sách hotels từ search
        stay_url = "http://localhost:8004/run"
        stay_payload = payload.copy()
        stay_payload.update({"hotels": search_result.get("hotels", [])})
        stay_result = await call_agent(stay_url, stay_payload)
        
        # Tổng hợp kết quả từ các agent
        return {
            "itinerary": entertainment_result.get("itinerary", []),
            "meals": meal_result.get("meals", []),
            "stays": stay_result.get("stays", {})
        }
