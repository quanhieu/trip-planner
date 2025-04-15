import uvicorn
from common.a2a_server import create_app
from task_manager import OrchestratorAgent

agent = OrchestratorAgent()
app = create_app(agent)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
