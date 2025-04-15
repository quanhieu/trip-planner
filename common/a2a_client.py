import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class A2AClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._circuit_breaker = CircuitBreaker()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def call_agent(self, endpoint: str, payload: dict) -> dict:
        if not self._circuit_breaker.is_available():
            raise ServiceUnavailableError()
            
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(f"{self.base_url}/{endpoint}", json=payload)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self._circuit_breaker.record_failure()
            raise
