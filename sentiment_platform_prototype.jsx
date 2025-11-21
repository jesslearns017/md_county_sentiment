import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { MessageSquare, TrendingUp, AlertCircle, Send, ThumbsUp, ThumbsDown, Meh } from 'lucide-react';

// Mock data for sentiment analysis
const mockPosts = [
  { id: 1, text: "Just got my business license approved! The online portal made it so easy. Thank you Miami-Dade!", sentiment: "positive", topic: "permits", timestamp: "2h ago" },
  { id: 2, text: "Still waiting on my permit approval. It's been 3 weeks. This is frustrating.", sentiment: "negative", topic: "permits", timestamp: "5h ago" },
  { id: 3, text: "The small business grant workshop was incredibly helpful. Learned so much!", sentiment: "positive", topic: "funding", timestamp: "1d ago" },
  { id: 4, text: "Why is the business tax process so complicated? Need more guidance.", sentiment: "negative", topic: "taxes", timestamp: "1d ago" },
  { id: 5, text: "Attended the entrepreneur training session. Great resources available!", sentiment: "positive", topic: "training", timestamp: "2d ago" },
  { id: 6, text: "County website is confusing. Can't find information about health permits.", sentiment: "negative", topic: "permits", timestamp: "3d ago" },
  { id: 7, text: "Got connected with a business advisor through the county. Game changer!", sentiment: "positive", topic: "support", timestamp: "3d ago" },
  { id: 8, text: "The pandemic relief program saved my restaurant. Forever grateful.", sentiment: "positive", topic: "funding", timestamp: "4d ago" },
];

const sentimentTrend = [
  { date: 'Mon', positive: 45, negative: 20, neutral: 35 },
  { date: 'Tue', positive: 52, negative: 18, neutral: 30 },
  { date: 'Wed', positive: 48, negative: 25, neutral: 27 },
  { date: 'Thu', positive: 60, negative: 15, neutral: 25 },
  { date: 'Fri', positive: 55, negative: 22, neutral: 23 },
  { date: 'Sat', positive: 50, negative: 20, neutral: 30 },
  { date: 'Sun', positive: 58, negative: 17, neutral: 25 },
];

const topicData = [
  { name: 'Permits', value: 35, color: '#3b82f6' },
  { name: 'Funding', value: 25, color: '#10b981' },
  { name: 'Training', value: 20, color: '#f59e0b' },
  { name: 'Taxes', value: 12, color: '#ef4444' },
  { name: 'Support', value: 8, color: '#8b5cf6' },
];

const resources = {
  permits: [
    { name: "Online Permit Portal", url: "#", description: "Fast-track your business permits online" },
    { name: "Permit Assistance Program", url: "#", description: "Get help navigating the permit process" },
    { name: "Virtual Permit Workshops", url: "#", description: "Weekly sessions on permit requirements" },
  ],
  funding: [
    { name: "Small Business Grant Program", url: "#", description: "Grants up to $50,000 for eligible businesses" },
    { name: "Low-Interest Loan Program", url: "#", description: "Competitive rates for business expansion" },
    { name: "Emergency Relief Fund", url: "#", description: "Support for businesses facing hardship" },
  ],
  training: [
    { name: "Entrepreneur Boot Camp", url: "#", description: "12-week intensive business training" },
    { name: "Digital Marketing Workshop", url: "#", description: "Learn to market your business online" },
    { name: "Financial Planning Sessions", url: "#", description: "Master your business finances" },
  ],
  taxes: [
    { name: "Business Tax Calculator", url: "#", description: "Estimate your tax obligations" },
    { name: "Tax Filing Assistance", url: "#", description: "Free help with business tax returns" },
    { name: "Tax Credit Information", url: "#", description: "Discover available tax incentives" },
  ],
  support: [
    { name: "Business Advisor Matching", url: "#", description: "Get paired with an expert advisor" },
    { name: "Mentorship Program", url: "#", description: "Connect with successful entrepreneurs" },
    { name: "24/7 Business Hotline", url: "#", description: "Call anytime for quick answers" },
  ],
};

