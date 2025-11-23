"""
Small Business Sentiment Intelligence Platform
Backend API with AI/ML capabilities

Features:
- Sentiment analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Topic extraction using keyword matching
- Resource recommendation engine
- Social media data simulation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Initialize VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

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
    Analyze sentiment using VADER (better for social media text!)
    VADER understands emojis, slang, capitalization, and punctuation intensity
    Returns: sentiment score (-1 to 1) and classification
    """
    # Get VADER scores
    scores = vader_analyzer.polarity_scores(text)
    
    # VADER returns: neg, neu, pos, compound
    # compound is the overall score (-1 to +1)
    compound = scores['compound']
    
    # Classify based on compound score
    # VADER recommended thresholds: >= 0.05 positive, <= -0.05 negative
    if compound >= 0.05:
        sentiment = 'positive'
    elif compound <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'score': round(compound, 2),
        'sentiment': sentiment,
        'positive': round(scores['pos'], 2),
        'negative': round(scores['neg'], 2),
        'neutral': round(scores['neu'], 2)
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

# Mock Data Generator
def generate_mock_posts(count=20):
    """
    Generate realistic mock social media posts about small business experiences
    with BALANCED sentiments, topics, and sources
    """
    
    # Template posts with different sentiments and topics
    post_templates = {
        'permits': {
            'positive': [
                "Just got my Miami-Dade business license renewed online! The new portal is so much easier than before. Took only 15 minutes! 🎉",
                "Finally completed all permit paperwork for my food truck. Miami-Dade permit office was super helpful throughout the process!",
                "Permit approved! 🙌 The online system made it incredibly smooth. Highly recommend using the digital portal.",
                "Got my health permit approved in record time! Miami-Dade is really streamlining their processes. Impressed! 👍"
            ],
            'negative': [
                "Been waiting 8 weeks for my food truck permit approval in Miami-Dade. This is costing me thousands in lost revenue. Need this resolved ASAP!",
                "The permit application process is way too complicated. Spent hours trying to figure out which forms I need. Very frustrating! 😤",
                "Still no response on my permit application. Called three times, emailed twice. Getting desperate here!",
                "Why is the business permit process so confusing? Too many forms, unclear requirements. Miami-Dade needs to simplify this!",
                "Permit delays are killing my business. Been waiting 3 months with no updates. Absolutely unacceptable!"
            ],
            'neutral': [
                "Working on getting my Miami-Dade business permits today. Anyone know how long the approval typically takes?",
                "Submitted my permit application yesterday. Fingers crossed it goes smoothly.",
                "Looking into what permits I need for my new retail store in Miami-Dade. Any advice?",
                "Just filled out form BTR-1 for business permits. Pretty straightforward process."
            ]
        },
        'funding': {
            'positive': [
                "The Miami-Dade County small business grant saved my restaurant after the hurricane! Forever grateful for this program! 🙏",
                "Just received approval for a low-interest business loan from the county program. Game changer for my expansion plans!",
                "Got funding through the Miami-Dade emergency relief fund. This will help us survive the slow season. Thank you!",
                "Applied for and received a $25,000 grant! Miami-Dade really supports small businesses. So thankful! 💰"
            ],
            'negative': [
                "Applied for the small business grant three months ago, still haven't heard back. Running out of cash reserves! 😟",
                "Got rejected for the loan program. Wish they had clearer eligibility criteria. Now I don't know where to turn for funding.",
                "The grant application process is overwhelming. So many requirements and documents needed. Feeling discouraged.",
                "Need emergency funding but the application is so complex. Small businesses need help now, not in 6 months!",
                "Third time being rejected for county funding. This is ridiculous. No support for struggling businesses!"
            ],
            'neutral': [
                "Exploring funding options for my startup. Anyone have experience with Miami-Dade grant programs?",
                "Submitted my grant application today. Hope to hear back soon.",
                "Looking into the low-interest loan program. Trying to understand all the requirements.",
                "Reading through the grant eligibility criteria. Seems doable but lots of paperwork."
            ]
        },
        'training': {
            'positive': [
                "Attended the Miami-Dade small business workshop on digital marketing yesterday. Great speakers and learned so much about social media strategies! 📚",
                "The entrepreneur boot camp was amazing! Met other business owners and got solid advice on scaling my company.",
                "Just completed the financial planning workshop. Finally understand my cash flow! These training programs are invaluable.",
                "The free business courses from Miami-Dade are top-notch. Already implementing what I learned! 🌟"
            ],
            'negative': [
                "Signed up for the business training workshop but it was cancelled last minute. Really needed that info!",
                "The workshop was too basic. Wished they had more advanced training options for established businesses.",
                "Couldn't attend the training because it was only offered during business hours. Need evening options!",
                "Paid for a business seminar and it was a complete waste of time and money. Very disappointed.",
                "Miami-Dade training programs are always full. Can never get a spot. Very frustrating!"
            ],
            'neutral': [
                "Looking for good business training programs in Miami-Dade. Any recommendations?",
                "Signed up for the next entrepreneur workshop. Curious to see what I'll learn.",
                "Considering taking some business courses. Has anyone tried the county programs?",
                "Browsing through available workshops. Might register for the tax filing one."
            ]
        },
        'taxes': {
            'positive': [
                "Miami-Dade tax workshop saved me a lot of confusion! Now I understand my quarterly obligations much better.",
                "Got help from the county tax assistance program. They walked me through everything step by step. Awesome service!",
                "Finally filed my business taxes correctly thanks to the free county resources. Big relief! 😌"
            ],
            'negative': [
                "Why is the business tax filing process so complicated in Miami-Dade? Spent 3 hours trying to figure out form BTR-1. Need simpler instructions!",
                "Tax deadline approaching and I'm still confused about what I owe. The online portal is not user-friendly at all! 😫",
                "Got a penalty for late filing because I didn't understand the requirements. Wish the process was clearer from the start.",
                "Business tax system in Miami-Dade is a nightmare. Unclear instructions and unhelpful staff.",
                "Just got hit with unexpected tax penalties. The county website had wrong information. Absolutely furious!"
            ],
            'neutral': [
                "Working on my quarterly business taxes. Anyone know a good accountant in Miami-Dade?",
                "Tax season again. Time to organize all my receipts and paperwork.",
                "Trying to understand my business tax obligations. The rules seem to change every year.",
                "Downloaded the tax forms from the county website. Going through them now."
            ]
        },
        'legal': {
            'positive': [
                "Used the free legal consultation service for small businesses. They helped me understand my contract obligations. Great resource!",
                "Miami-Dade legal aid for small businesses is fantastic! Got help with my LLC formation for free.",
                "The business attorney consultation saved me from signing a bad lease. So glad Miami-Dade offers this service! ⚖️"
            ],
            'negative': [
                "Need legal help with a contract dispute but can't afford an attorney. Wish there were more free options.",
                "The legal consultation was only 30 minutes. Not enough time to cover everything I needed!",
                "Waited two weeks for a legal consultation appointment. By then my issue had gotten worse.",
                "Legal services for small businesses are inadequate. Need more support and longer consultation times.",
                "Tried to get legal help three times. Never got a callback. System is broken!"
            ],
            'neutral': [
                "Looking for legal resources for small business owners. What's available through the county?",
                "Need to review a lease agreement. Considering using the county legal services.",
                "Anyone used Miami-Dade's free legal consultation for businesses? How was it?",
                "Scheduling a legal consultation for next week. Hope it helps with my contract questions."
            ]
        },
        'general': {
            'positive': [
                "Love being a small business owner in Miami-Dade! The county has so many resources and support programs.",
                "My small business is thriving! Grateful for all the local support and programs available.",
                "Miami-Dade really knows how to support entrepreneurs. Feeling optimistic about the future! ✨"
            ],
            'negative': [
                "Running a small business in Miami-Dade is harder than expected. So many regulations and fees!",
                "Feeling overwhelmed as a new business owner. There's so much to learn and keep track of.",
                "Sometimes wonder if it's worth it. Being a small business owner is exhausting and stressful! 😓",
                "Too many bureaucratic hurdles in Miami-Dade. Makes running a business unnecessarily difficult.",
                "Business failed after 6 months. County resources weren't enough to save it. Very disappointed."
            ],
            'neutral': [
                "Another day running my small business. Some challenges but moving forward.",
                "Working on my business plan today. Lots to think about.",
                "Small business life in Miami-Dade. Taking it one day at a time.",
                "Reviewing my quarterly results. Some ups and downs but overall steady progress."
            ]
        }
    }
    
    topics = list(post_templates.keys())
    sources = ['twitter', 'facebook', 'instagram', 'reddit', 'nextdoor']
    
    # Create balanced sentiment distribution
    # Aim for realistic distribution: 40% positive, 35% negative, 25% neutral
    sentiments_pool = (
        ['positive'] * 40 + 
        ['negative'] * 35 + 
        ['neutral'] * 25
    )
    
    posts = []
    for i in range(count):
        # Pick random topic
        topic = random.choice(topics)
        
        # Pick sentiment from balanced pool
        sentiment = random.choice(sentiments_pool)
        
        # Get a random post from templates
        text = random.choice(post_templates[topic][sentiment])
        
        # Generate timestamp (within last 30 days)
        days_ago = random.randint(0, 30)
        timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        # Analyze with VADER to get score, but keep template sentiment for consistency
        analysis = analyze_sentiment(text)
        
        posts.append({
            'text': text,
            'topic': topic,
            'sentiment': sentiment,  # Use template sentiment for balanced data
            'sentiment_score': analysis['score'],  # But use VADER score
            'timestamp': timestamp,
            'source': random.choice(sources)
        })
    
    return posts

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Get analyzed social media posts - supports both real data and mock generation
    Query params:
    - count: number of posts to return (default 20)
    - mock: if 'true', generate mock data instead of using real_data.json
    """
    try:
        count = request.args.get('count', 20, type=int)
        use_mock = request.args.get('mock', 'false').lower() == 'true'
        
        # If mock requested OR real_data.json doesn't exist, generate mock data
        if use_mock or not os.path.exists('real_data.json'):
            posts = generate_mock_posts(count)
            return jsonify({
                'posts': posts,
                'total': len(posts),
                'data_source': 'mock'
            })
        
        # Otherwise, load from real_data.json
        with open('real_data.json', 'r') as f:
            import json
            all_posts = json.load(f)
            posts = all_posts[:count]
        
        # Analyze sentiment for each post using VADER
        for post in posts:
            if 'sentiment_score' not in post:
                analysis = analyze_sentiment(post['text'])
                post['sentiment_score'] = analysis['score']
                post['sentiment'] = analysis['sentiment']
        
        return jsonify({
            'posts': posts,
            'total': len(posts),
            'data_source': 'real'
        })
        
    except Exception as e:
        # If any error, fall back to mock data
        posts = generate_mock_posts(count if 'count' in locals() else 20)
        return jsonify({
            'posts': posts,
            'total': len(posts),
            'data_source': 'mock',
            'note': 'Generated mock data due to error'
        })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get overall sentiment statistics - uses real data if available, mock data otherwise
    """
    try:
        # Try to load real data first
        if os.path.exists('real_data.json'):
            with open('real_data.json', 'r') as f:
                import json
                posts = json.load(f)
        else:
            # Generate mock data for statistics
            posts = generate_mock_posts(100)
        
        # Analyze sentiment for posts that don't have it
        for post in posts:
            if 'sentiment' not in post:
                analysis = analyze_sentiment(post['text'])
                post['sentiment'] = analysis['sentiment']
        
        # Calculate statistics
        sentiments = [p.get('sentiment', 'neutral') for p in posts]
        topics = [p.get('topic', 'general') for p in posts]
        
        stats = {
            'total_posts': len(posts),
            'sentiment_breakdown': {
                'positive': sentiments.count('positive'),
                'negative': sentiments.count('negative'),
                'neutral': sentiments.count('neutral')
            },
            'topic_breakdown': {},
            'overall_sentiment_percentage': round((sentiments.count('positive') / len(posts)) * 100, 1) if posts else 0
        }
        
        # Count topics
        for topic in set(topics):
            stats['topic_breakdown'][topic] = topics.count(topic)
        
        return jsonify(stats)
        
    except Exception as e:
        # If any error, generate mock stats
        posts = generate_mock_posts(100)
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
