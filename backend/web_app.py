from flask import Flask, render_template, request, jsonify, send_file
from google_places_extractor import GooglePlacesReviewsAPI, load_place_ids_from_json
from datetime import datetime
import logging
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instance
places_api = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/load-place-ids', methods=['GET'])
def load_place_ids():
    """API endpoint to load place IDs from existing JSON file"""
    try:
        place_ids = load_place_ids_from_json("place_razao_table.json")
        return jsonify({
            'success': True,
            'place_ids': place_ids,
            'count': len(place_ids)
        })
    except Exception as e:
        logger.error(f"Error loading place IDs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch-places', methods=['POST'])
def fetch_places():
    """API endpoint to fetch places data"""
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        place_ids = data.get('place_ids', [])
        batch_size = data.get('batch_size', 10)
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        if not place_ids:
            return jsonify({'error': 'No place IDs provided'}), 400
        
        global places_api
        places_api = GooglePlacesReviewsAPI(api_key)
        
        # Process places
        logger.info(f"Starting to process {len(place_ids)} places")
        places_data = places_api.fetch_multiple_places(place_ids, batch_size)
        
        # Export data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"raizen_places_reviews_{timestamp}"
        csv_path = places_api.export_to_csv(base_filename)
        json_path = places_api.export_to_json(base_filename)
        
        # Prepare response
        total_reviews = sum(len(place.reviews) for place in places_data)
        valid_ratings = [place.rating for place in places_data if place.rating > 0]
        avg_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0
        
        summary = {
            'total_places': len(places_data),
            'total_reviews': total_reviews,
            'avg_rating': round(avg_rating, 2),
            'csv_places_file': f"{csv_path}_places.csv",
            'csv_reviews_file': f"{csv_path}_reviews.csv",
            'json_file': json_path
        }
        
        # Get sample data for preview
        sample_places = []
        for place in places_data[:5]:  # First 5 places
            sample_places.append({
                'name': place.name,
                'rating': place.rating,
                'reviews_count': len(place.reviews),
                'address': place.address[:50] + '...' if len(place.address) > 50 else place.address
            })
        
        return jsonify({
            'success': True,
            'summary': summary,
            'sample_places': sample_places
        })
        
    except Exception as e:
        logger.error(f"Error in fetch_places: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """Download exported files"""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {str(e)}")
        return jsonify({'error': str(e)}), 404

if __name__ == "__main__":
    print("🚀 Starting Google Places Reviews Extractor Web App...")
    print("📍 Visit http://localhost:5000 to use the web interface")
    print("📂 Make sure you have your Google Places API key ready")
    app.run(debug=True, host='localhost', port=5000)
