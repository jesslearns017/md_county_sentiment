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

# Expanded Resource Database with 12+ Categories
RESOURCES = {
    'permits': [
        {
            'id': 1,
            'name': 'Online Permit Portal',
            'description': 'Fast-track your business permits online',
            'url': 'https://business.miamidade.gov/permits',
            'keywords': ['permit', 'license', 'approval', 'registration', 'certificate', 'zoning']
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
        },
        {
            'id': 4,
            'name': 'Food Service Permits',
            'description': 'Specialized help for restaurant and food business permits',
            'url': 'https://business.miamidade.gov/food-permits',
            'keywords': ['food', 'restaurant', 'catering', 'health', 'mobile', 'truck']
        }
    ],
    'funding': [
        {
            'id': 5,
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
    ],
    'legal': [
        {
            'id': 16,
            'name': 'Legal Aid Services',
            'description': 'Free and low-cost legal assistance for small businesses',
            'url': 'https://business.miamidade.gov/legal-aid',
            'keywords': ['legal', 'lawyer', 'attorney', 'law', 'contract', 'lawsuit', 'court']
        },
        {
            'id': 17,
            'name': 'Business Structure Consultation',
            'description': 'Help choosing LLC, Corporation, or Sole Proprietorship',
            'url': 'https://business.miamidade.gov/structure',
            'keywords': ['llc', 'corporation', 'structure', 'entity', 'incorporation']
        },
        {
            'id': 18,
            'name': 'Contract Review Service',
            'description': 'Expert review of business contracts and agreements',
            'url': 'https://business.miamidade.gov/contracts',
            'keywords': ['contract', 'agreement', 'review', 'terms', 'legal']
        },
        {
            'id': 19,
            'name': 'Guardianship & Estate Planning',
            'description': 'Business succession and guardianship planning resources',
            'url': 'https://business.miamidade.gov/guardianship',
            'keywords': ['guardianship', 'estate', 'succession', 'will', 'trust', 'planning']
        }
    ],
    'insurance': [
        {
            'id': 20,
            'name': 'Business Insurance Guide',
            'description': 'Understanding liability, property, and workers comp insurance',
            'url': 'https://business.miamidade.gov/insurance',
            'keywords': ['insurance', 'liability', 'coverage', 'workers comp', 'protection']
        },
        {
            'id': 21,
            'name': 'Insurance Provider Directory',
            'description': 'Connect with business insurance providers in Miami-Dade',
            'url': 'https://business.miamidade.gov/insurance-providers',
            'keywords': ['insurance', 'provider', 'broker', 'agent', 'quote']
        },
        {
            'id': 22,
            'name': 'Health Insurance Options',
            'description': 'Affordable health insurance for small business owners',
            'url': 'https://business.miamidade.gov/health-insurance',
            'keywords': ['health', 'medical', 'insurance', 'coverage', 'benefits']
        }
    ],
    'marketing': [
        {
            'id': 23,
            'name': 'Digital Marketing Bootcamp',
            'description': 'Master social media, SEO, and online advertising',
            'url': 'https://business.miamidade.gov/marketing',
            'keywords': ['marketing', 'advertising', 'promotion', 'branding', 'social media']
        },
        {
            'id': 24,
            'name': 'Website Development Resources',
            'description': 'Build your business website with free tools and templates',
            'url': 'https://business.miamidade.gov/web-development',
            'keywords': ['website', 'web', 'online', 'digital', 'internet', 'domain']
        },
        {
            'id': 25,
            'name': 'Marketing Grant Program',
            'description': 'Grants up to $10,000 for marketing and advertising',
            'url': 'https://business.miamidade.gov/marketing-grants',
            'keywords': ['marketing', 'advertising', 'grant', 'promotion', 'budget']
        }
    ],
    'technology': [
        {
            'id': 26,
            'name': 'Technology Consultation',
            'description': 'Free IT assessment and technology planning for your business',
            'url': 'https://business.miamidade.gov/tech-consult',
            'keywords': ['technology', 'it', 'computer', 'software', 'system', 'tech']
        },
        {
            'id': 27,
            'name': 'Cybersecurity Resources',
            'description': 'Protect your business from cyber threats',
            'url': 'https://business.miamidade.gov/cybersecurity',
            'keywords': ['cybersecurity', 'security', 'hacking', 'data', 'breach', 'protection']
        },
        {
            'id': 28,
            'name': 'E-commerce Setup Help',
            'description': 'Launch your online store with expert guidance',
            'url': 'https://business.miamidade.gov/ecommerce',
            'keywords': ['ecommerce', 'online', 'store', 'shop', 'selling', 'website']
        }
    ],
    'real_estate': [
        {
            'id': 29,
            'name': 'Commercial Property Listings',
            'description': 'Find the perfect location for your business',
            'url': 'https://business.miamidade.gov/property',
            'keywords': ['property', 'real estate', 'location', 'space', 'lease', 'rent', 'office']
        },
        {
            'id': 30,
            'name': 'Zoning & Land Use Help',
            'description': 'Navigate zoning laws and land use regulations',
            'url': 'https://business.miamidade.gov/zoning',
            'keywords': ['zoning', 'land', 'property', 'location', 'code', 'regulation']
        },
        {
            'id': 31,
            'name': 'Lease Negotiation Assistance',
            'description': 'Expert help negotiating commercial leases',
            'url': 'https://business.miamidade.gov/lease-help',
            'keywords': ['lease', 'rent', 'landlord', 'negotiate', 'contract', 'space']
        }
    ],
    'hr': [
        {
            'id': 32,
            'name': 'Hiring & Employment Guide',
            'description': 'Everything you need to know about hiring employees',
            'url': 'https://business.miamidade.gov/hiring',
            'keywords': ['hiring', 'employee', 'staff', 'recruit', 'employment', 'hr', 'payroll']
        },
        {
            'id': 33,
            'name': 'Employee Benefits Planning',
            'description': 'Design competitive benefits packages for your team',
            'url': 'https://business.miamidade.gov/benefits',
            'keywords': ['benefits', 'employee', 'health', 'retirement', 'perks', 'compensation']
        },
        {
            'id': 34,
            'name': 'Workplace Compliance Training',
            'description': 'Stay compliant with labor laws and regulations',
            'url': 'https://business.miamidade.gov/compliance',
            'keywords': ['compliance', 'labor', 'law', 'regulation', 'hr', 'employee', 'rights']
        }
    ],
    'export': [
        {
            'id': 35,
            'name': 'International Trade Office',
            'description': 'Expand your business to international markets',
            'url': 'https://business.miamidade.gov/export',
            'keywords': ['export', 'international', 'trade', 'global', 'foreign', 'import']
        },
        {
            'id': 36,
            'name': 'Export Documentation Help',
            'description': 'Navigate customs, tariffs, and shipping requirements',
            'url': 'https://business.miamidade.gov/export-docs',
            'keywords': ['export', 'customs', 'shipping', 'documentation', 'international']
        },
        {
            'id': 37,
            'name': 'Trade Mission Programs',
            'description': 'Join delegations to explore new markets',
            'url': 'https://business.miamidade.gov/trade-missions',
            'keywords': ['trade', 'mission', 'international', 'export', 'delegation']
        }
    ],
    'networking': [
        {
            'id': 38,
            'name': 'Business Networking Events',
            'description': 'Monthly meetups and networking opportunities',
            'url': 'https://business.miamidade.gov/networking',
            'keywords': ['networking', 'events', 'meetup', 'connect', 'community', 'entrepreneurs']
        },
        {
            'id': 39,
            'name': 'Industry-Specific Groups',
            'description': 'Join groups focused on your industry',
            'url': 'https://business.miamidade.gov/industry-groups',
            'keywords': ['industry', 'group', 'association', 'network', 'peers', 'community']
        },
        {
            'id': 40,
            'name': 'Chamber of Commerce',
            'description': 'Connect with the Miami-Dade business community',
            'url': 'https://business.miamidade.gov/chamber',
            'keywords': ['chamber', 'commerce', 'business', 'community', 'networking']
        }
    ],
    'certification': [
        {
            'id': 41,
            'name': 'Minority Business Certification',
            'description': 'MBE certification for minority-owned businesses',
            'url': 'https://business.miamidade.gov/mbe',
            'keywords': ['minority', 'mbe', 'certification', 'diversity', 'certified']
        },
        {
            'id': 42,
            'name': 'Women-Owned Business Certification',
            'description': 'WBE certification opens doors to new contracts',
            'url': 'https://business.miamidade.gov/wbe',
            'keywords': ['women', 'wbe', 'certification', 'female', 'certified']
        },
        {
            'id': 43,
            'name': 'Small Business Certification',
            'description': 'SBE certification for County contracting opportunities',
            'url': 'https://business.miamidade.gov/sbe',
            'keywords': ['small', 'sbe', 'certification', 'certified', 'contractor']
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
    
    # Comprehensive topic keywords for 12 categories
    topic_keywords = {
        'permits': ['permit', 'license', 'approval', 'registration', 'certificate', 'zoning', 'inspection', 'code'],
        'funding': ['grant', 'loan', 'funding', 'money', 'finance', 'capital', 'investment', 'relief'],
        'training': ['training', 'workshop', 'course', 'education', 'learn', 'teach', 'bootcamp', 'class'],
        'taxes': ['tax', 'taxes', 'irs', 'filing', 'deduction', 'credit', 'return', 'obligation'],
        'legal': ['legal', 'lawyer', 'attorney', 'law', 'contract', 'lawsuit', 'court', 'guardianship', 'estate', 'succession', 'llc', 'corporation', 'incorporation', 'entity', 'structure'],
        'insurance': ['insurance', 'liability', 'coverage', 'workers comp', 'protection', 'health insurance', 'medical', 'benefits', 'broker', 'agent'],
        'marketing': ['marketing', 'advertising', 'promotion', 'branding', 'social media', 'website', 'web', 'online presence', 'seo', 'digital'],
        'technology': ['technology', 'it', 'computer', 'software', 'system', 'tech', 'cybersecurity', 'security', 'ecommerce', 'online store'],
        'real_estate': ['property', 'real estate', 'location', 'space', 'lease', 'rent', 'office', 'zoning', 'land use', 'landlord'],
        'hr': ['hiring', 'employee', 'staff', 'recruit', 'employment', 'hr', 'payroll', 'benefits', 'compensation', 'compliance', 'labor'],
        'export': ['export', 'international', 'trade', 'global', 'foreign', 'import', 'customs', 'shipping', 'tariff'],
        'networking': ['networking', 'events', 'meetup', 'connect', 'community', 'entrepreneurs', 'chamber', 'industry group'],
        'certification': ['minority', 'mbe', 'wbe', 'sbe', 'certification', 'certified', 'women-owned', 'diversity', 'contractor'],
        'support': ['help', 'support', 'assistance', 'advisor', 'mentor', 'guidance', 'hotline', 'question']
    }
    
    # Check for matches in order of specificity (most specific first)
    for topic, keywords in topic_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            topics.append(topic)
    
    # Remove duplicates while preserving order
    seen = set()
    topics = [x for x in topics if not (x in seen or seen.add(x))]
    
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
    Get social media posts - real or mock data
    """
    count = request.args.get('count', 20, type=int)
    
    # Try to load real data first
    try:
        with open('real_data.json', 'r') as f:
            import json
            all_posts = json.load(f)
            posts = all_posts[:count]
            print(f"✅ Loaded {len(posts)} posts from real_data.json")
    except FileNotFoundError:
        # Fall back to mock data if file doesn't exist
        posts = generate_mock_posts(count)
        print(f"ℹ️ Using mock data ({len(posts)} posts)")
    
    # Analyze each post
    for post in posts:
        if 'sentiment_score' not in post:
            analysis = analyze_sentiment(post['text'])
            post['sentiment_score'] = analysis['score']
    
    return jsonify({
        'posts': posts,
        'total': len(posts),
        'data_source': 'real' if 'real_data.json' else 'mock'
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
