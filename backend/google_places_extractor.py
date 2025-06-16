import googlemaps
import pandas as pd
import json
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PlaceReview:
    place_id: str
    place_name: str
    author_name: str
    rating: int
    text: str
    time: int
    relative_time_description: str
    language: str

@dataclass
class PlaceInfo:
    place_id: str
    name: str
    rating: float
    user_ratings_total: int
    reviews: List[PlaceReview]
    address: str
    phone_number: str
    website: str
    business_status: str
    price_level: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]

class GooglePlacesReviewsAPI:
    def __init__(self, api_key: str):
        """
        Initialize the Google Places API client
        
        Args:
            api_key: Your Google Places API key
        """
        self.client = googlemaps.Client(key=api_key)
        self.places_data = []
        
    def get_place_details(self, place_id: str, fields: List[str] = None, cost_optimized: bool = False) -> Optional[Dict]:
        """
        Get detailed information about a place including reviews
        
        Args:
            place_id: Google Places ID
            fields: List of fields to retrieve (cost optimization)
            cost_optimized: If True, use only Essential tier fields for minimal cost
            
        Returns:
            Place details dictionary or None if error
        """
        if fields is None:
            if cost_optimized:
                # COST-OPTIMIZED: Essential tier only ($5/1000 requests)
                fields = [
                    'place_id', 'name', 'formatted_address', 'geometry'
                ]
            else:
                # FULL DATA: Mix of Pro + Enterprise + Atmosphere tiers
                # Pro tier ($17/1000): business_status
                # Enterprise tier ($20/1000): rating, user_ratings_total, formatted_phone_number, website, price_level
                # Enterprise + Atmosphere tier ($25/1000): reviews
                fields = [
                    'place_id', 'name', 'rating', 'user_ratings_total',
                    'reviews', 'formatted_address', 'formatted_phone_number',
                    'website', 'business_status', 'price_level', 'geometry'
                ]
        
        try:
            # Add delay to respect rate limits
            time.sleep(0.1)
            
            result = self.client.place(
                place_id=place_id,
                fields=fields,
                language='en'  # Set language for consistency
            )
            
            logger.info(f"Successfully fetched data for place_id: {place_id}")
            return result.get('result', {})
            
        except Exception as e:
            logger.error(f"Error fetching place details for {place_id}: {str(e)}")
            return None
    
    def process_place_data(self, place_data: Dict, place_id: str) -> PlaceInfo:
        """
        Process raw place data into structured format
        
        Args:
            place_data: Raw data from Google Places API
            place_id: The place ID
            
        Returns:
            PlaceInfo object
        """
        reviews = []
        
        # Process reviews if available
        if 'reviews' in place_data:
            for review in place_data['reviews']:
                place_review = PlaceReview(
                    place_id=place_id,
                    place_name=place_data.get('name', ''),
                    author_name=review.get('author_name', ''),
                    rating=review.get('rating', 0),
                    text=review.get('text', ''),
                    time=review.get('time', 0),
                    relative_time_description=review.get('relative_time_description', ''),
                    language=review.get('language', 'en')
                )
                reviews.append(place_review)
        
        # Extract coordinates from geometry data
        latitude = None
        longitude = None
        if 'geometry' in place_data and 'location' in place_data['geometry']:
            location = place_data['geometry']['location']
            latitude = location.get('lat')
            longitude = location.get('lng')
        
        # Create PlaceInfo object
        place_info = PlaceInfo(
            place_id=place_id,
            name=place_data.get('name', ''),
            rating=place_data.get('rating', 0.0),
            user_ratings_total=place_data.get('user_ratings_total', 0),
            reviews=reviews,
            address=place_data.get('formatted_address', ''),
            phone_number=place_data.get('formatted_phone_number', ''),
            website=place_data.get('website', ''),
            business_status=place_data.get('business_status', ''),
            price_level=place_data.get('price_level'),
            latitude=latitude,
            longitude=longitude
        )
        
        return place_info
    
    def fetch_multiple_places(self, place_ids: List[str], batch_size: int = 10) -> List[PlaceInfo]:
        """
        Fetch data for multiple places with rate limiting
        
        Args:
            place_ids: List of Google Places IDs
            batch_size: Number of places to process before longer delay
            
        Returns:
            List of PlaceInfo objects
        """
        all_places = []
        
        for i, place_id in enumerate(place_ids):
            logger.info(f"Processing place {i+1}/{len(place_ids)}: {place_id}")
            
            place_data = self.get_place_details(place_id)
            
            if place_data:
                place_info = self.process_place_data(place_data, place_id)
                all_places.append(place_info)
                self.places_data.append(place_info)
            
            # Add longer delay every batch_size requests to avoid rate limiting
            if (i + 1) % batch_size == 0:
                logger.info(f"Processed {i+1} places. Taking a short break...")
                time.sleep(2)
        
        return all_places
    
    def export_to_csv(self, filename: str = None) -> str:
        """
        Export places and reviews data to CSV files
        
        Args:
            filename: Base filename (without extension)
            
        Returns:
            Path to the created files
        """
        if filename is None:
            filename = f"google_places_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create directories if they don't exist
        Path("data").mkdir(exist_ok=True)
        
        # Prepare places data
        places_data = []
        reviews_data = []
        
        for place in self.places_data:
            places_data.append({
                'place_id': place.place_id,
                'name': place.name,
                'rating': place.rating,
                'user_ratings_total': place.user_ratings_total,
                'address': place.address,
                'phone_number': place.phone_number,
                'website': place.website,
                'business_status': place.business_status,
                'price_level': place.price_level,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'reviews_count': len(place.reviews)
            })
            
            # Add reviews data
            for review in place.reviews:
                reviews_data.append({
                    'place_id': review.place_id,
                    'place_name': review.place_name,
                    'author_name': review.author_name,
                    'rating': review.rating,
                    'text': review.text,
                    'time': review.time,
                    'relative_time_description': review.relative_time_description,
                    'language': review.language,
                    'review_date': datetime.fromtimestamp(review.time).strftime('%Y-%m-%d %H:%M:%S') if review.time else ''
                })
        
        # Save to CSV
        places_df = pd.DataFrame(places_data)
        reviews_df = pd.DataFrame(reviews_data)
        
        places_file = f"data/{filename}_places.csv"
        reviews_file = f"data/{filename}_reviews.csv"
        
        places_df.to_csv(places_file, index=False, encoding='utf-8')
        reviews_df.to_csv(reviews_file, index=False, encoding='utf-8')
        
        logger.info(f"CSV files saved: {places_file}, {reviews_file}")
        return f"data/{filename}"
    
    def export_to_json(self, filename: str = None) -> str:
        """
        Export data to JSON format
        
        Args:
            filename: Base filename (without extension)
            
        Returns:
            Path to the created file
        """
        if filename is None:
            filename = f"google_places_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create directories if they don't exist
        Path("data").mkdir(exist_ok=True)
        
        # Convert to JSON-serializable format
        json_data = []
        
        for place in self.places_data:
            place_dict = {
                'place_id': place.place_id,
                'name': place.name,
                'rating': place.rating,
                'user_ratings_total': place.user_ratings_total,
                'address': place.address,
                'phone_number': place.phone_number,
                'website': place.website,
                'business_status': place.business_status,
                'price_level': place.price_level,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'reviews': []
            }
            
            for review in place.reviews:
                review_dict = {
                    'author_name': review.author_name,
                    'rating': review.rating,
                    'text': review.text,
                    'time': review.time,
                    'relative_time_description': review.relative_time_description,
                    'language': review.language,
                    'review_date': datetime.fromtimestamp(review.time).strftime('%Y-%m-%d %H:%M:%S') if review.time else ''
                }
                place_dict['reviews'].append(review_dict)
            
            json_data.append(place_dict)
        
        json_file = f"data/{filename}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON file saved: {json_file}")
        return json_file

