"""
Quick start script for Google Places Reviews Extractor
Run this to test the system with a few sample places
"""

from google_places_extractor import GooglePlacesReviewsAPI, load_place_ids_from_json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_test():
    """Quick test with sample places from your data"""
    
    print("🚀 Google Places Reviews Extractor - Quick Test")
    print("=" * 50)
    
    # Get API key from user
    api_key = input("Enter your Google Places API key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Load place IDs from your JSON file
    print("\n📍 Loading place IDs from place_razao_table.json...")
    place_ids = load_place_ids_from_json("place_razao_table.json")
    
    if not place_ids:
        print("❌ No place IDs found in the JSON file!")
        return
    
    print(f"✅ Found {len(place_ids)} place IDs")
    
    # Ask how many to test
    try:
        num_places = int(input(f"\nHow many places to test? (1-{min(10, len(place_ids))}): "))
        if num_places < 1 or num_places > min(10, len(place_ids)):
            num_places = 3
            print(f"Using default: {num_places} places")
    except ValueError:
        num_places = 3
        print(f"Using default: {num_places} places")
    
    # Initialize API
    print(f"\n🔄 Processing {num_places} places...")
    places_api = GooglePlacesReviewsAPI(api_key)
    
    # Process places
    test_place_ids = place_ids[:num_places]
    places_data = places_api.fetch_multiple_places(test_place_ids, batch_size=5)
    
    if not places_data:
        print("❌ No data retrieved. Check your API key and network connection.")
        return
    
    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"quick_test_{timestamp}"
    
    csv_path = places_api.export_to_csv(filename)
    json_path = places_api.export_to_json(filename)
    
    # Display results
    print("\n" + "=" * 50)
    print("🎉 RESULTS SUMMARY")
    print("=" * 50)
    print(f"📊 Places processed: {len(places_data)}")
    
    total_reviews = sum(len(place.reviews) for place in places_data)
    print(f"📝 Total reviews: {total_reviews}")
    
    if places_data:
        valid_ratings = [place.rating for place in places_data if place.rating > 0]
        if valid_ratings:
            avg_rating = sum(valid_ratings) / len(valid_ratings)
            print(f"⭐ Average rating: {avg_rating:.2f}/5")
    
    print(f"\n📁 Files saved:")
    print(f"  • {csv_path}_places.csv")
    print(f"  • {csv_path}_reviews.csv") 
    print(f"  • {json_path}")
    
    print("\n📋 Places Details:")
    for i, place in enumerate(places_data, 1):
        print(f"  {i}. {place.name}")
        print(f"     ⭐ Rating: {place.rating}/5")
        print(f"     📝 Reviews: {len(place.reviews)}")
        print(f"     📍 Address: {place.address[:60]}...")
        print()
    
    print("✅ Quick test completed successfully!")
    print("\n💡 Next steps:")
    print("  1. Review the exported files")
    print("  2. Run the full web application: python web_app.py")
    print("  3. Process all your places through the web interface")

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your API key and internet connection")
