# Jjungles Trend Engine

A comprehensive social media trend analysis toolkit featuring both Twitter and TikTok hashtag scrapers with advanced analytics and database integration.

## 🚀 Projects Overview

This repository contains two powerful scraping tools:

### 1. Twitter Trending Hashtags Scraper
A Python-based web scraper that extracts trending hashtags from trends24.in (India) and stores them in Supabase with sentiment analysis and engagement scoring.

### 2. TikTok Hashtag Scraper V4
A powerful Python-based web scraper that extracts trending hashtags from TikTok's Creative Center with advanced features including engagement scoring, sentiment analysis, and automatic Supabase database integration.

---

## 📱 Twitter Scraper Features

- 🔥 Scrapes trending hashtags from trends24.in for India
- 📊 Calculates engagement scores (1-10 scale) for each hashtag
- 😊 Performs sentiment analysis (Positive/Negative/Neutral)
- 🔗 Generates Twitter and Instagram search links
- 💾 Stores data in Supabase database
- 🧹 Fresh data insertion (clears old data before inserting new)
- 🎯 Filters for Indian-relevant content

## � TikTok Scraper Features

### Core Functionality
- **Multi-URL Strategy**: Scrapes from multiple TikTok Creative Center regions (US, GB, IN, SG)
- **Smart "View More" Detection**: Automatically finds and clicks pagination buttons to load additional content
- **Comprehensive Data Extraction**: Extracts hashtag names, post counts, rankings, and categories
- **Duplicate Prevention**: Automatically removes duplicate hashtags

### Advanced Analytics
- **Engagement Score Calculation**: 1-10 scale scoring based on post volume, category popularity, and trending keywords
- **Sentiment Analysis**: Uses TextBlob library for sentiment classification
- **Smart Categorization**: Automatically categorizes hashtags into 12 major categories

---

## 📋 Requirements

### Common Dependencies
- Python 3.7+
- Internet connection for web scraping

### Twitter Scraper Dependencies
```
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
supabase>=1.0.0
textblob>=0.17.0
```

### TikTok Scraper Dependencies
```
selenium>=4.0.0
undetected-chromedriver>=3.5.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
requests>=2.28.0
textblob>=0.17.0
supabase>=1.0.0
```

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/Aditya0611/jjungles-trend-engine.git
cd jjungles-trend-engine
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` file and add your Supabase credentials:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

## 🚀 Usage

### Twitter Scraper
```bash
python t3_scraper.py
```

### TikTok Scraper
```bash
python base.py
```

## ⚙️ Configuration

### Twitter Scraper Configuration
Edit `config.txt` to customize scraper behavior:
```json
{
    "TWEET_MAX_CHARS": 280,
    "HEADLESS_MODE": false,
    "ENGLISH_ONLY_REGEX": false,
    "SLEEP_TIME_PAGE_LOAD": 5,
    "SLEEP_TIME_AFTER_COOKIE_CONSENT": 2,
    "SLEEP_TIME_AFTER_TAB_CLICK": 3
}
```

### TikTok Scraper Configuration
Modify the `config` dictionary in the `main()` function of `base.py`:
```python
config = {
    'scrolls': 15,          # Number of scroll attempts
    'delay': 3,             # Delay between scrolls (seconds)
    'headless': False,      # Run browser in background
    'output_file': None,    # Custom output filename
    'debug': True           # Enable debug output
}
```

## 💾 Database Setup

### Supabase Setup
1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Update credentials in your `.env` file

### Twitter Scraper Table
```sql
CREATE TABLE "Twitter trending_Hashtags" (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    count TEXT,
    engagement_score INTEGER,
    sentiment TEXT,
    twitter_link TEXT,
    post_content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### TikTok Scraper Table
```sql
CREATE TABLE tiktok_hashtags (
    id SERIAL PRIMARY KEY,
    rank INTEGER,
    hashtag TEXT NOT NULL,
    posts TEXT,
    views TEXT,
    category TEXT DEFAULT 'General',
    engagement_score DECIMAL(3,1),
    sentiment_polarity DECIMAL(4,3),
    sentiment_label TEXT DEFAULT 'Neutral',
    scraped_at TIMESTAMP DEFAULT NOW(),
    original_text TEXT
);
```

## 📁 Project Structure

```
jjungles-trend-engine/
├── t3_scraper.py          # Twitter scraper main script
├── base.py               # TikTok scraper main script
├── config_manager.py     # Twitter scraper configuration management
├── config.txt           # Twitter scraper configuration settings
├── requirements.txt     # Python dependencies for both scrapers
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore patterns
└── README.md          # This documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

These scrapers are designed for research and educational purposes. Users are responsible for complying with platform terms of service and applicable laws.

## 📝 Notes

- Both scrapers respect website rate limits and include appropriate delays
- Data is refreshed completely on each run for accuracy
- Ensure your Supabase RLS policies allow insertions if enabled
- For TikTok scraper: Please respect TikTok's terms of service and rate limits

---

**Last Updated**: September 2025  
**Compatibility**: Python 3.7+, Chrome Latest