def load_place_ids_from_json(json_file: str) -> List[str]:
    """
    Load place IDs from your existing JSON file
    
    Args:
        json_file: Path to the JSON file
        
    Returns:
        List of place IDs
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        place_ids = []
        for item in data:
            if 'PLACE ID ' in item and item['PLACE ID ']:
                place_ids.append(item['PLACE ID '].strip())
        
        logger.info(f"Loaded {len(place_ids)} place IDs from {json_file}")
        return place_ids
        
    except Exception as e:
        logger.error(f"Error loading place IDs from {json_file}: {str(e)}")
        return []

if __name__ == "__main__":
    # Example usage with your data
    def example_usage():
        """Example of how to use the API with your data"""
        
        # Your Google Places API key - REPLACE WITH YOUR ACTUAL KEY
        API_KEY = "apikey"
        
        # Load place IDs from your existing JSON file
        place_ids = load_place_ids_from_json("place_razao_table.json")
        
        if not place_ids:
            print("No place IDs found in the JSON file.")
            return
        
        print(f"Found {len(place_ids)} place IDs to process")
        print(f"💰 Estimated cost: ${len(place_ids) * 0.017:.2f}")
        print(f"⏱️  Estimated time: {len(place_ids) * 1.2 / 60:.1f} minutes")
        
        # Confirm before processing all places
        confirm = input(f"\n🤔 Process ALL {len(place_ids)} places? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Processing cancelled. Using first 5 places for testing...")
            place_ids = place_ids[:5]
        
        # Initialize the API
        places_api = GooglePlacesReviewsAPI(API_KEY)
        
        print(f"🚀 Processing {len(place_ids)} places...")
        
        places_data = places_api.fetch_multiple_places(place_ids, batch_size=10)
        
        # Export to CSV and JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        places_api.export_to_csv(f"raizen_places_reviews_{timestamp}")
        places_api.export_to_json(f"raizen_places_reviews_{timestamp}")
        
        print(f"\n✅ Processing completed!")
        print(f"📊 Processed {len(places_data)} places")
        
        total_reviews = sum(len(place.reviews) for place in places_data)
        print(f"📝 Total reviews collected: {total_reviews}")
        
        if places_data:
            avg_rating = sum(place.rating for place in places_data if place.rating > 0) / len([p for p in places_data if p.rating > 0])
            print(f"⭐ Average rating: {avg_rating:.2f}")
        
        for place in places_data:
            print(f"- {place.name}: {place.rating}/5 ({len(place.reviews)} reviews)")
    
    # Run the example
    example_usage()
