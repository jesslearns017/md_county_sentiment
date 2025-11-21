"""
Small Business Sentiment Intelligence Platform
Backend API with AI/ML capabilities

Features:
- Sentiment analysis using TextBlob
- Topic extraction using keyword matching
- Resource recommendation engine
- Social media data simulation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import re
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Resource Database
RESOURCES = {
    'permits': [
        {
            'id': 1,
            'name': 'Online Permit Portal',
            'description': 'Fast-track your business permits online',
            'url': 'https://business.miamidade.gov/permits',
            'keywords': ['permit', 'license', 'approval', 'registration']
        },
        {
            'id': 2,
            'name': 'Permit Assistance Program',
            'description': 'Get help navigating the permit process',
            'url': 'https://business.miamidade.gov/permit-help',
            'keywords': ['permit', 'help', 'guidance', 'assistance']
        },
        {
            'id': 3,
            'name': 'Virtual Permit Workshops',
            'description': 'Weekly sessions on permit requirements',
            'url': 'https://business.miamidade.gov/workshops',
            'keywords': ['permit', 'training', 'workshop', 'learn']
        }
    ],
    'funding': [
        {
            'id': 4,
            'name': 'Small Business Grant Program',
            'description': 'Grants up to $50,000 for eligible businesses',
            'url': 'https://business.miamidade.gov/grants',
            'keywords': ['grant', 'money', 'funding', 'financial']
        },
        {
            'id': 5,
            'name': 'Low-Interest Loan Program',
            'description': 'Competitive rates for business expansion',
            'url': 'https://business.miamidade.gov/loans',
            'keywords': ['loan', 'credit', 'financing', 'capital']
        },
        {
            'id': 6,
            'name': 'Emergency Relief Fund',
            'description': 'Support for businesses facing hardship',
            'url': 'https://business.miamidade.gov/relief',
            'keywords': ['emergency', 'relief', 'pandemic', 'crisis']
        }
    ],
    'training': [
        {
            'id': 7,
            'name': 'Entrepreneur Boot Camp',
            'description': '12-week intensive business training',
            'url': 'https://business.miamidade.gov/bootcamp',
            'keywords': ['training', 'education', 'course', 'learn']
        },
        {
            'id': 8,
            'name': 'Digital Marketing Workshop',
            'description': 'Learn to market your business online',
            'url': 'https://business.miamidade.gov/digital',
            'keywords': ['marketing', 'digital', 'online', 'social media']
        },
        {
            'id': 9,
            'name': 'Financial Planning Sessions',
            'description': 'Master your business finances',
            'url': 'https://business.miamidade.gov/finance',
            'keywords': ['financial', 'accounting', 'budget', 'planning']
        }
    ],
    'taxes': [
        {
            'id': 10,
            'name': 'Business Tax Calculator',
            'description': 'Estimate your tax obligations',
            'url': 'https://business.miamidade.gov/tax-calc',
            'keywords': ['tax', 'calculate', 'estimate', 'obligation']
        },
        {
            'id': 11,
            'name': 'Tax Filing Assistance',
            'description': 'Free help with business tax returns',
            'url': 'https://business.miamidade.gov/tax-help',
            'keywords': ['tax', 'filing', 'return', 'help']
        },
        {
            'id': 12,
            'name': 'Tax Credit Information',
            'description': 'Discover available tax incentives',
            'url': 'https://business.miamidade.gov/credits',
            'keywords': ['tax', 'credit', 'incentive', 'deduction']
        }
    ],
    'support': [
        {
            'id': 13,
            'name': 'Business Advisor Matching',
            'description': 'Get paired with an expert advisor',
            'url': 'https://business.miamidade.gov/advisors',
            'keywords': ['advisor', 'consultant', 'expert', 'guidance']
        },
        {
            'id': 14,
            'name': 'Mentorship Program',
            'description': 'Connect with successful entrepreneurs',
            'url': 'https://business.miamidade.gov/mentors',
            'keywords': ['mentor', 'coach', 'guidance', 'support']
        },
        {
            'id': 15,
            'name': '24/7 Business Hotline',
            'description': 'Call anytime for quick answers',
            'url': 'https://business.miamidade.gov/hotline',
            'keywords': ['help', 'support', 'questions', 'hotline']
        }
    ]
}

def analyze_sentiment(text):
    """
    Analyze sentiment using TextBlob
    Returns: sentiment score (-1 to 1) and classification
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'score': round(polarity, 2),
        'sentiment': sentiment,
        'subjectivity': round(blob.sentiment.subjectivity, 2)
    }

def extract_topics(text):
    """
    Extract topics from text using keyword matching
    Returns: list of topics found
    """
    text_lower = text.lower()
    topics = []
    
    topic_keywords = {
        'permits': ['permit', 'license', 'approval', 'registration', 'certificate'],
        'funding': ['grant', 'loan', 'funding', 'money', 'finance', 'capital'],
        'training': ['training', 'workshop', 'course', 'education', 'learn', 'teach'],
        'taxes': ['tax', 'taxes', 'irs', 'filing', 'deduction'],
        'support': ['help', 'support', 'assistance', 'advisor', 'mentor']
    }
    
    for topic, keywords in topic_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            topics.append(topic)
    
    return topics if topics else ['support']  # Default to support

