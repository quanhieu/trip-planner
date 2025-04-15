from typing import List, Dict, Any
import aiohttp
import logging
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
from common.config import settings
import asyncio

logger = logging.getLogger(__name__)

class SearchCache:
    def __init__(self, expire_hours: int = 24):
        self.cache = {}
        self.expire_time = timedelta(hours=expire_hours)

    async def get_or_fetch(self, key: str, fetch_func):
        now = datetime.now()
        if key in self.cache:
            data, timestamp = self.cache[key]
            if now - timestamp < self.expire_time:
                logger.debug(f"Cache hit for key: {key}")
                return data
        logger.debug(f"Cache miss for key: {key}")
        data = await fetch_func()
        self.cache[key] = (data, now)
        return data

class GooglePlacesProvider:
    def __init__(self):
        self.api_key = settings.GOOGLE_PLACES_API_KEY
        if not self.api_key:
            logger.warning("GOOGLE_PLACES_API_KEY not set. Google Places searches will fail.")
        self.cache = SearchCache(expire_hours=settings.SEARCH_CACHE_DURATION)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _make_request(self, session: aiohttp.ClientSession, url: str, params: Dict) -> Dict:
        if not self.api_key:
            logger.error("API key not set for Google Places. Cannot make request.")
            return {"results": [], "error": "API key not configured"}

        try:
            async with session.get(url, params=params, timeout=settings.SEARCH_TIMEOUT) as response:
                if response.status == 403:
                    logger.error("Google Places API access forbidden. Check API key validity.")
                    return {"results": [], "error": "API access forbidden"}
                elif response.status == 429:
                    logger.error("Google Places API rate limit exceeded.")
                    return {"results": [], "error": "Rate limit exceeded"}
                elif response.status >= 400:
                    logger.error(f"Google Places API error: HTTP {response.status}")
                    return {"results": [], "error": f"API error: HTTP {response.status}"}
                
                data = await response.json()
                status = data.get("status")
                if status and status != "OK":
                    logger.error(f"Google Places API returned error status: {status}")
                    return {"results": [], "error": f"API error: {status}"}
                
                return data
        except asyncio.TimeoutError:
            logger.error(f"Request to {url} timed out after {settings.SEARCH_TIMEOUT}s")
            return {"results": [], "error": "Request timed out"}
        except Exception as e:
            logger.error(f"Request to {url} failed: {str(e)}")
            return {"results": [], "error": str(e)}

    async def search_places(self, query: str = None, location: str = None, destination: str = None, type: str = None) -> List[Dict[str, Any]]:
        """
        Search for places using the Google Places API.
        
        Args:
            query: The search query.
            location: Alias for query.
            destination: Alias for query.
            type: The type of place to search for.
            
        Returns:
            A list of places.
        """
        # Use the first non-None parameter as the search query
        search_query = query or location or destination
        if not search_query:
            logger.error("No search query provided for Google Places search")
            return []
        
        cache_key = f"google_places:{search_query}:{type}"
        
        async def fetch():
            async with aiohttp.ClientSession() as session:
                url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
                params = {
                    "query": search_query,
                    "key": self.api_key,
                    "type": type
                }
                data = await self._make_request(session, url, params)
                results = data.get("results", [])[:settings.MAX_RESULTS_PER_CATEGORY]
                return [self._process_place(place) for place in results]
        
        return await self.cache.get_or_fetch(cache_key, fetch)

    def _process_place(self, place: Dict) -> Dict:
        return {
            "name": place.get("name", ""),
            "address": place.get("formatted_address", ""),
            "rating": place.get("rating", 0.0),
            "reviews": place.get("user_ratings_total", 0),
            "location": place.get("geometry", {}).get("location", {}),
            "photos": [photo.get("photo_reference", "") for photo in place.get("photos", [])],
            "place_id": place.get("place_id", ""),
            "types": place.get("types", [])
        }

