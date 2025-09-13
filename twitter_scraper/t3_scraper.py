import requests
from bs4 import BeautifulSoup
import re
import os
import math
from dotenv import load_dotenv
from supabase import create_client, Client
from textblob import TextBlob

# --- Step 1: Load Environment Variables ---
# This line loads the variables from your .env file
load_dotenv()
print("Attempting to load environment variables from .env file...")

# --- Step 2: Supabase Configuration ---
# Get credentials from the loaded environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Safety Check: Ensure that the variables were loaded correctly
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("FATAL: Supabase URL and Key must be set in your .env file. Please check the file.")
else:
    print("Environment variables loaded successfully.")

# Initialize the Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully.")
except Exception as e:
    raise RuntimeError(f"FATAL: Could not initialize Supabase client. Error: {e}")


def is_indian_text(text):
    """Checks if the text is likely related to India."""
    devanagari_pattern = re.compile(r'[\u0900-\u097F]')
    indian_terms = ['india', 'bharat', 'hindu', 'delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata']
    
    if devanagari_pattern.search(text):
        return True
    
    text_lower = text.lower()
    if any(term in text_lower for term in indian_terms):
        return True
    
    return False

def generate_twitter_search_link(topic):
    """Generate a Twitter search link for the given topic."""
    return f"https://twitter.com/search?q={topic.replace('#', '%23')}"

def generate_instagram_search_link(topic):
    """Generate an Instagram search link for the given topic."""
    return f"https://www.instagram.com/explore/tags/{topic.replace('#', '')}"

