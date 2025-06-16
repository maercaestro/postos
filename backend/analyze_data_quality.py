#!/usr/bin/env python3
"""
Data Quality Analysis Script for Raizen Gas Station Reviews
Analyzes extracted Google Places data to determine coverage and quality metrics.
"""

import json
import os
from collections import defaultdict
from datetime import datetime

def analyze_json_files(data_dir="/Users/abuhuzaifahbidin/Documents/GitHub/postos/data"):
    """Analyze all JSON files in the data directory."""
    
    # Find all JSON files with reviews data
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json') and 'reviews' in f]
    
    if not json_files:
        print("No review JSON files found in data directory")
        return
    
    print(f"Found {len(json_files)} JSON files to analyze:")
    for file in json_files:
        print(f"  - {file}")
    print()
    
    # Combined statistics across all files
    total_places = 0
    places_with_reviews = 0
    places_with_rating = 0
    total_reviews = 0
    rating_distribution = defaultdict(int)
    review_count_distribution = defaultdict(int)
    business_status_counts = defaultdict(int)
    
    # Analyze each file
    for json_file in json_files:
        file_path = os.path.join(data_dir, json_file)
        print(f"Analyzing {json_file}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_places = len(data)
            file_with_reviews = sum(1 for place in data if place.get('reviews'))
            file_with_rating = sum(1 for place in data if place.get('rating', 0) > 0)
            file_total_reviews = sum(len(place.get('reviews', [])) for place in data)
            
            print(f"  Places: {file_places}")
            print(f"  With reviews: {file_with_reviews} ({file_with_reviews/file_places*100:.1f}%)")
            print(f"  With ratings: {file_with_rating} ({file_with_rating/file_places*100:.1f}%)")
            print(f"  Total reviews: {file_total_reviews}")
            print()
            
            # Update totals
            total_places += file_places
            places_with_reviews += file_with_reviews
            places_with_rating += file_with_rating
            total_reviews += file_total_reviews
            
            # Collect detailed statistics
            for place in data:
                # Rating distribution
                rating = place.get('rating', 0)
                if rating > 0:
                    rating_bucket = int(rating)
                    rating_distribution[rating_bucket] += 1
                
                # Review count distribution
                review_count = len(place.get('reviews', []))
                if review_count == 0:
                    review_count_distribution['0'] += 1
                elif review_count <= 5:
                    review_count_distribution['1-5'] += 1
                elif review_count <= 10:
                    review_count_distribution['6-10'] += 1
                elif review_count <= 20:
                    review_count_distribution['11-20'] += 1
                else:
                    review_count_distribution['20+'] += 1
                
                # Business status
                status = place.get('business_status', 'Unknown')
                business_status_counts[status] += 1
                
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
            continue
    
    # Print combined statistics
    print("=" * 60)
    print("COMBINED STATISTICS ACROSS ALL FILES")
    print("=" * 60)
    print(f"Total places analyzed: {total_places}")
    print(f"Places with reviews: {places_with_reviews} ({places_with_reviews/total_places*100:.1f}%)")
    print(f"Places with ratings: {places_with_rating} ({places_with_rating/total_places*100:.1f}%)")
    print(f"Total reviews collected: {total_reviews}")
    print(f"Average reviews per place: {total_reviews/total_places:.2f}")
    print(f"Average reviews per place with reviews: {total_reviews/places_with_reviews:.2f}" if places_with_reviews > 0 else "N/A")
    print()
    
    # Rating distribution
    print("RATING DISTRIBUTION:")
    for rating in sorted(rating_distribution.keys()):
        count = rating_distribution[rating]
        percentage = count / places_with_rating * 100 if places_with_rating > 0 else 0
        print(f"  {rating}.0-{rating}.9 stars: {count} places ({percentage:.1f}%)")
    print()
    
    # Review count distribution
    print("REVIEW COUNT DISTRIBUTION:")
    order = ['0', '1-5', '6-10', '11-20', '20+']
    for bucket in order:
        count = review_count_distribution[bucket]
        percentage = count / total_places * 100
        print(f"  {bucket} reviews: {count} places ({percentage:.1f}%)")
    print()
    
    # Business status
    print("BUSINESS STATUS:")
    for status, count in sorted(business_status_counts.items()):
        percentage = count / total_places * 100
        print(f"  {status}: {count} places ({percentage:.1f}%)")
    print()
    
    # Data quality assessment
    print("DATA QUALITY ASSESSMENT:")
    print("-" * 30)
    if places_with_reviews / total_places > 0.3:
        print("✅ GOOD: High percentage of places have reviews")
    elif places_with_reviews / total_places > 0.15:
        print("⚠️  MODERATE: Reasonable percentage of places have reviews")
    else:
        print("❌ LOW: Low percentage of places have reviews")
    
    if total_reviews / total_places > 5:
        print("✅ GOOD: High average reviews per place")
    elif total_reviews / total_places > 2:
        print("⚠️  MODERATE: Reasonable average reviews per place")
    else:
        print("❌ LOW: Low average reviews per place")
    
    operational_rate = business_status_counts.get('OPERATIONAL', 0) / total_places
    if operational_rate > 0.8:
        print("✅ GOOD: Most places are operational")
    elif operational_rate > 0.6:
        print("⚠️  MODERATE: Some places may be closed")
    else:
        print("❌ LOW: Many places appear to be closed")
    
    print()
    print("RECOMMENDATIONS:")
    print("-" * 15)
    
    if places_with_reviews / total_places > 0.2:
        print("• Data quality is sufficient for analysis")
        print("• Consider processing all remaining place IDs")
    else:
        print("• Data quality is limited - many places lack reviews")
        print("• Focus on places with higher review counts")
    
    if total_reviews > 1000:
        print("• Sufficient data for sentiment analysis")
        print("• Consider implementing review categorization")
    
    print(f"• Estimated API cost for full dataset: ~${total_places * 0.017:.2f}")

if __name__ == "__main__":
    analyze_json_files()
