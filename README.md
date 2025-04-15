# Trip Planner Application

## Introduction

This application uses a multi-agent architecture with ADK and A2A protocol. The agents (built with FastAPI) communicate with each other to create a trip plan consisting of 1 orchestrator agent, 1 internet search agent, 1 entertainment itinerary agent, 1 meal planning agent, and 1 accommodation suggestion agent. The user interface is built with Streamlit. It uses models such as OpenAI 4o mini, Gemini, Grok, and Claude 3.7.

## Project Structure

- **agents/**: Contains individual agents:
  - `orchestrator_agent/`: Orchestrator agent that aggregates results from child agents.
  - `search_agent/`: Agent for searching factual information (attractions, restaurants, hotels).
  - `entertainment_agent/`: Agent for planning entertainment itineraries.
  - `meal_agent/`: Agent for meal planning.
  - `stay_agent/`: Agent for accommodation suggestions.
- **common/**: Shared code for A2A communication and configuration.
  - `a2a_server.py`: Basic FastAPI server for agents.
  - `a2a_client.py`: Client for communication between agents.
  - `config.py`: Configuration and environment variable management.
- **travel_ui.py**: Frontend interface (Streamlit).
- **requirements.txt**: List of dependencies.
- **.env.template**: Environment configuration template.
- **README.md**: Application instructions.

## Installation and Execution Guide

1. **Create a virtual environment and install libraries:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/Mac (Windows: .venv\Scripts\activate)
   pip install -r requirements.txt
   ```

2. **Set up the environment:**

   ```bash
   # Copy the environment template file
   cp .env.template .env

   # Edit the .env file with necessary information:
   # - Add API keys for services (OpenAI, Gemini, Claude)
   # - Adjust agent URLs if needed
   # - Configure model and application parameters
   ```

3. **Run the agents (each agent in a separate terminal):**

   ```bash
   # Run Search Agent (port 8001)
   python -m agents.search_agent

   # Run Entertainment Agent (port 8002)
   python -m agents.entertainment_agent

   # Run Meal Agent (port 8003)
   python -m agents.meal_agent

   # Run Stay Agent (port 8004)
   python -m agents.stay_agent

   # Run Orchestrator Agent (port 8000)
   python -m agents.orchestrator_agent
   ```

4. **Run the user interface (Streamlit):**

   ```bash
   streamlit run travel_ui.py
   ```

   Open your browser and access the displayed address (usually http://localhost:8501).

5. **Using the application:**
   - Enter trip information: destination, travel dates, number of people, and budget per person.
   - Click "Plan Trip" to call the Orchestrator, which then calls the child agents sequentially.
   - Results (itinerary, meal plan, accommodation suggestions) will be displayed on the Streamlit interface.

## Environment Variables

Important environment variables in the `.env` file:

- **API Keys:**

  - `OPENAI_API_KEY`: API key for OpenAI
  - `GEMINI_API_KEY`: API key for Google Gemini
  - `CLAUDE_API_KEY`: API key for Anthropic Claude
  <!-- - `OLLAMA_API_URL`: URL for Ollama API (default: http://localhost:11434) -->

- **Agent URLs:**

  - `ORCHESTRATOR_URL`: URL of the orchestrator agent
  - `SEARCH_AGENT_URL`: URL of the search agent
  - `ENTERTAINMENT_AGENT_URL`: URL of the entertainment itinerary agent
  - `MEAL_AGENT_URL`: URL of the meal planning agent
  - `STAY_AGENT_URL`: URL of the accommodation suggestion agent

- **Model Configuration:**

  <!-- - `DEFAULT_MODEL`: Default model (e.g., gpt-4) -->

  - `TEMPERATURE`: Model creativity level (0-1)
  - `MAX_TOKENS`: Maximum tokens for each call

- **Application Settings:**
  - `DEBUG`: Debug mode (true/false)
  - `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

## Notes

- Ensure you've correctly configured the API keys in the `.env` file before running the application.
- Check that the default ports (8000-8004) are not already in use.
- In a production environment, you should change the agent URLs to the actual server addresses.
- Make sure to secure the `.env` file and not commit it to git.

## Conclusion

The code above provides a complete example of how to build a multi-agent trip planning application using ADK, A2A, FastAPI, and Streamlit. You can extend and integrate additional functionality (e.g., real search API calls, connection to actual AI models) according to your specific needs. If you have any questions or need further assistance, please let me know!

---

<!-- ```
trip_planner/
├── agents/
│   ├── orchestrator_agent/
│   │   ├── __main__.py          # Launch FastAPI for orchestrator (port 8000)
│   │   ├── task_manager.py      # Logic for calling child agents and aggregating results
│   │   └── agent.json           # Metadata for orchestrator agent
│   ├── search_agent/
│   │   ├── __main__.py          # Launch FastAPI for search agent (port 8001)
│   │   ├── agent_logic.py       # Logic for performing "web search"
│   │   └── agent.json           # Metadata for search agent
│   ├── entertainment_agent/
│   │   ├── __main__.py          # Launch FastAPI for entertainment agent (port 8002)
│   │   ├── agent.py             # Logic for entertainment itinerary planning
│   │   └── agent.json           # Metadata for entertainment agent
│   ├── meal_agent/
│   │   ├── __main__.py          # Launch FastAPI for meal agent (port 8003)
│   │   ├── agent.py             # Logic for meal planning
│   │   └── agent.json           # Metadata for meal agent
│   └── stay_agent/
│       ├── __main__.py          # Launch FastAPI for stay agent (port 8004)
│       ├── agent.py             # Logic for suggesting suitable accommodations
│       └── agent.json           # Metadata for stay agent
├── common/
│   ├── a2a_server.py            # Create FastAPI app with /run endpoint for each agent
│   └── a2a_client.py            # Utility functions for calling APIs of other agents (A2A client)
├── travel_ui.py                 # Streamlit interface (frontend)
├── requirements.txt             # List of libraries to install
├── Dockerfile                   # Dockerfile for the entire project
├── docker-compose.yml           # Defines services using Docker Compose
└── README.md                    # Deployment instructions

``` -->
