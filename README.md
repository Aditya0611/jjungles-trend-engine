# Twitter Trending Hashtags Scraper

A Python-based web scraper that extracts trending hashtags from trends24.in (India) and stores them in Supabase with sentiment analysis and engagement scoring.

## Features

- Scrapes trending hashtags from trends24.in for India
- Calculates engagement scores (1-10 scale) for each hashtag
- Performs sentiment analysis (Positive/Negative/Neutral)
- Generates Twitter and Instagram search links
- Stores data in Supabase database
- Fresh data insertion (clears old data before inserting new)
- Filters for Indian-relevant content

## Requirements

- Python 3.7+
- Supabase account and project
- Internet connection for web scraping

## Installation

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

## Supabase Setup

Create a table named `Twitter trending_Hashtags` in your Supabase project with the following columns:

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

## Usage

Run the scraper:
```bash
python t3_scraper.py
```

The script will:
1. Connect to Supabase using your credentials
2. Scrape trending topics from trends24.in
3. Calculate engagement scores and sentiment for each hashtag
4. Clear existing data and insert fresh trending topics
5. Display results in the terminal

## Configuration

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

## Project Structure

```
├── t3_scraper.py          # Main scraper script
├── config_manager.py      # Configuration management
├── config.txt            # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # Project documentation
```

## Functions Overview

- `get_trending_topics()` - Scrapes trends from trends24.in
- `analyze_hashtag_sentiment()` - Performs sentiment analysis using TextBlob
- `calculate_engagement_score()` - Calculates engagement scores (1-10)
- `insert_fresh_data_only()` - Clears old data and inserts fresh trends
- `is_indian_text()` - Filters for India-relevant content

## Data Schema

Each trending hashtag includes:
- **topic**: The hashtag text (e.g., "#TrendingNow")
- **count**: Tweet count if available (e.g., "25K")
- **engagement_score**: Calculated score from 1-10
- **sentiment**: Positive/Negative/Neutral
- **twitter_link**: Direct Twitter search URL
- **post_content**: Sample post content for the hashtag

## Error Handling

The scraper includes robust error handling for:
- Network connectivity issues
- Supabase connection problems
- Website structure changes
- Missing environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Notes

- The scraper respects website rate limits and includes appropriate delays
- Trending topics are filtered for Indian relevance
- Data is refreshed completely on each run for accuracy
- Ensure your Supabase RLS policies allow insertions if enabled
