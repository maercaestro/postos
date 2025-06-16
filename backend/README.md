# Google Places Reviews Extractor

A cost-efficient Python application to extract reviews and ratings from Google Places API for Raizen gas stations.

## 🚀 Features

- **Cost-Optimized API Calls**: Only requests necessary fields to minimize costs
- **Rate Limiting**: Respects Google's API limits with intelligent delays
- **Batch Processing**: Processes multiple places efficiently
- **Multiple Export Formats**: CSV and JSON outputs
- **Web Interface**: User-friendly web application
- **Error Handling**: Robust error handling and logging
- **Progress Tracking**: Real-time processing updates

## 📋 Prerequisites

1. **Google Places API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Places API
   - Create an API key
   - Restrict it to Places API for security

2. **Python 3.7+**

## 🛠️ Installation

1. **Clone or download the files to your project directory**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Option 1: Web Application (Recommended)

1. **Start the web application:**
   ```bash
   python web_app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Follow the web interface:**
   - Step 1: Load place IDs from your existing `place_razao_table.json` file
   - Step 2: Enter your Google Places API key
   - Step 3: Configure batch size and start extraction

### Option 2: Direct Python Script

1. **Edit the API key in `google_places_extractor.py`:**
   ```python
   API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
   ```

2. **Run the script:**
   ```bash
   python google_places_extractor.py
   ```

## 📁 Output Files

The application creates a `data` folder with:

- **`*_places.csv`**: Overview of each place (ratings, address, phone, etc.)
- **`*_reviews.csv`**: Individual reviews with details
- **`*.json`**: Complete structured data

## 💰 Cost Optimization Features

1. **Selective Field Retrieval**: Only requests necessary data fields
2. **Rate Limiting**: Built-in delays to prevent hitting API limits
3. **Batch Processing**: Efficient processing with configurable batch sizes
4. **Error Recovery**: Continues processing even if individual places fail

## 🔧 Configuration

### Batch Sizes
- **5**: Conservative (safest for rate limits)
- **10**: Recommended (good balance)
- **15**: Aggressive (faster but higher risk)
- **20**: Fast (use only with high quotas)

### API Fields Retrieved
The application only requests these essential fields to minimize costs:
- place_id, name, rating, user_ratings_total
- reviews, formatted_address, formatted_phone_number
- website, business_status, price_level

## 📊 Sample Output Structure

### Places CSV
```csv
place_id,name,rating,user_ratings_total,address,phone_number,website,business_status,reviews_count
ChIJ...,Posto Shell Centro,4.2,150,"Rua Principal, 123","+55 11 1234-5678,https://shell.com,OPERATIONAL,5
```

### Reviews CSV
```csv
place_id,place_name,author_name,rating,text,review_date,language
ChIJ...,Posto Shell Centro,João Silva,5,"Excelente atendimento!",2023-06-15 14:30:00,pt
```

## 🚨 Important Notes

### API Costs
- Google Places API charges per request
- Each place requires 1 API call
- Current pricing: ~$0.017 per place details request
- For 100 places = ~$1.70

### Rate Limits
- Default: 100 requests per 100 seconds
- The application includes delays to respect these limits
- Monitor your usage in Google Cloud Console

### Best Practices
1. Start with small batches to test
2. Monitor your API usage and costs
3. Use the web interface for better control
4. Keep your API key secure

## 🔍 Troubleshooting

### Common Issues

1. **"API key not valid"**
   - Verify your API key is correct
   - Ensure Places API is enabled
   - Check API key restrictions

2. **"Quota exceeded"**
   - Reduce batch size
   - Wait and try again later
   - Check your Google Cloud billing

3. **"No place IDs found"**
   - Ensure `place_razao_table.json` exists
   - Check file format and content

## 📞 Support

For issues or questions:
1. Check the console logs for detailed error messages
2. Verify your Google Cloud Console for API status
3. Ensure all required files are in place

## 🎨 Web Interface Preview

The web application provides:
- **Modern, responsive design**
- **Real-time progress tracking**
- **Automatic file loading**
- **Download links for all exports**
- **Sample data preview**
- **Error handling with user-friendly messages**

Start with the web interface for the best user experience!
