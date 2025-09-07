# PathWise Chatbot Service

AI-powered chatbot microservice for career guidance and professional development.

## Features

- **ML-Powered Intent Classification**: Uses TF-IDF and cosine similarity for natural language understanding
- **Career Guidance**: Personalized advice for career paths and transitions
- **Skill Assessment**: Help users evaluate their skills and identify gaps
- **Project Ideas**: Suggest relevant projects based on user interests
- **Learning Paths**: Create structured learning roadmaps
- **Resume Help**: Provide resume optimization advice
- **No API Keys Required**: Completely self-contained ML solution

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Service**
   ```bash
   python start_server.py
   ```

3. **Access the Service**
   - API: http://localhost:8002
   - Documentation: http://localhost:8002/docs
   - Health Check: http://localhost:8002/health

## API Endpoints

### POST /chat
Send a message to the chatbot.

**Request:**
```json
{
  "message": "Help me plan my career path",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "response": "I'd be happy to help with career guidance! What specific area are you interested in?",
  "suggestions": [
    "What skills should I develop for tech careers?",
    "How do I transition from non-tech to tech?",
    "What are the highest paying tech roles?"
  ],
  "confidence": 0.85
}
```

### GET /suggestions
Get conversation starter suggestions.

### GET /health
Health check endpoint.

## How It Works

1. **Intent Classification**: Uses TF-IDF vectorization and cosine similarity to classify user messages into categories
2. **Response Generation**: Selects appropriate responses based on classified intent
3. **Suggestion System**: Provides relevant follow-up questions based on the conversation context
4. **Confidence Scoring**: Calculates confidence levels for responses

## Knowledge Base

The chatbot is trained on a comprehensive knowledge base covering:
- Career guidance and transitions
- Skill assessment and development
- Project ideas and portfolio building
- Learning paths and education
- Resume optimization and job search
- General professional development

## Integration

This service is designed to integrate with the PathWise dashboard frontend. The frontend sends user messages and receives structured responses with suggestions for continued conversation.
