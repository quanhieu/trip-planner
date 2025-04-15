import uvicorn
from common.a2a_server import create_app
from agent import execute

class MealAgent:
    async def execute(self, payload: dict) -> dict:
        return await execute(payload)

agent = MealAgent()
app = create_app(agent)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
