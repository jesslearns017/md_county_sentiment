"""
Social Media Data Scraper for Small Business Sentiment Analysis
Collects posts from Twitter, Reddit, and simulates Facebook data

Usage:
    python data_scraper.py --source twitter --count 100
    python data_scraper.py --source reddit --count 50
    python data_scraper.py --source all --count 100

Requirements:
    pip install tweepy praw textblob pandas --break-system-packages
"""

import argparse
import json
from datetime import datetime
import pandas as pd

# You'll need to fill these in with your own API credentials
TWITTER_CONFIG = {
    'consumer_key': 'YOUR_CONSUMER_KEY',
    'consumer_secret': 'YOUR_CONSUMER_SECRET',
    'access_token': 'YOUR_ACCESS_TOKEN',
    'access_token_secret': 'YOUR_ACCESS_TOKEN_SECRET'
}

REDDIT_CONFIG = {
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'user_agent': 'SmallBusinessSentiment/1.0'
}

# Search queries for Miami-Dade business topics
SEARCH_QUERIES = [
    "Miami-Dade small business",
    "Miami business permit",
    "Miami-Dade business license",
    "Miami small business grant",
    "Miami business help",
    "South Florida small business",
    "#MiamiSmallBusiness",
    "#MiamiEntrepreneur"
]

