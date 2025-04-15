from fastapi import FastAPI, Request

def create_app(agent):
    app = FastAPI()

    @app.post("/run")
    async def run(request: Request):
        payload = await request.json()
        result = await agent.execute(payload)
        return result

    return app