def get_trending_topics():
    """Scrapes trending topics from trends24.in for India."""
    urls_to_try = [
        "https://trends24.in/india/",
        "http://trends24.in/india/",
        "https://www.trends24.in/india/"
    ]
    
    for url in urls_to_try:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            
            print(f"\nTrying to fetch data from {url}...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            print("Successfully connected! Parsing HTML content...")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            trend_links = soup.find_all('a', class_='trend-link')
            
            if not trend_links:
                print("No trend links found. Trying next URL...")
                continue
            
            trending_topics = []
            seen_topics = set()  
            
            print(f"Found {len(trend_links)} potential trends. Filtering for unique Indian topics...")
            for link in trend_links:
                trend_text = link.get_text().strip()
                
                if trend_text in seen_topics:
                    continue
                
                if trend_text.startswith('#') and (is_indian_text(trend_text) or len(trending_topics) < 5):
                    tweet_count = "N/A"
                    
                    # Generate Twitter search link only
                    twitter_link = generate_twitter_search_link(trend_text)
                    
                    parent_li = link.find_parent('li')
                    if parent_li:
                        count_span = parent_li.find('span', class_='tweet-count')
                        if count_span and count_span.get_text().strip():
                            tweet_count = count_span.get_text().strip()
                    
                    trending_topics.append({
                        "topic": trend_text,
                        "count": tweet_count,
                        "twitter_link": twitter_link
                    })
                    seen_topics.add(trend_text) 
                    print(f"  -> Added: {trend_text} (Count: {tweet_count})")
                    print(f"     Twitter: {twitter_link}")
                    
                    if len(trending_topics) >= 9:
                        break
            
            return trending_topics
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trends: {str(e)}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred during scraping: {str(e)}")
            continue
    
    print("All URLs failed. Returning empty list.")
    return []

def get_hashtag_post_content(hashtag, link=None):
    """Get sample post content for a hashtag."""
    try:
        # For now, generate sample content based on hashtag
        # In future, this could scrape actual posts from the link
        
        hashtag_clean = hashtag.replace('#', '')
        
        # Generate contextual sample content based on hashtag
        sample_contents = {
            'election': f"Breaking: Major developments in {hashtag_clean}. Citizens actively participating in democratic process.",
            'flood': f"Emergency update on {hashtag_clean}. Relief operations underway, stay safe and follow official guidelines.",
            'dharma': f"Spiritual discourse on {hashtag_clean}. Ancient wisdom for modern times.",
            'football': f"Exciting match updates for {hashtag_clean}. Team performance analysis and fan reactions.",
            'bollywood': f"Latest entertainment news about {hashtag_clean}. Celebrity updates and movie reviews.",
            'batra': f"Tribute to heroes in {hashtag_clean}. Remembering courage and sacrifice for the nation.",
            'default': f"Trending discussion about {hashtag_clean}. Join the conversation and share your thoughts."
        }
        
        # Match hashtag to appropriate content type
        hashtag_lower = hashtag_clean.lower()
        for key, content in sample_contents.items():
            if key in hashtag_lower:
                return content
        
        return sample_contents['default']
        
    except Exception as e:
        print(f"Error generating content for {hashtag}: {e}")
        return f"Trending topic: {hashtag}. Join the discussion."

def analyze_hashtag_sentiment(hashtag):
    """Analyze the sentiment of a hashtag using TextBlob."""
    try:
        # Clean the hashtag for better sentiment analysis
        clean_text = hashtag.replace('#', '').replace('_', ' ')
        
        # Create TextBlob object
        blob = TextBlob(clean_text)
        polarity = blob.sentiment.polarity
        
        print(f"DEBUG: Sentiment for '{hashtag}' -> polarity: {polarity}")
        
        # More sensitive sentiment thresholds
        if polarity > 0.05:
            sentiment = "Positive"
        elif polarity < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        print(f"DEBUG: Final sentiment: {sentiment}")
        return sentiment
        
    except Exception as e:
        print(f"ERROR analyzing sentiment for {hashtag}: {e}")
        return "Neutral"

def calculate_engagement_score(topic_data):
    """Calculate engagement score for a trending topic (1-10 scale)."""
    try:
        topic = topic_data.get("topic", "")
        count_str = topic_data.get("count", "N/A")
        
        # Base score starts at 1
        engagement_score = 1.0
        
        # Parse tweet count if available
        if count_str != "N/A" and count_str:
            try:
                # Extract numeric value from count (e.g., "22K" -> 22000)
                count_clean = count_str.replace('K', '000').replace('M', '000000').replace(',', '')
                count_clean = ''.join(filter(str.isdigit, count_clean))
                if count_clean:
                    tweet_count = int(count_clean)
                    # Logarithmic scaling for tweet count (1-6 points)
                    if tweet_count > 0:
                        engagement_score += min(5, max(0, (tweet_count / 10000) * 2))
            except:
                pass
        
        # Topic characteristics bonus (up to 4 points)
        topic_lower = topic.lower()
        
        # Trending keywords bonus
        trending_keywords = ['election', 'breaking', 'urgent', 'live', 'update', 'news']
        if any(keyword in topic_lower for keyword in trending_keywords):
            engagement_score += 1.5
        
        # Indian relevance bonus
        indian_keywords = ['india', 'indian', 'bharath', 'delhi', 'mumbai', 'modi', 'bjp', 'congress']
        if any(keyword in topic_lower for keyword in indian_keywords):
            engagement_score += 1.0
        
        # Hashtag length factor
        if len(topic) > 15:
            engagement_score += 0.5
        
        # Special characters or numbers
        if any(char in topic for char in ['2024', '2023', '!', '@']):
            engagement_score += 0.5
        
        # Cap the score at 10 and ensure minimum of 1
        engagement_score = max(1, min(10, round(engagement_score)))
        return int(engagement_score)
        
    except Exception as e:
        print(f"Error calculating engagement score: {e}")
        return 1

def format_engagement_display(score):
    """Format engagement score for terminal display with color coding."""
    if score >= 8:
        return f"🔥 {score} (Very High)"
    elif score >= 6:
        return f"⚡ {score} (High)"
    elif score >= 4:
        return f"📈 {score} (Medium)"
    elif score >= 2:
        return f"📊 {score} (Low)"
    else:
        return f"📉 {score} (Very Low)"

def clear_all_supabase_data():
    """Completely clear all existing data from Twitter trending_Hashtags table."""
    try:
        print("🗑️  CLEARING ALL EXISTING DATA from Twitter trending_Hashtags table...")
        
        # Delete all records from Twitter trending_Hashtags table
        result = supabase.table('Twitter trending_Hashtags').delete().gte('id', 0).execute()
        
        print("✅ ALL PREVIOUS DATA CLEARED from Twitter trending_Hashtags table.")
        
        print("\n⚠️  IMPORTANT: To reset ID numbers to start from 1:")
        print("   1. Go to your Supabase Dashboard")
        print("   2. Click on 'SQL Editor'")
        print("   3. Run this command:")
        print("      ALTER SEQUENCE \"Twitter trending_Hashtags_id_seq\" RESTART WITH 1;")
        print("   4. Then run your scraper again")
        print("\n   OR continue without resetting - your data will still be fresh!")
        
        print("📊 Ready to insert fresh data.")
        
    except Exception as e:
        print(f"❌ ERROR clearing data: {e}")

def insert_fresh_data_only(topics_list):
    """Insert only fresh trending topics data after clearing all existing data."""
    if not topics_list:
        print("No topics to store in Supabase.")
        return
    
    # Step 1: Clear all existing data first
    clear_all_supabase_data()
    
    try:
        # Step 2: Process and insert only fresh data
        processed_topics = []
        print(f"\n📥 PROCESSING {len(topics_list)} FRESH TOPICS:")
        
        for i, topic in enumerate(topics_list):
            print(f"  {i+1}. Processing: {topic['topic']}")
            
            # Calculate fresh engagement score
            engagement_score = calculate_engagement_score(topic)
            
            # Calculate fresh sentiment
            sentiment = analyze_hashtag_sentiment(topic["topic"])
            
            # Get twitter link
            twitter_link = topic.get("twitter_link", generate_twitter_search_link(topic["topic"]))
            
            # Get post content
            post_content = get_hashtag_post_content(topic["topic"])
            
            processed_topic = {
                "topic": topic["topic"],
                "count": topic["count"],
                "engagement_score": int(engagement_score),
                "sentiment": str(sentiment),
                "twitter_link": str(twitter_link),
                "post_content": str(post_content)
            }
            
            processed_topics.append(processed_topic)
            print(f"     ✓ Engagement: {engagement_score} - Sentiment: {sentiment}")
            print(f"     ✓ Post Content: {post_content[:60]}...")
            print(f"     ✓ Data to store: {processed_topic}")
        
        # Step 3: Insert fresh data
        print(f"\n💾 INSERTING {len(processed_topics)} FRESH RECORDS...")
        data, count = supabase.table('Twitter trending_Hashtags').insert(processed_topics).execute()
        
        if data and len(data[1]) > 0:
            print(f"🎉 SUCCESS: {len(data[1])} fresh records inserted!")
            print("📋 Your Supabase now contains ONLY current trending topics.")
        else:
            print("⚠️  WARNING: Data insertion may have failed.")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def store_topics_in_supabase(topics_list):
    """Inserts a list of topic dictionaries into the Supabase table."""
    if not topics_list:
        print("No topics to store in Supabase.")
        return
        
    print(f"\nAttempting to store {len(topics_list)} topics in Supabase...")
    
    # Create payload with all available columns
    supabase_topics = []
    for topic in topics_list:
        sentiment = analyze_hashtag_sentiment(topic["topic"])
        post_content = get_hashtag_post_content(topic["topic"])
        supabase_topic = {
            "topic": topic["topic"],
            "count": topic["count"],
            "engagement_score": topic.get("engagement_score", 0),
            "sentiment": sentiment,
            "twitter_link": topic.get("twitter_link", ""),
            "post_content": post_content
        }
        supabase_topics.append(supabase_topic)
    
    print("Data payload being sent:", supabase_topics)

    try:
        # Store all data including engagement_score, sentiment, and twitter_link
        data, count = supabase.table('Twitter trending_Hashtags').insert(supabase_topics).execute()
        
        if data and len(data[1]) > 0:
            print(f"SUCCESS: Successfully inserted {len(data[1])} records into Supabase.")
            print("All data including engagement scores, sentiment, and Twitter links stored successfully.")
        else:
            print("WARNING: Data insertion may have failed. The API did not return any inserted data.")
            print("Please check your Supabase dashboard's 'Twitter trending_Hashtags' table and RLS policies.")

    except Exception as e:
        print(f"ERROR: An error occurred while inserting data into Supabase: {e}")
        print("Continuing with terminal display only...")

def test_engagement_scores():
    """Test function to demonstrate engagement score calculation with mock data."""
    print("\n--- Testing Engagement Score Functionality ---")
    
    # Mock trending topics data similar to what we'd get from trends24.in
    mock_topics = [
        {"topic": "#Nepal", "count": "N/A"},
        {"topic": "#SocialMediaBan", "count": "N/A"},
        {"topic": "#TheBadsOfBollywood", "count": "N/A"},
        {"topic": "#ISupportAryanMaan", "count": "25K"},
        {"topic": "#OnePlusNordBuds3r", "count": "14K"},
        {"topic": "#BharatRatna", "count": "N/A"},
        {"topic": "#IndiaKaGame", "count": "N/A"},
        {"topic": "#BharatJodoYatra", "count": "N/A"},
        {"topic": "#BreakingNews", "count": "50K"},
        {"topic": "#LiveUpdate", "count": "2.1M"}
    ]
    
    print(f"Calculating engagement scores for {len(mock_topics)} trending topics:\n")
    
    for topic in mock_topics:
        engagement_score = calculate_engagement_score(topic)
        topic["engagement_score"] = engagement_score
        sentiment = analyze_hashtag_sentiment(topic["topic"])
        topic["sentiment"] = sentiment
        post_content = get_hashtag_post_content(topic["topic"])
        topic["post_content"] = post_content
        print(f"  -> {topic['topic']} (Count: {topic['count']}) - Engagement: {format_engagement_display(engagement_score)} - Sentiment: {sentiment} - Post Content: {post_content}")
    
    print(f"\nMock data with engagement scores ready for Supabase storage!")
    return mock_topics

def main():
    """Main function to orchestrate the scraping and storing process."""
    print("\n--- Starting Twitter Trend Scraper ---")
    
    trending_topics = get_trending_topics()
    
    # If scraping fails, offer to test with mock data
    if not trending_topics:
        print("\nNo trending Indian hashtags found from trends24.in.")
        print("This could be due to network issues or site unavailability.")
        print("\nWould you like to test the engagement score functionality with mock data?")
        print("You can run: test_engagement_scores() in Python console or add the call below.")
        
        # Uncomment the next line to automatically test with mock data
        # trending_topics = test_engagement_scores()
    else:
        print(f"\nSuccessfully found {len(trending_topics)} unique trending Indian hashtags!")
        for topic in trending_topics:
            engagement_score = calculate_engagement_score(topic)
            topic["engagement_score"] = engagement_score
            sentiment = analyze_hashtag_sentiment(topic["topic"])
            topic["sentiment"] = sentiment
            post_content = get_hashtag_post_content(topic["topic"])
            topic["post_content"] = post_content
            print(f"  -> {topic['topic']} (Count: {topic['count']}) - Engagement: {format_engagement_display(engagement_score)} - Sentiment: {sentiment} - Post Content: {post_content}")
            print(f"     Twitter: {topic.get('twitter_link', 'N/A')}")
        
        insert_fresh_data_only(trending_topics)

if __name__ == "__main__":
    main()