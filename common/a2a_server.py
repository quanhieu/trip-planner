from fastapi import FastAPI, Request

def create_app(agent):
    app = FastAPI()

    @app.post("/run")
    async def run(request: Request):
        payload = await request.json()
        result = await agent.execute(payload)
        return result

    @app.get("/.well-known/agent-card")
    async def get_agent_card():
        return agent.get_card()

    return app
