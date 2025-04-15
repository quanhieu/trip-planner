import asyncio
import logging
from typing import Dict, List, Any
from .providers import GooglePlacesProvider, TripAdvisorProvider, BookingProvider

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.google_provider = GooglePlacesProvider()
        self.tripadvisor_provider = TripAdvisorProvider()
        self.booking_provider = BookingProvider()

    async def search_attractions(self, destination: str) -> List[Dict[str, Any]]:
        """Search for tourist attractions using multiple providers."""
        try:
            # Search both Google Places and TripAdvisor
            google_results, tripadvisor_results = await asyncio.gather(
                self.google_provider.search_places(
                    query=f"tourist attractions in {destination}",
                    type="tourist_attraction"
                ),
                self.tripadvisor_provider.search_places(
                    location=destination,
                    type="attractions"
                )
            )
            
            # Combine and deduplicate results
            all_results = google_results + tripadvisor_results
            seen_names = set()
            unique_results = []
            
            for result in all_results:
                name = result.get("name", "").lower()
                if name and name not in seen_names:
                    seen_names.add(name)
                    unique_results.append(result)
            
            return unique_results
        except Exception as e:
            logger.error(f"Error searching attractions: {str(e)}")
            return []

    async def search_restaurants(self, destination: str) -> List[Dict[str, Any]]:
        """Search for restaurants using multiple providers."""
        try:
            # Search both Google Places and TripAdvisor
            google_results, tripadvisor_results = await asyncio.gather(
                self.google_provider.search_places(
                    query=f"best restaurants in {destination}",
                    type="restaurant"
                ),
                self.tripadvisor_provider.search_places(
                    location=destination,
                    type="restaurants"
                )
            )
            
            # Combine and deduplicate results
            all_results = google_results + tripadvisor_results
            seen_names = set()
            unique_results = []
            
            for result in all_results:
                name = result.get("name", "").lower()
                if name and name not in seen_names:
                    seen_names.add(name)
                    unique_results.append(result)
            
            return unique_results
        except Exception as e:
            logger.error(f"Error searching restaurants: {str(e)}")
            return []

    async def search_hotels(self, destination: str) -> List[Dict[str, Any]]:
        """Search for hotels using multiple providers."""
        try:
            # Search both Google Places and Booking.com
            google_results, booking_results = await asyncio.gather(
                self.google_provider.search_places(
                    query=f"hotels in {destination}",
                    type="lodging"
                ),
                self.booking_provider.search_hotels(location=destination)
            )
            
            # Combine and deduplicate results
            all_results = google_results + booking_results
            seen_names = set()
            unique_results = []
            
            for result in all_results:
                name = result.get("name", "").lower()
                if name and name not in seen_names:
                    seen_names.add(name)
                    unique_results.append(result)
            
            return unique_results
        except Exception as e:
            logger.error(f"Error searching hotels: {str(e)}")
            return []

    async def search_all(self, destination: str):
        """Search for attractions, restaurants, and hotels in parallel."""
        attractions, restaurants, hotels = await asyncio.gather(
            self.search_attractions(destination),
            self.search_restaurants(destination),
            self.search_hotels(destination)
        )
        return attractions, restaurants, hotels

# Initialize the search service
search_service = SearchService()

async def execute(payload: dict) -> dict:
    """Main execution function for the search agent."""
    try:
        destination = payload.get("destination", "Unknown")
        logger.info(f"Starting search for destination: {destination}")
        
        # Execute all searches in parallel
        attractions, restaurants, hotels = await asyncio.gather(
            search_service.search_attractions(destination),
            search_service.search_restaurants(destination),
            search_service.search_hotels(destination)
        )
        
        logger.info(f"Search completed for {destination}")
        return {
            "attractions": attractions,
            "restaurants": restaurants,
            "hotels": hotels
        }
    except Exception as e:
        logger.error(f"Search execution failed: {str(e)}")
        # Return empty results in case of error
        return {
            "attractions": [],
            "restaurants": [],
            "hotels": [],
            "error": str(e)
        }
