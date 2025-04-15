# Trip Planner Technical Context

## Technology Stack

### 1. Core Technologies

- Python 3.9+
- FastAPI
- HTTPX
- Pydantic
- Uvicorn

### 2. AI/LLM Services

- OpenAI GPT-4o (High complexity, creative tasks)
- OpenAI GPT-4o-mini (Medium complexity, basic planning)
- Google Gemini-2.0-flash (Medium complexity, factual queries)
- Anthropic Claude-3.7-sonnet (High complexity, analysis)
- Local LLM support (Ollama)

### 3. Development Tools

- Git for version control
- Docker for containerization
- Poetry for dependency management
- Pytest for testing

## Development Setup

### 1. Environment Setup

```bash
# Clone repository
git clone [repository-url]

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env with required API keys and settings
```

### 2. Running the System

```bash
# Start individual agents
python -m agents.search_agent
python -m agents.entertainment_agent
python -m agents.meal_agent
python -m agents.stay_agent
python -m agents.orchestrator_agent

# Start UI
streamlit run travel_ui.py
```

### 3. Docker Setup

```bash
# Build and run all agents
docker-compose up

# Build and run specific agent
docker-compose up orchestrator_agent
```

## Technical Constraints

### 1. API Limitations

- Rate limits per provider
- Token/request costs
- Response time variations
- Service availability
- Model-specific constraints:
  - Context length limits
  - Cost per token variations
  - Capability differences

### 2. Resource Constraints

- Memory usage limits
- CPU utilization
- Network bandwidth
- Storage capacity
- Model loading overhead

### 3. Security Requirements

- API key protection
- Data encryption
- Input validation
- Error handling
- Model access control

## Dependencies

### 1. External Services

- OpenAI API
- Google Gemini API
- Anthropic API
- Ollama API

### 2. Python Packages

```toml
[dependencies]
fastapi = "^0.68.0"
httpx = "^0.24.0"
pydantic = "^2.0.0"
python-dotenv = "^1.0.0"
uvicorn = "^0.15.0"
streamlit = "^1.18.0"
python-a2a = "^0.1.0"
tenacity = "^8.0.0"
aiohttp = "^3.8.0"
```

### 3. Development Dependencies

```toml
[dev-dependencies]
pytest = "^7.0.0"
pytest-asyncio = "^0.20.0"
black = "^23.0.0"
isort = "^5.12.0"
mypy = "^1.0.0"
```

## System Requirements

### 1. Hardware Requirements

- Minimum 4GB RAM
- 2+ CPU cores
- 10GB storage
- Stable internet connection

### 2. Software Requirements

- Python 3.9+
- Docker (optional)
- Git
- Modern web browser

### 3. Network Requirements

- HTTP/HTTPS access
- WebSocket support
- DNS resolution
- Firewall configuration

## Model Configuration

### 1. Model Capabilities

- GPT-4o:

  - Complexity: HIGH
  - Context Length: 8000
  - Cost per Token: 0.03
  - Strengths: Complex reasoning, creative tasks, detailed planning

- GPT-4o-mini:

  - Complexity: MEDIUM
  - Context Length: 4000
  - Cost per Token: 0.015
  - Strengths: Complex reasoning, basic planning

- Gemini-2.0-flash:

  - Complexity: MEDIUM
  - Context Length: 4000
  - Cost per Token: 0.01
  - Strengths: Factual queries, basic planning, information extraction

- Claude-3.7-sonnet:
  - Complexity: HIGH
  - Context Length: 6000
  - Cost per Token: 0.02
  - Strengths: Analysis, structured output, travel planning

### 2. Selection Criteria

- Strength Match (40% weight)
- Complexity Match (30% weight)
- Cost Efficiency (30% weight)

### 3. Task-Specific Requirements

- Search: Factual queries, information extraction
- Entertainment: Creative tasks, detailed planning
- Meal: Basic planning, analysis
- Stay: Analysis, structured output, travel planning

### 4. Environment Configuration

```
# Environment variables (.env file)
DEFAULT_MODEL=gpt-4o
TEMPERATURE=0.7
MAX_TOKENS=2000
SEARCH_CACHE_DURATION=24
MAX_RESULTS_PER_CATEGORY=10
SEARCH_TIMEOUT=30
LOG_LEVEL=INFO
```
