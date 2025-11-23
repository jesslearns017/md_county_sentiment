# 🏛️ Miami-Dade County Small Business Sentiment Intelligence Platform

AI-powered sentiment analysis and resource recommendation system for Miami-Dade County small business owners.

![Miami-Dade County](https://img.shields.io/badge/Miami--Dade%20County-Official%20Demo-0075C9)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![VADER](https://img.shields.io/badge/VADER-Sentiment-orange)
![Passion Project](https://img.shields.io/badge/Type-Passion%20Project-ff69b4)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Features](#features)
- [Why I Built This](#why-i-built-this)
- [Technologies](#technologies)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Project Structure](#project-structure)


---

## 🎯 Overview

This platform was developed out of **personal passion to help Miami-Dade County small businesses** - not as a required assignment, but as a voluntary initiative to create real impact.

### What It Does

The system provides Miami-Dade County with an intelligent platform to:
- **Analyze sentiment** from small business owners' social media posts using VADER
- **Recommend resources** from 44+ county programs across 13 categories
- **Track satisfaction trends** in real-time with visual dashboards
- **Provide AI assistance** through an interactive chatbot interface
- **Generate realistic data** for testing and demonstrations

### Why This Matters

I wanted to create a practical solution that would genuinely help entrepreneurs in my community navigate the challenges of starting and running a business. Rather than just building something to meet requirements, 
I chose to build something that could actually be deployed and used.

---

## 🌐 Live Demo

**Frontend Dashboard:** [https://mdcountysentiment.netlify.app](https://mdcountysentiment.netlify.app)

**Backend API:** [https://md-county-sentiment.onrender.com](https://md-county-sentiment.onrender.com)

**API Health:** [https://md-county-sentiment.onrender.com/api/health](https://md-county-sentiment.onrender.com/api/health)

---

## ✨ Features

### 🧠 AI Sentiment Analysis
- **VADER** for accurate sentiment detection
- Positive, negative, and neutral percentage breakdown
- Topic detection across 13 business categories
- Real-time processing

### 💬 Interactive AI Chatbot
- Natural language understanding
- 8 quick-reply buttons (Permits, Funding, Training, etc.)
- Smart resource recommendations
- Improved UX with optimized button placement

### 🎲 Dynamic Mock Data Generation
- **120+ unique post templates** across 6 topics
- Generates realistic social media posts on-demand
- Perfect for demonstrations and scalability testing
- API parameter: `?mock=true`

### 📊 Social Media Dashboard
- Real-time sentiment tracking
- Visual statistics cards
- Color-coded post display
- Load 10, 50, or 100+ posts instantly

### 🎯 Smart Resource Matching
- **44+ Miami-Dade County resources**
- **13 categories**
- Keyword-based relevance scoring
- Direct links to county services

---

## 💝 Why I Built This

### Personal Initiative

This project was **voluntarily undertaken** - not because it was required, but because I wanted to:
- ✅ Address a real community need
- ✅ Create a production-ready solution
- ✅ Integrate cutting-edge AI/ML technology
- ✅ Build something that could actually be used
- ✅ Demonstrate initiative beyond the classroom
- ✅ Use my skills to make a positive impact

---

## 🛠️ Technologies

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python 3.11, Flask 3.0.0
- **AI/ML:** VADER Sentiment 3.3.2
- **Hosting:** Netlify (frontend) + Render (backend)
- **API:** RESTful with 5 endpoints

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/jesslearns017/md_county_sentiment.git
cd md_county_sentiment
```

2. **Install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the backend**
```bash
python backend_api.py
```

4. **Open index.html** in your browser

---

## 📚 API Documentation

Base URL: `https://md-county-sentiment.onrender.com`

### Key Endpoints

**Health Check:**
```bash
GET /api/health
```

**Analyze Sentiment:**
```bash
POST /api/analyze
Content-Type: application/json
{"text": "Your text here"}
```

**Get Recommendations:**
```bash
POST /api/recommend
Content-Type: application/json
{"query": "I need help with permits"}
```

**Get Posts:**
```bash
# Real data
GET /api/posts?count=10

# Mock data
GET /api/posts?count=50&mock=true
```

**Get Statistics:**
```bash
GET /api/statistics
```

---

## 🌍 Deployment

### Backend (Render)
1. Push to GitHub
2. Connect repository to Render
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn backend_api:app`

### Frontend (Netlify)
1. Connect repository to Netlify
2. Auto-deploys on git push

---

## 📁 Project Structure

```
md_county_sentiment/
├── index.html           # Frontend dashboard
├── backend_api.py      # Flask API + VADER + Mock Generator
├── requirements.txt    # Python dependencies
├── real_data.json      # Social media posts (optional)
├── README.md           # Documentation
└── .gitignore          # Git ignore rules
```

---

## 🎓 Project Background

**Personal Initiative:** This project was voluntarily undertaken out of passion - not as a required assignment.

**Institution:** Miami Dade College  
**Program:** Data Analytics 
**Year:** 2025  
**Instructor:** Dr. Ernesto Lee
**Motivation:** Genuine desire to use technology to solve real-world problems, inspired by Dr. Lee's challenge to step outside my 
comfort zone

### Skills Demonstrated
- Full-stack development
- RESTful API design
- Natural Language Processing (VADER)
- Cloud deployment
- Self-directed learning
- Initiative beyond requirements
- Stepping outside comfort zone to tackle ambitious challenges
  
---

## 📝 License

MIT License

---

## 🙏 Acknowledgments

- **Dr. Ernesto Lee** - Instructor and mentor who challenged me to step out of my comfort zone and pursue this ambitious project. 
  His encouragement to think beyond requirements made this possible.
- **Miami-Dade County Small Business Community** - The inspiration
- **Miami Dade College** - Educational support
- **VADER Sentiment Analysis** - C.J. Hutto & Eric Gilbert
- **Flask Community** - Excellent framework
- **Render & Netlify** - Free hosting platforms

---

**Links:**
- Live Demo: https://mdcountysentiment.netlify.app
- API: https://md-county-sentiment.onrender.com
- GitHub: https://github.com/jesslearns017/md_county_sentiment

---

<p align="center">
  <strong>Built with ❤️ for Miami-Dade County Small Businesses</strong><br>
  A Passion Project | Miami Dade College 2025<br>
  <em>Created not because I had to, but because I wanted to make a difference</em>
</p>

---

**Last Updated:** November 22, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Type:** 💝 Voluntary Passion Project
