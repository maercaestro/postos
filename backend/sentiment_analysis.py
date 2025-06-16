import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class RaizenSentimentAnalyzer:
    def __init__(self, places_file: str, reviews_file: str):
        """
        Initialize the sentiment analyzer with data files
        
        Args:
            places_file: Path to places CSV file
            reviews_file: Path to reviews CSV file
        """
        self.places_df = pd.read_csv(places_file)
        self.reviews_df = pd.read_csv(reviews_file)
        
        # Filter only places and reviews with actual data
        self.places_with_reviews = self.places_df[self.places_df['reviews_count'] > 0].copy()
        self.reviews_with_text = self.reviews_df[
            (self.reviews_df['text'].notna()) & 
            (self.reviews_df['text'].str.len() > 5)
        ].copy()
        
        print(f"📊 Data Summary:")
        print(f"   • Total places: {len(self.places_df)}")
        print(f"   • Places with reviews: {len(self.places_with_reviews)}")
        print(f"   • Total reviews with text: {len(self.reviews_with_text)}")
        print(f"   • Average rating: {self.places_with_reviews['rating'].mean():.2f}")
    
    def perform_sentiment_analysis(self):
        """
        Perform sentiment analysis on review texts
        """
        print("🔍 Performing sentiment analysis...")
        
        # Calculate sentiment scores using TextBlob
        sentiments = []
        polarities = []
        subjectivities = []
        
        for text in self.reviews_with_text['text']:
            if pd.isna(text) or len(str(text).strip()) < 3:
                sentiments.append('neutral')
                polarities.append(0.0)
                subjectivities.append(0.0)
                continue
                
            try:
                blob = TextBlob(str(text))
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                # Classify sentiment based on polarity
                if polarity > 0.1:
                    sentiment = 'positive'
                elif polarity < -0.1:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                
                sentiments.append(sentiment)
                polarities.append(polarity)
                subjectivities.append(subjectivity)
                
            except Exception as e:
                sentiments.append('neutral')
                polarities.append(0.0)
                subjectivities.append(0.0)
        
        # Add sentiment data to reviews dataframe
        self.reviews_with_text['sentiment'] = sentiments
        self.reviews_with_text['polarity'] = polarities
        self.reviews_with_text['subjectivity'] = subjectivities
        
        # Create sentiment categories based on rating as well
        self.reviews_with_text['rating_sentiment'] = self.reviews_with_text['rating'].apply(
            lambda x: 'positive' if x >= 4 else ('negative' if x <= 2 else 'neutral')
        )
        
        print("✅ Sentiment analysis completed!")
        return self.reviews_with_text
    
    def create_sentiment_dashboard(self):
        """
        Create comprehensive sentiment analysis dashboard
        """
        # Overall sentiment distribution
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Sentiment Distribution (Text Analysis)', 
                'Rating Distribution',
                'Sentiment vs Rating Correlation',
                'Sentiment Trends Over Time'
            ),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # 1. Sentiment distribution pie chart
        sentiment_counts = self.reviews_with_text['sentiment'].value_counts()
        colors = {'positive': '#2E8B57', 'neutral': '#FFD700', 'negative': '#DC143C'}
        
        fig.add_trace(
            go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                marker_colors=[colors[label] for label in sentiment_counts.index],
                name="Sentiment"
            ),
            row=1, col=1
        )
        
        # 2. Rating distribution
        rating_counts = self.reviews_with_text['rating'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(
                x=rating_counts.index,
                y=rating_counts.values,
                marker_color='skyblue',
                name="Ratings"
            ),
            row=1, col=2
        )
        
        # 3. Sentiment vs Rating scatter
        sentiment_numeric = self.reviews_with_text['sentiment'].map({
            'positive': 1, 'neutral': 0, 'negative': -1
        })
        
        fig.add_trace(
            go.Scatter(
                x=self.reviews_with_text['rating'],
                y=sentiment_numeric,
                mode='markers',
                marker=dict(
                    color=self.reviews_with_text['polarity'],
                    colorscale='RdYlGn',
                    size=8,
                    opacity=0.6
                ),
                name="Sentiment vs Rating"
            ),
            row=2, col=1
        )
        
        # 4. Sentiment trends over time (if we have dates)
        if 'review_date' in self.reviews_with_text.columns:
            self.reviews_with_text['review_date'] = pd.to_datetime(self.reviews_with_text['review_date'])
            monthly_sentiment = self.reviews_with_text.groupby([
                self.reviews_with_text['review_date'].dt.to_period('M'),
                'sentiment'
            ]).size().unstack(fill_value=0)
            
            for sentiment in ['positive', 'negative', 'neutral']:
                if sentiment in monthly_sentiment.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=monthly_sentiment.index.astype(str),
                            y=monthly_sentiment[sentiment],
                            mode='lines+markers',
                            name=f"{sentiment.title()} Trends",
                            line=dict(color=colors[sentiment])
                        ),
                        row=2, col=2
                    )
        
        fig.update_layout(
            title_text="🏪 Raizen Gas Stations - Sentiment Analysis Dashboard",
            showlegend=True,
            height=800
        )
        
        fig.write_html("data/sentiment_dashboard.html")
        print("📊 Dashboard saved to data/sentiment_dashboard.html")
        return fig
    
    def analyze_by_station(self, min_reviews=5):
        """
        Analyze sentiment by individual gas station
        
        Args:
            min_reviews: Minimum number of reviews to include a station
        """
        print(f"🏪 Analyzing sentiment by station (min {min_reviews} reviews)...")
        
        # Group by place and calculate sentiment metrics
        station_analysis = []
        
        for place_id in self.reviews_with_text['place_id'].unique():
            place_reviews = self.reviews_with_text[self.reviews_with_text['place_id'] == place_id]
            place_info = self.places_with_reviews[self.places_with_reviews['place_id'] == place_id].iloc[0]
            
            if len(place_reviews) >= min_reviews:
                sentiment_counts = place_reviews['sentiment'].value_counts()
                
                station_analysis.append({
                    'place_id': place_id,
                    'name': place_info['name'],
                    'address': place_info['address'],
                    'latitude': place_info.get('latitude'),
                    'longitude': place_info.get('longitude'),
                    'total_reviews': len(place_reviews),
                    'avg_rating': place_reviews['rating'].mean(),
                    'avg_polarity': place_reviews['polarity'].mean(),
                    'positive_reviews': sentiment_counts.get('positive', 0),
                    'negative_reviews': sentiment_counts.get('negative', 0),
                    'neutral_reviews': sentiment_counts.get('neutral', 0),
                    'positive_ratio': sentiment_counts.get('positive', 0) / len(place_reviews),
                    'negative_ratio': sentiment_counts.get('negative', 0) / len(place_reviews),
                    'sentiment_score': sentiment_counts.get('positive', 0) - sentiment_counts.get('negative', 0)
                })
        
        station_df = pd.DataFrame(station_analysis)
        station_df = station_df.sort_values('sentiment_score', ascending=False)
        
        # Save detailed analysis
        station_df.to_csv('data/station_sentiment_analysis.csv', index=False)
        print(f"💾 Station analysis saved to data/station_sentiment_analysis.csv")
        
        return station_df
    
    def extract_key_topics(self, sentiment_type='negative', top_words=20):
        """
        Extract key topics from reviews by sentiment
        
        Args:
            sentiment_type: 'positive', 'negative', or 'neutral'
            top_words: Number of top words to extract
        """
        print(f"🔍 Extracting key topics from {sentiment_type} reviews...")
        
        # Filter reviews by sentiment
        sentiment_reviews = self.reviews_with_text[
            self.reviews_with_text['sentiment'] == sentiment_type
        ]
        
        if len(sentiment_reviews) == 0:
            print(f"No {sentiment_type} reviews found!")
            return
        
        # Combine all review texts
        all_text = ' '.join(sentiment_reviews['text'].astype(str))
        
        # Clean and process text (basic cleaning for Portuguese/English)
        text_clean = re.sub(r'[^\w\s]', ' ', all_text.lower())
        words = text_clean.split()
        
        # Remove common stop words (basic list)
        stop_words = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas',
            'para', 'por', 'com', 'sem', 'sobre', 'até', 'após', 'antes', 'durante', 'entre', 'contra',
            'e', 'ou', 'mas', 'porém', 'contudo', 'todavia', 'entretanto',
            'que', 'se', 'quando', 'onde', 'como', 'porque', 'qual', 'quem', 'quanto',
            'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
            'meu', 'minha', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'seu', 'sua', 'seus', 'suas',
            'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela', 'aqueles', 'aquelas',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were',
            'posto', 'shell', 'gas', 'station', 'gasolina', 'combustível', 'top'
        }
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        top_words_list = word_freq.most_common(top_words)
        
        # Create word cloud
        if len(filtered_words) > 0:
            wordcloud_text = ' '.join(filtered_words)
            wordcloud = WordCloud(
                width=800, height=400, 
                background_color='white',
                colormap='RdYlGn' if sentiment_type == 'positive' else 'Reds'
            ).generate(wordcloud_text)
            
            plt.figure(figsize=(12, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Key Topics in {sentiment_type.title()} Reviews', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig(f'data/wordcloud_{sentiment_type}.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        print(f"📝 Top {top_words} words in {sentiment_type} reviews:")
        for word, count in top_words_list:
            print(f"   • {word}: {count}")
        
        return top_words_list
    
    def create_map_visualization(self, station_df):
        """
        Create an interactive map showing stations colored by sentiment
        """
        print("🗺️ Creating sentiment map visualization...")
        
        # Filter stations with coordinates
        stations_with_coords = station_df[
            (station_df['latitude'].notna()) & 
            (station_df['longitude'].notna())
        ].copy()
        
        if len(stations_with_coords) == 0:
            print("❌ No stations with coordinates found for mapping!")
            return None
        
        # Create color scale based on sentiment score
        fig = px.scatter_mapbox(
            stations_with_coords,
            lat="latitude",
            lon="longitude",
            color="sentiment_score",
            size="total_reviews",
            hover_data={
                'name': True,
                'avg_rating': ':.2f',
                'positive_ratio': ':.2%',
                'negative_ratio': ':.2%',
                'total_reviews': True
            },
            color_continuous_scale="RdYlGn",
            size_max=20,
            zoom=5,
            title="🏪 Raizen Gas Stations - Sentiment Analysis Map"
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            height=600,
            title_x=0.5
        )
        
        fig.write_html("data/sentiment_map.html")
        print("🗺️ Map saved to data/sentiment_map.html")
        return fig
    
    def generate_summary_report(self, station_df):
        """
        Generate a comprehensive summary report
        """
        print("📋 Generating summary report...")
        
        # Calculate overall statistics
        total_reviews = len(self.reviews_with_text)
        avg_rating = self.reviews_with_text['rating'].mean()
        avg_polarity = self.reviews_with_text['polarity'].mean()
        
        sentiment_dist = self.reviews_with_text['sentiment'].value_counts(normalize=True)
        
        # Best and worst performing stations
        best_stations = station_df.head(5)
        worst_stations = station_df.tail(5)
        
        report = f"""
# 🏪 Raizen Gas Stations - Sentiment Analysis Report
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Overall Statistics
- **Total Reviews Analyzed**: {total_reviews:,}
- **Average Rating**: {avg_rating:.2f}/5.0
- **Average Sentiment Polarity**: {avg_polarity:.3f} (-1 = very negative, +1 = very positive)

## 🎭 Sentiment Distribution
- **Positive Reviews**: {sentiment_dist.get('positive', 0):.1%}
- **Neutral Reviews**: {sentiment_dist.get('neutral', 0):.1%}
- **Negative Reviews**: {sentiment_dist.get('negative', 0):.1%}

## 🏆 Top 5 Best Performing Stations (by sentiment score)
"""
        
        for i, station in best_stations.iterrows():
            report += f"""
### {station['name']}
- **Location**: {station['address']}
- **Reviews**: {station['total_reviews']} | **Avg Rating**: {station['avg_rating']:.2f}
- **Positive**: {station['positive_ratio']:.1%} | **Negative**: {station['negative_ratio']:.1%}
- **Sentiment Score**: {station['sentiment_score']}
"""
        
        report += "\n## ⚠️ Bottom 5 Stations (need attention)\n"
        
        for i, station in worst_stations.iterrows():
            report += f"""
### {station['name']}
- **Location**: {station['address']}
- **Reviews**: {station['total_reviews']} | **Avg Rating**: {station['avg_rating']:.2f}
- **Positive**: {station['positive_ratio']:.1%} | **Negative**: {station['negative_ratio']:.1%}
- **Sentiment Score**: {station['sentiment_score']}
"""
        
        # Save report
        with open('data/sentiment_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("📋 Report saved to data/sentiment_analysis_report.md")
        return report

def main():
    """
    Main function to run the complete sentiment analysis
    """
    print("🚀 Starting Raizen Gas Stations Sentiment Analysis...")
    
    # Initialize analyzer with your latest data
    analyzer = RaizenSentimentAnalyzer(
        places_file='data/raizen_places_reviews_20250609_150209_places.csv',
        reviews_file='data/raizen_places_reviews_20250609_150209_reviews.csv'
    )
    
    # Perform sentiment analysis
    reviews_with_sentiment = analyzer.perform_sentiment_analysis()
    
    # Create dashboard
    dashboard_fig = analyzer.create_sentiment_dashboard()
    
    # Analyze by station
    station_analysis = analyzer.analyze_by_station(min_reviews=3)
    
    # Extract key topics for positive and negative reviews
    print("\n" + "="*50)
    analyzer.extract_key_topics('positive', top_words=15)
    
    print("\n" + "="*50)
    analyzer.extract_key_topics('negative', top_words=15)
    
    # Create map visualization
    map_fig = analyzer.create_map_visualization(station_analysis)
    
    # Generate summary report
    report = analyzer.generate_summary_report(station_analysis)
    
    print("\n🎉 Sentiment Analysis Complete!")
    print("📁 Generated Files:")
    print("   • data/sentiment_dashboard.html - Interactive dashboard")
    print("   • data/sentiment_map.html - Interactive map")
    print("   • data/station_sentiment_analysis.csv - Detailed station analysis")
    print("   • data/sentiment_analysis_report.md - Summary report")
    print("   • data/wordcloud_positive.png - Positive reviews word cloud")
    print("   • data/wordcloud_negative.png - Negative reviews word cloud")

if __name__ == "__main__":
    main()
