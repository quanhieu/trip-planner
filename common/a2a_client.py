import httpx

async def call_agent(url: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
