from google.adk import Agent, Tool
from google.adk.tools import google_search
from typing import Dict, Any, List
import asyncio
import logging
from common.config import settings

logger = logging.getLogger(__name__)

class SearchTool(Tool):
    """Custom search tool that combines Google Search with other providers."""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information about places, attractions, and travel destinations"
        )
        self.google_search = google_search.GoogleSearchTool()

    async def _execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute the search using Google Search API and process results."""
        try:
            # Use Google Search API
            search_results = await self.google_search.execute(
                query,
                num_results=settings.MAX_RESULTS_PER_CATEGORY
            )

            # Process and structure the results
            processed_results = []
            for result in search_results:
                processed_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", ""),
                    "published_date": result.get("published", "")
                })

            return {
                "results": processed_results,
                "query": query,
                "total_results": len(processed_results)
            }
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return {"error": str(e), "results": []}

class SearchAgent(Agent):
    """ADK-based search agent with enhanced capabilities."""
    
    def __init__(self):
        super().__init__(
            name="travel_search_agent",
            description="An agent that searches for travel-related information using multiple sources",
            tools=[SearchTool(), google_search.GoogleSearchTool()]
        )
        self.model = settings.DEFAULT_MODEL
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS

    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a search query using multiple tools and combine results."""
        try:
            # Create a comprehensive search prompt
            search_prompt = self._create_search_prompt(query)
            
            # Generate search response using the model
            response = await self.generate(search_prompt)
            
            # Extract and structure the information
            structured_results = await self._structure_results(response)
            
            return structured_results
        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}")
            return {"error": str(e)}

    def _create_search_prompt(self, query: str) -> str:
        """Create a detailed search prompt for better results."""
        return f"""
        Please search for comprehensive information about {query}.
        Focus on:
        1. Key tourist attractions and points of interest
        2. Local restaurants and dining options
        3. Accommodation options
        4. Travel tips and recommendations
        5. Recent reviews and ratings
        
        Provide detailed, factual information with sources where possible.
        """

    async def _structure_results(self, raw_results: str) -> Dict[str, Any]:
        """Structure the raw search results into a organized format."""
        # Implement result structuring logic here
        return {
            "structured_data": raw_results,
            "timestamp": asyncio.get_event_loop().time(),
            "version": "1.0"
        } 