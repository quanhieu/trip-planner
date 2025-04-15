from typing import List, Dict, Any
import aiohttp
import logging
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
from common.config import settings

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
        self.cache = SearchCache(expire_hours=settings.SEARCH_CACHE_DURATION)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _make_request(self, session: aiohttp.ClientSession, url: str, params: Dict) -> Dict:
        try:
            async with session.get(url, params=params, timeout=settings.SEARCH_TIMEOUT) as response:
                if response.status >= 400:
                    logger.error(f"Google Places API error: {response.status}")
                    raise Exception(f"API error: {response.status}")
                return await response.json()
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    async def search_places(self, query: str, type: str = None) -> List[Dict[str, Any]]:
        cache_key = f"google_places:{query}:{type}"
        
        async def fetch():
            async with aiohttp.ClientSession() as session:
                url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
                params = {
                    "query": query,
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
        self.cache = SearchCache(expire_hours=settings.SEARCH_CACHE_DURATION)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search_places(self, location: str, type: str = None) -> List[Dict[str, Any]]:
        cache_key = f"tripadvisor:{location}:{type}"
        
        async def fetch():
            async with aiohttp.ClientSession() as session:
                url = "https://api.content.tripadvisor.com/api/v1/location/search"
                params = {
                    "key": self.api_key,
                    "searchQuery": location,
                    "category": type,
                    "language": "vi"
                }
                try:
                    async with session.get(url, params=params, timeout=settings.SEARCH_TIMEOUT) as response:
                        if response.status >= 400:
                            logger.error(f"TripAdvisor API error: {response.status}")
                            return []
                        data = await response.json()
                        return data.get("data", [])[:settings.MAX_RESULTS_PER_CATEGORY]
                except Exception as e:
                    logger.error(f"TripAdvisor request failed: {str(e)}")
                    return []

        return await self.cache.get_or_fetch(cache_key, fetch)

class BookingProvider:
    def __init__(self):
        self.api_key = settings.BOOKING_API_KEY
        self.cache = SearchCache(expire_hours=settings.SEARCH_CACHE_DURATION)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search_hotels(self, location: str) -> List[Dict[str, Any]]:
        cache_key = f"booking:{location}"
        
        async def fetch():
            async with aiohttp.ClientSession() as session:
                url = "https://distribution-xml.booking.com/json/bookings"
                params = {
                    "city": location,
                    "apikey": self.api_key
                }
                try:
                    async with session.get(url, params=params, timeout=settings.SEARCH_TIMEOUT) as response:
                        if response.status >= 400:
                            logger.error(f"Booking.com API error: {response.status}")
                            return []
                        data = await response.json()
                        return data.get("hotels", [])[:settings.MAX_RESULTS_PER_CATEGORY]
                except Exception as e:
                    logger.error(f"Booking.com request failed: {str(e)}")
                    return []

        return await self.cache.get_or_fetch(cache_key, fetch) 