def scrape_twitter(count=100):
    """
    Scrape tweets about Miami-Dade small businesses
    """
    try:
        import tweepy
        
        # Authenticate
        auth = tweepy.OAuthHandler(
            TWITTER_CONFIG['consumer_key'],
            TWITTER_CONFIG['consumer_secret']
        )
        auth.set_access_token(
            TWITTER_CONFIG['access_token'],
            TWITTER_CONFIG['access_token_secret']
        )
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        posts = []
        
        print(f"🐦 Scraping Twitter for {count} tweets...")
        
        for query in SEARCH_QUERIES:
            try:
                tweets = api.search_tweets(
                    q=query,
                    lang='en',
                    count=min(100, count // len(SEARCH_QUERIES)),
                    tweet_mode='extended'
                )
                
                for tweet in tweets:
                    posts.append({
                        'id': tweet.id,
                        'text': tweet.full_text,
                        'source': 'twitter',
                        'author': tweet.user.screen_name,
                        'created_at': tweet.created_at.isoformat(),
                        'likes': tweet.favorite_count,
                        'retweets': tweet.retweet_count,
                        'url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                    })
                
                print(f"  ✓ Found {len(tweets)} tweets for '{query}'")
                
            except Exception as e:
                print(f"  ✗ Error with query '{query}': {e}")
        
        print(f"✅ Collected {len(posts)} tweets total")
        return posts
        
    except ImportError:
        print("❌ Tweepy not installed. Run: pip install tweepy")
        return []
    except Exception as e:
        print(f"❌ Twitter scraping failed: {e}")
        print("💡 Make sure your API credentials are set up correctly")
        return []

def scrape_reddit(count=50):
    """
    Scrape Reddit posts about Miami-Dade small businesses
    """
    try:
        import praw
        
        # Authenticate
        reddit = praw.Reddit(
            client_id=REDDIT_CONFIG['client_id'],
            client_secret=REDDIT_CONFIG['client_secret'],
            user_agent=REDDIT_CONFIG['user_agent']
        )
        
        posts = []
        
        print(f"🤖 Scraping Reddit for {count} posts...")
        
        # Relevant subreddits
        subreddits = ['Miami', 'Florida', 'smallbusiness', 'Entrepreneur']
        
        for subreddit_name in subreddits:
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Search for small business related posts
                for query in ['small business', 'business permit', 'startup Miami']:
                    for submission in subreddit.search(query, limit=count // len(subreddits)):
                        posts.append({
                            'id': submission.id,
                            'text': f"{submission.title} {submission.selftext}",
                            'source': 'reddit',
                            'subreddit': subreddit_name,
                            'author': str(submission.author),
                            'created_at': datetime.fromtimestamp(submission.created_utc).isoformat(),
                            'score': submission.score,
                            'num_comments': submission.num_comments,
                            'url': f"https://reddit.com{submission.permalink}"
                        })
                
                print(f"  ✓ Scraped r/{subreddit_name}")
                
            except Exception as e:
                print(f"  ✗ Error with r/{subreddit_name}: {e}")
        
        print(f"✅ Collected {len(posts)} Reddit posts")
        return posts
        
    except ImportError:
        print("❌ PRAW not installed. Run: pip install praw")
        return []
    except Exception as e:
        print(f"❌ Reddit scraping failed: {e}")
        print("💡 Make sure your Reddit API credentials are set up correctly")
        return []

def generate_mock_data(count=100):
    """
    Generate mock social media posts for testing
    """
    import random
    
    print(f"🎭 Generating {count} mock posts...")
    
    templates = [
        "Just got my business license approved! The online portal made it so easy. #MiamiSmallBusiness",
        "Still waiting on my permit approval. It's been {weeks} weeks. Very frustrating.",
        "The small business grant workshop was incredibly helpful! Highly recommend.",
        "Why is the business tax process so complicated in Miami-Dade? Need help!",
        "Attended the entrepreneur training session. Great resources available!",
        "County website is confusing. Can't find information about health permits.",
        "Got connected with a business advisor through the county. Game changer!",
        "The pandemic relief program saved my restaurant. Forever grateful.",
        "Applied for a business grant {weeks} weeks ago. No response yet. Anyone else?",
        "Business license renewal process was smooth this year. Much improved!",
        "Trying to start a food truck in Miami. Where do I even begin with permits?",
        "The County's small business hotline was super helpful. Got answers immediately.",
        "Frustrated with the zoning approval process. Been waiting months.",
        "Just received my certificate of use! Ready to open my coffee shop! ☕",
        "Does anyone know about tax incentives for minority-owned businesses in Miami-Dade?",
        "The business development center helped me write my business plan. Free service!",
        "Permit fees seem high compared to other counties. Is this normal?",
        "Finally got my vendors license. Now I can sell at the farmers market!",
        "Looking for small business networking groups in Miami. Recommendations?",
        "The county's website redesign made finding resources so much easier.",
    ]
    
    posts = []
    for i in range(count):
        template = random.choice(templates)
        text = template.format(weeks=random.randint(2, 8))
        
        posts.append({
            'id': f'mock_{i}',
            'text': text,
            'source': random.choice(['twitter', 'reddit', 'facebook']),
            'author': f'user{random.randint(1000, 9999)}',
            'created_at': datetime.now().isoformat(),
            'engagement': random.randint(0, 100)
        })
    
    print(f"✅ Generated {len(posts)} mock posts")
    return posts

def analyze_posts(posts):
    """
    Add sentiment analysis to collected posts
    """
    try:
        from textblob import TextBlob
        
        print(f"🔍 Analyzing sentiment for {len(posts)} posts...")
        
        for post in posts:
            blob = TextBlob(post['text'])
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            post['sentiment'] = sentiment
            post['sentiment_score'] = round(polarity, 2)
            post['subjectivity'] = round(blob.sentiment.subjectivity, 2)
        
        # Calculate statistics
        sentiments = [p['sentiment'] for p in posts]
        stats = {
            'total': len(posts),
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral'),
            'positive_percentage': round((sentiments.count('positive') / len(posts)) * 100, 1)
        }
        
        print(f"✅ Analysis complete:")
        print(f"   Positive: {stats['positive']} ({stats['positive_percentage']}%)")
        print(f"   Negative: {stats['negative']}")
        print(f"   Neutral: {stats['neutral']}")
        
        return posts, stats
        
    except ImportError:
        print("❌ TextBlob not installed. Run: pip install textblob")
        return posts, {}

def save_data(posts, stats, format='json'):
    """
    Save collected data to file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == 'json':
        # Save posts
        filename = f'social_media_posts_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(posts, f, indent=2)
        print(f"💾 Saved {len(posts)} posts to {filename}")
        
        # Save stats
        stats_filename = f'sentiment_stats_{timestamp}.json'
        with open(stats_filename, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"📊 Saved statistics to {stats_filename}")
        
    elif format == 'csv':
        df = pd.DataFrame(posts)
        filename = f'social_media_posts_{timestamp}.csv'
        df.to_csv(filename, index=False)
        print(f"💾 Saved {len(posts)} posts to {filename}")
    
    return filename

def main():
    parser = argparse.ArgumentParser(description='Scrape social media for small business sentiment')
    parser.add_argument('--source', choices=['twitter', 'reddit', 'mock', 'all'], default='mock',
                        help='Data source to scrape')
    parser.add_argument('--count', type=int, default=100,
                        help='Number of posts to collect')
    parser.add_argument('--format', choices=['json', 'csv'], default='json',
                        help='Output format')
    parser.add_argument('--no-analyze', action='store_true',
                        help='Skip sentiment analysis')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🏢 Small Business Sentiment Data Scraper")
    print("="*60 + "\n")
    
    # Collect data
    posts = []
    
    if args.source == 'twitter' or args.source == 'all':
        posts.extend(scrape_twitter(args.count))
    
    if args.source == 'reddit' or args.source == 'all':
        posts.extend(scrape_reddit(args.count))
    
    if args.source == 'mock' or (args.source == 'all' and len(posts) == 0):
        posts.extend(generate_mock_data(args.count))
    
    if not posts:
        print("❌ No data collected. Using mock data instead.")
        posts = generate_mock_data(args.count)
    
    # Analyze sentiment
    if not args.no_analyze:
        posts, stats = analyze_posts(posts)
    else:
        stats = {}
    
    # Save data
    filename = save_data(posts, stats, args.format)
    
    print("\n" + "="*60)
    print("✅ Data collection complete!")
    print(f"📁 File: {filename}")
    print(f"📊 Posts: {len(posts)}")
    print("="*60 + "\n")
    
    print("💡 Next steps:")
    print("   1. Review the collected data")
    print("   2. Import into your Flask API")
    print("   3. Visualize in your React dashboard")
    print("\n")

if __name__ == '__main__':
    # Quick test without API credentials
    print("\n🚀 Running in demo mode with mock data...\n")
    posts = generate_mock_data(50)
    posts, stats = analyze_posts(posts)
    save_data(posts, stats, 'json')
    
    print("\n💡 To scrape real data:")
    print("   1. Get Twitter API credentials from developer.twitter.com")
    print("   2. Get Reddit API credentials from reddit.com/prefs/apps")
    print("   3. Update TWITTER_CONFIG and REDDIT_CONFIG in this file")
    print("   4. Run: python data_scraper.py --source twitter --count 100")
    print("\n")