class TripAdvisorProvider:
    def __init__(self):
        self.api_key = settings.TRIPADVISOR_API_KEY
        if not self.api_key:
            logger.warning("TRIPADVISOR_API_KEY not set. TripAdvisor searches will fail.")
        self.cache = SearchCache(expire_hours=settings.SEARCH_CACHE_DURATION)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search_places(self, location: str = None, query: str = None, destination: str = None, type: str = None) -> List[Dict[str, Any]]:
        """
        Search for places using the TripAdvisor API.
        
        Args:
            location: The location to search for.
            query: Alias for location.
            destination: Alias for location.
            type: The type of place to search for.
            
        Returns:
            A list of places.
        """
        if not self.api_key:
            logger.error("API key not set for TripAdvisor. Cannot make request.")
            return []
        
        # Use the first non-None parameter as the search query
        search_location = location or query or destination
        if not search_location:
            logger.error("No location provided for TripAdvisor search")
            return []
        
        cache_key = f"tripadvisor:{search_location}:{type}"
        
        async def fetch():
            async with aiohttp.ClientSession() as session:
                url = "https://api.content.tripadvisor.com/api/v1/location/search"
                params = {
                    "key": self.api_key,
                    "searchQuery": search_location,
                    "category": type,
                    "language": "vi"
                }
                try:
                    async with session.get(url, params=params, timeout=settings.SEARCH_TIMEOUT) as response:
                        if response.status == 403:
                            logger.error("TripAdvisor API access forbidden. Check API key validity.")
                            return []
                        elif response.status == 429:
                            logger.error("TripAdvisor API rate limit exceeded.")
                            return []
                        elif response.status >= 400:
                            logger.error(f"TripAdvisor API error: {response.status}")
                            return []
                        data = await response.json()
                        return data.get("data", [])[:settings.MAX_RESULTS_PER_CATEGORY]
                except asyncio.TimeoutError:
                    logger.error(f"TripAdvisor request timed out after {settings.SEARCH_TIMEOUT}s")
                    return []
                except Exception as e:
                    logger.error(f"TripAdvisor request failed: {str(e)}")
                    return []

        return await self.cache.get_or_fetch(cache_key, fetch)

class BookingProvider:
    def __init__(self):
        self.api_key = settings.BOOKING_API_KEY
        if not self.api_key:
            logger.warning("BOOKING_API_KEY not set. Booking.com searches will fail.")
        self.cache = SearchCache(expire_hours=settings.SEARCH_CACHE_DURATION)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search_hotels(self, location: str = None, query: str = None, destination: str = None) -> List[Dict[str, Any]]:
        """
        Search for hotels using the Booking.com API.
        
        Args:
            location: The location to search for hotels.
            query: Alias for location.
            destination: Alias for location.
            
        Returns:
            A list of hotels.
        """
        if not self.api_key:
            logger.error("API key not set for Booking.com. Cannot make request.")
            return []
        
        # Use the first non-None parameter as the search location
        search_location = location or query or destination
        if not search_location:
            logger.error("No location provided for Booking.com search")
            return []
        
        cache_key = f"booking:{search_location}"
        
        async def fetch():
            async with aiohttp.ClientSession() as session:
                url = "https://distribution-xml.booking.com/json/bookings"
                params = {
                    "city": search_location,
                    "apikey": self.api_key
                }
                try:
                    async with session.get(url, params=params, timeout=settings.SEARCH_TIMEOUT) as response:
                        if response.status == 403:
                            logger.error("Booking.com API access forbidden. Check API key validity.")
                            return []
                        elif response.status == 429:
                            logger.error("Booking.com API rate limit exceeded.")
                            return []
                        elif response.status >= 400:
                            logger.error(f"Booking.com API error: {response.status}")
                            return []
                        data = await response.json()
                        return data.get("hotels", [])[:settings.MAX_RESULTS_PER_CATEGORY]
                except asyncio.TimeoutError:
                    logger.error(f"Booking.com request timed out after {settings.SEARCH_TIMEOUT}s")
                    return []
                except Exception as e:
                    logger.error(f"Booking.com request failed: {str(e)}")
                    return []

        return await self.cache.get_or_fetch(cache_key, fetch) 