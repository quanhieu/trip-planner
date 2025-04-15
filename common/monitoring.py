from prometheus_client import Counter, Histogram
import structlog

# Metrics
request_counter = Counter('a2a_requests_total', 'Total A2A requests', ['agent', 'endpoint'])
response_time = Histogram('a2a_response_time_seconds', 'Response time in seconds')

# Structured logging
logger = structlog.get_logger()

class MetricsMiddleware:
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        request_counter.labels(
            agent=request.app.state.agent_name,
            endpoint=request.url.path
        ).inc()
        
        response_time.observe(duration)
        return response