const SmallBusinessPlatform = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [chatMessages, setChatMessages] = useState([
    { sender: 'bot', text: "Hi! 👋 I'm your County resource assistant. What do you need help with today?" }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const getSentimentIcon = (sentiment) => {
    switch(sentiment) {
      case 'positive': return <ThumbsUp className="text-green-500" size={16} />;
      case 'negative': return <ThumbsDown className="text-red-500" size={16} />;
      default: return <Meh className="text-gray-500" size={16} />;
    }
  };

  const analyzeMessage = (message) => {
    const lowerMsg = message.toLowerCase();
    
    // Simple keyword matching for demo
    if (lowerMsg.includes('permit') || lowerMsg.includes('license')) {
      return { topic: 'permits', keywords: ['permit', 'license'] };
    } else if (lowerMsg.includes('grant') || lowerMsg.includes('fund') || lowerMsg.includes('loan')) {
      return { topic: 'funding', keywords: ['grant', 'funding', 'loan'] };
    } else if (lowerMsg.includes('train') || lowerMsg.includes('learn') || lowerMsg.includes('workshop')) {
      return { topic: 'training', keywords: ['training', 'workshop'] };
    } else if (lowerMsg.includes('tax')) {
      return { topic: 'taxes', keywords: ['tax'] };
    } else {
      return { topic: 'support', keywords: ['help', 'support'] };
    }
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    // Add user message
    setChatMessages(prev => [...prev, { sender: 'user', text: inputMessage }]);
    setInputMessage('');
    setIsTyping(true);

    // Analyze and respond
    setTimeout(() => {
      const analysis = analyzeMessage(inputMessage);
      const recommendations = resources[analysis.topic];
      
      const responseText = `Great question! Based on what you're looking for, here are some resources that can help:`;
      
      setChatMessages(prev => [...prev, 
        { sender: 'bot', text: responseText },
        { sender: 'bot', recommendations: recommendations }
      ]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const DashboardView = () => (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Overall Sentiment</p>
              <p className="text-3xl font-bold text-green-600">62%</p>
              <p className="text-sm text-gray-600">Positive</p>
            </div>
            <ThumbsUp className="text-green-500" size={40} />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Mentions</p>
              <p className="text-3xl font-bold text-blue-600">1,247</p>
              <p className="text-sm text-gray-600">This week</p>
            </div>
            <TrendingUp className="text-blue-500" size={40} />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Top Issue</p>
              <p className="text-2xl font-bold text-orange-600">Permits</p>
              <p className="text-sm text-gray-600">35% of discussions</p>
            </div>
            <AlertCircle className="text-orange-500" size={40} />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Sentiment Trend (7 Days)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={sentimentTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="positive" stroke="#10b981" strokeWidth={2} />
              <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="neutral" stroke="#6b7280" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Topics Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={topicData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {topicData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Posts */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Social Media Posts</h3>
        <div className="space-y-4">
          {mockPosts.map(post => (
            <div key={post.id} className="border-l-4 border-blue-500 pl-4 py-2 hover:bg-gray-50 transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="text-gray-800">{post.text}</p>
                  <div className="flex items-center gap-3 mt-2 text-sm text-gray-500">
                    <span className="flex items-center gap-1">
                      {getSentimentIcon(post.sentiment)}
                      {post.sentiment}
                    </span>
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {post.topic}
                    </span>
                    <span>{post.timestamp}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const ChatbotView = () => (
    <div className="bg-white rounded-lg shadow h-[600px] flex flex-col">
      <div className="bg-blue-600 text-white p-4 rounded-t-lg">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <MessageSquare size={24} />
          Resource Recommender Assistant
        </h3>
        <p className="text-sm text-blue-100">Ask me about permits, funding, training, or support!</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatMessages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.recommendations ? (
              <div className="bg-gray-50 rounded-lg p-4 max-w-md space-y-3">
                {msg.recommendations.map((resource, ridx) => (
                  <div key={ridx} className="bg-white border border-gray-200 rounded p-3 hover:shadow-md transition">
                    <h4 className="font-semibold text-blue-600">{resource.name}</h4>
                    <p className="text-sm text-gray-600 mt-1">{resource.description}</p>
                    <button className="text-xs text-blue-500 hover:underline mt-2">
                      Learn more →
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className={`rounded-lg px-4 py-2 max-w-md ${
                msg.sender === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {msg.text}
              </div>
            )}
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="border-t p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about business resources..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSendMessage}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
          >
            <Send size={18} />
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          💡 Try asking: "I need help with permits" or "How can I get funding?"
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🏢 Small Business Sentiment Intelligence
          </h1>
          <p className="text-gray-600">
            AI-Powered Platform for Miami-Dade County
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-lg mb-6">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex-1 py-4 px-6 font-semibold transition ${
                activeTab === 'dashboard'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              📊 Sentiment Dashboard
            </button>
            <button
              onClick={() => setActiveTab('chatbot')}
              className={`flex-1 py-4 px-6 font-semibold transition ${
                activeTab === 'chatbot'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              💬 Resource Recommender
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="transition-all duration-300">
          {activeTab === 'dashboard' ? <DashboardView /> : <ChatbotView />}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600 text-sm">
          <p>🎯 MVP Prototype - Built for MDC Capstone Project</p>
          <p className="mt-1">Combining Projects #2 (Sentiment Analysis) + #8 (Resource Recommender)</p>
        </div>
      </div>
    </div>
  );
};

export default SmallBusinessPlatform;