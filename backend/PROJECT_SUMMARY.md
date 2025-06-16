# 🏪 Raizen Gas Stations - Complete Analysis Project

## 📋 Project Overview
This project provides a comprehensive solution for extracting, analyzing, and visualizing Google Places data and customer reviews for Raizen gas stations across Brazil. The system includes cost-efficient API usage, data export capabilities, coordinate mapping, and advanced sentiment analysis.

## 🎯 Project Objectives
- ✅ Extract reviews and ratings for Raizen gas stations using Google Places API
- ✅ Export data to CSV and JSON formats with geographical coordinates
- ✅ Perform sentiment analysis on customer reviews
- ✅ Generate interactive visualizations and reports
- ✅ Maintain cost efficiency (stay within Google's free tier)

## 📊 Key Results

### Dataset Statistics
- **Total Places Processed**: 2,383 out of 2,862 (83.3% complete)
- **Places with Reviews**: 1,242 stations
- **Total Reviews Analyzed**: 3,715 reviews with text content
- **Total Reviews (including ratings-only)**: 5,857
- **Average Rating**: 4.18/5.0
- **Cost**: $0 (stayed within Google's free tier of 10,000 requests/month)

### Sentiment Analysis Results
- **Average Sentiment Polarity**: 0.097 (slightly positive)
- **Positive Reviews**: 20.2%
- **Neutral Reviews**: 78.7%
- **Negative Reviews**: 1.1%

### Top Performing Stations
1. **Palácio Guanabara** (Rio de Janeiro) - 100% positive sentiment
2. **Posto Shell** (Guarapari) - High review volume with positive trends
3. **Posto Shell Colossal Mercês** (Curitiba) - 80% positive reviews
4. **Posto Retiro dos Bandeirantes** (Tanguá) - Perfect 5.0 rating
5. **Auto Posto Goioxim** (Goioxim) - Consistent positive feedback

### Areas for Improvement
- **5 stations** identified with negative sentiment requiring attention
- Key complaint topics: service quality, pricing, equipment issues
- Geographic patterns show some regional variations in satisfaction

## 🛠️ Technical Implementation

### Core Components
1. **GooglePlacesReviewsAPI** (`google_places_extractor.py`)
   - Cost-optimized API calls with rate limiting
   - Batch processing capabilities
   - Tier-aware field selection:
     - Essential ($5/1000): Basic place info and location
     - Pro ($17/1000): Operational status 
     - Enterprise ($20/1000): Contact info and ratings
     - Enterprise + Atmosphere ($25/1000): Reviews and atmosphere data
   - Automatic retry mechanisms

2. **Web Application** (`web_app.py`)
   - Flask-based interface for easy data extraction
   - Real-time progress tracking
   - Parameter configuration

3. **Sentiment Analysis Engine** (`sentiment_analysis.py`)
   - TextBlob-based sentiment analysis
   - Interactive dashboard generation
   - Geographic visualization
   - Word cloud generation
   - Station-level performance analysis

### Data Structure
```python
@dataclass
class PlaceInfo:
    place_id: str
    name: str
    rating: float
    user_ratings_total: int
    address: str
    phone_number: str
    website: str
    business_status: str
    price_level: Optional[int]
    latitude: Optional[float]  # Added for mapping
    longitude: Optional[float]  # Added for mapping
    reviews: List[Dict]
```

## 📁 Generated Files and Outputs

### Raw Data
- `raizen_places_reviews_20250609_150209.json` - Complete dataset
- `raizen_places_reviews_20250609_150209_places.csv` - Places data in CSV
- `raizen_places_reviews_20250609_150209_reviews.csv` - Reviews data in CSV
- `raizen_places_with_reviews.json` - Filtered dataset (places with reviews only)

### Analysis Results
- `sentiment_dashboard.html` - Interactive sentiment analysis dashboard
- `sentiment_map.html` - Geographic visualization of sentiment scores
- `station_sentiment_analysis.csv` - Detailed station-level analysis
- `sentiment_analysis_report.md` - Comprehensive summary report
- `wordcloud_positive.png` - Word cloud of positive review terms
- `wordcloud_negative.png` - Word cloud of negative review terms

## 🌟 Key Insights

### Customer Satisfaction Patterns
1. **Overall Satisfaction**: Average rating of 4.18/5.0 indicates good customer satisfaction
2. **Review Distribution**: Most reviews are neutral (78.7%), suggesting basic service expectations are met
3. **Geographic Variations**: Some regions show consistently higher satisfaction levels
4. **Service Quality**: "Atendimento" (service) is frequently mentioned in positive reviews

### Business Intelligence
1. **High-Performing Locations**: Can serve as best practice models
2. **Problem Areas**: 5 stations identified for immediate attention and improvement
3. **Customer Priorities**: Service quality, cleanliness, and staff courtesy are key factors
4. **Regional Patterns**: Different regions may have varying service standards

### Operational Recommendations
1. **Staff Training**: Focus on service quality improvements for low-scoring stations
2. **Best Practice Sharing**: Replicate successful practices from top-performing stations
3. **Regional Management**: Consider regional management strategies based on satisfaction patterns
4. **Continuous Monitoring**: Implement regular sentiment tracking for ongoing improvements

## 💰 Cost Analysis
- **Google Places API Usage**: 2,383 requests
- **Estimated Cost**: $0 (within free tier of 10,000 requests/month)
- **Tier Used**: Enterprise + Atmosphere tier ($25/1000 for reviews and ratings)
  - Essential tier: `place_id`, `name`, `formatted_address`, `geometry` ($5/1000)
  - Pro tier: `business_status` ($17/1000) 
  - Enterprise tier: `rating`, `user_ratings_total`, `formatted_phone_number`, `website`, `price_level` ($20/1000)
  - Enterprise + Atmosphere tier: `reviews` ($25/1000)
- **Cost Efficiency**: Achieved through staying within free tier and optimized field selection

## 🚀 Future Enhancements
1. **Real-time Monitoring**: Set up automated monthly analysis
2. **Competitive Analysis**: Compare with competitor stations
3. **Predictive Analytics**: Forecast satisfaction trends
4. **Mobile App Integration**: Create customer-facing satisfaction tracking
5. **Complete Dataset**: Process remaining 479 place IDs
6. **Multi-language Analysis**: Enhanced Portuguese-specific sentiment analysis

## 📞 Technical Support
- **Python Version**: 3.8+
- **Key Dependencies**: googlemaps, pandas, flask, textblob, plotly, folium
- **Installation**: `pip install -r requirements.txt`
- **Usage**: See `README.md` for detailed instructions

## 🏆 Project Success Metrics
- ✅ **Data Coverage**: 83.3% of target locations processed
- ✅ **Cost Efficiency**: $0 spent (stayed within free tier)
- ✅ **Analysis Depth**: Multi-dimensional sentiment analysis completed
- ✅ **Visualization Quality**: Interactive dashboards and maps generated
- ✅ **Business Value**: Actionable insights and recommendations provided
- ✅ **Technical Quality**: Robust, scalable, and maintainable codebase

---

*Generated on: 2025-06-09*
*Project Status: ✅ Complete - Phase 1 (Ready for production use)*