def recommend_resources(query, topics):
    """
    Recommend resources based on query and detected topics
    Returns: list of relevant resources
    """
    recommendations = []
    query_lower = query.lower()
    
    # Get resources for detected topics
    for topic in topics:
        if topic in RESOURCES:
            topic_resources = RESOURCES[topic]
            
            # Score each resource based on keyword matches
            for resource in topic_resources:
                score = 0
                for keyword in resource['keywords']:
                    if keyword in query_lower:
                        score += 1
                
                recommendations.append({
                    **resource,
                    'relevance_score': score,
                    'topic': topic
                })
    
    # Sort by relevance and return top 3
    recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
    return recommendations[:3]

def generate_mock_posts(count=20):
    """
    Generate mock social media posts for testing
    """
    templates = [
        ("Just got my business license approved! The online portal made it so easy. Thank you Miami-Dade!", "positive", "permits"),
        ("Still waiting on my permit approval. It's been {weeks} weeks. This is frustrating.", "negative", "permits"),
        ("The small business grant workshop was incredibly helpful. Learned so much!", "positive", "funding"),
        ("Why is the business tax process so complicated? Need more guidance.", "negative", "taxes"),
        ("Attended the entrepreneur training session. Great resources available!", "positive", "training"),
        ("County website is confusing. Can't find information about health permits.", "negative", "permits"),
        ("Got connected with a business advisor through the county. Game changer!", "positive", "support"),
        ("The pandemic relief program saved my restaurant. Forever grateful.", "positive", "funding"),
        ("Applied for a grant {weeks} weeks ago. No response yet. Anyone else?", "neutral", "funding"),
        ("Business license renewal process was smooth. Much better than last year!", "positive", "permits"),
    ]
    
    posts = []
    for i in range(count):
        template = random.choice(templates)
        text = template[0].format(weeks=random.randint(2, 8))
        
        # Add timestamp
        hours_ago = random.randint(1, 168)  # Last 7 days
        timestamp = datetime.now() - timedelta(hours=hours_ago)
        
        posts.append({
            'id': i + 1,
            'text': text,
            'sentiment': template[1],
            'topic': template[2],
            'timestamp': timestamp.isoformat(),
            'source': random.choice(['Twitter', 'Reddit', 'Facebook'])
        })
    
    return posts

# API Endpoints

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze sentiment and extract topics from text
    """
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    sentiment_result = analyze_sentiment(text)
    topics = extract_topics(text)
    
    return jsonify({
        'text': text,
        'sentiment': sentiment_result,
        'topics': topics
    })

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    Get resource recommendations based on query
    """
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Analyze the query
    sentiment_result = analyze_sentiment(query)
    topics = extract_topics(query)
    recommendations = recommend_resources(query, topics)
    
    return jsonify({
        'query': query,
        'sentiment': sentiment_result,
        'topics': topics,
        'recommendations': recommendations
    })

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Get mock social media posts
    """
    count = request.args.get('count', 20, type=int)
    posts = generate_mock_posts(count)
    
    # Analyze each post
    for post in posts:
        analysis = analyze_sentiment(post['text'])
        post['sentiment_score'] = analysis['score']
    
    return jsonify({
        'posts': posts,
        'total': len(posts)
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get overall sentiment statistics
    """
    posts = generate_mock_posts(100)
    
    # Calculate statistics
    sentiments = [p['sentiment'] for p in posts]
    topics = [p['topic'] for p in posts]
    
    stats = {
        'total_posts': len(posts),
        'sentiment_breakdown': {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        },
        'topic_breakdown': {},
        'overall_sentiment_percentage': round((sentiments.count('positive') / len(posts)) * 100, 1)
    }
    
    # Count topics
    for topic in set(topics):
        stats['topic_breakdown'][topic] = topics.count(topic)
    
    return jsonify(stats)

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

# Demo route
@app.route('/')
def index():
    return """
    <h1>🏢 Small Business Sentiment Intelligence API</h1>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><strong>POST /api/analyze</strong> - Analyze sentiment of text</li>
        <li><strong>POST /api/recommend</strong> - Get resource recommendations</li>
        <li><strong>GET /api/posts</strong> - Get mock social media posts</li>
        <li><strong>GET /api/statistics</strong> - Get sentiment statistics</li>
        <li><strong>GET /api/health</strong> - Health check</li>
    </ul>
    
    <h2>Quick Test:</h2>
    <p>Try this in your terminal:</p>
    <pre>
curl -X POST http://localhost:5000/api/recommend \\
  -H "Content-Type: application/json" \\
  -d '{"query": "I need help getting a business permit"}'
    </pre>
    """

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    # Default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running in production or development
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    print("🚀 Starting Small Business Sentiment Intelligence API...")
    print(f"📊 Running on port {port}")
    print(f"🌍 Environment: {'Production' if is_production else 'Development'}")
    
    if not is_production:
        print("\n💡 Quick start commands:")
        print(f"  curl http://localhost:{port}/api/health")
        print(f"  curl http://localhost:{port}/api/posts")
    
    print("\n✨ Ready to analyze sentiment and recommend resources!")
    
    # Use debug=False in production for security and performance
    app.run(debug=not is_production, host='0.0.0.0', port=port)
