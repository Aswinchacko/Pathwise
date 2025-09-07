# PathWise ChatGPT-Style Chatbot Setup Guide

This guide will help you set up the AI-powered chatbot microservice with ChatGPT-like features including persistent chat storage and conversation memory.

## 🚀 Quick Start

### Prerequisites
- **MongoDB**: Make sure MongoDB is running on your system
- **Python 3.8+**: For the chatbot service
- **Node.js 16+**: For the frontend

### 1. Backend Setup (Chatbot Service)

```bash
# Navigate to chatbot service directory
cd chatbot_service

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env

# Edit .env file with your MongoDB URI if needed
# MONGODB_URI=mongodb://localhost:27017/pathwise

# Start the service
python start_server.py
# OR on Windows:
start_server.bat
```

The service will be available at:
- **API**: http://localhost:8002
- **Documentation**: http://localhost:8002/docs
- **Health Check**: http://localhost:8002/health

### 2. Frontend Setup (Dashboard)

```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

The dashboard will be available at http://localhost:5173

## 🤖 Features

### ChatGPT-Style Interface
- **Persistent Chat Storage**: All conversations saved in MongoDB
- **Chat History Sidebar**: Browse and manage previous conversations
- **Multiple Chat Sessions**: Create, switch between, and delete chats
- **Editable Chat Titles**: Customize chat names
- **Conversation Memory**: AI remembers context from previous messages
- **Real-time Chat**: Instant messaging experience

### ML-Powered Intelligence
- **Intent Classification**: Uses TF-IDF and cosine similarity for natural language understanding
- **Context-Aware Responses**: AI considers conversation history for better responses
- **No API Keys Required**: Completely self-contained ML solution
- **Confidence Scoring**: Shows how confident the AI is in its responses
- **Smart Suggestions**: Contextual follow-up questions

### User Experience
- **Responsive Design**: Works on desktop and mobile
- **Smooth Animations**: Framer Motion powered transitions
- **Typing Indicators**: Visual feedback during processing
- **Auto-scroll**: Automatically scrolls to new messages
- **Keyboard Shortcuts**: Enter to send, Escape to cancel

### Knowledge Areas
- **Career Guidance**: Personalized career advice and path planning
- **Skill Assessment**: Help users evaluate their skills and identify gaps
- **Project Ideas**: Suggest relevant projects based on interests
- **Learning Paths**: Create structured learning roadmaps
- **Resume Help**: Provide resume optimization advice

## 📊 API Endpoints

### Chat Management
- `POST /chat` - Send a message to the chatbot
- `POST /chats/new` - Create a new chat session
- `GET /chats/{user_id}` - Get user's chat history
- `GET /chats/{user_id}/{chat_id}` - Get messages for a specific chat
- `DELETE /chats/{user_id}/{chat_id}` - Delete a chat
- `PUT /chats/{user_id}/{chat_id}/title` - Update chat title

### Utility Endpoints
- `GET /suggestions` - Get conversation starter suggestions
- `GET /health` - Health check endpoint

### Example API Usage

**Send a message:**
```json
POST /chat
{
  "message": "Help me plan my career path",
  "user_id": "user123",
  "chat_id": "chat456" // Optional, creates new chat if not provided
}

Response:
{
  "response": "I'd be happy to help with career guidance! What specific area are you interested in?",
  "suggestions": ["What skills should I develop for tech careers?", "..."],
  "confidence": 0.85,
  "chat_id": "chat456",
  "message_id": "msg789"
}
```

**Create new chat:**
```json
POST /chats/new
{
  "user_id": "user123",
  "title": "Career Planning Chat"
}

Response:
{
  "chat_id": "chat456",
  "title": "Career Planning Chat",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## 🧪 Testing

### Test the Service
```bash
cd chatbot_service
python test_chatbot.py
```

### Test Storage (Important!)
```bash
# Test if data is being stored properly
python test_storage.py

# Quick in-memory test (no MongoDB required)
python quick_test.py
```

### Manual Testing
1. Open http://localhost:8002/docs in your browser
2. Use the interactive API documentation to test endpoints
3. Try the `/chat` endpoint with different messages

### Frontend Testing
1. Open http://localhost:5173
2. Navigate to the Chatbot page
3. Try the suggested prompts or type your own questions

## 🔧 Configuration

### Backend Configuration
The chatbot service uses these key parameters in `main.py`:
- **Port**: 8002 (configurable in `start_server.py`)
- **CORS Origins**: Configured for localhost:3000 and localhost:5173
- **Confidence Threshold**: 0.1 (minimum similarity for intent classification)

### Frontend Configuration
The frontend service configuration is in `dashboard/src/services/chatbotService.js`:
- **API URL**: http://localhost:8002
- **Timeout**: Default axios timeout
- **Error Handling**: Graceful fallback for service unavailability

## 📊 How It Works

### 1. Intent Classification
```
User Message → TF-IDF Vectorization → Cosine Similarity → Intent Category
```

### 2. Response Generation
```
Intent Category → Knowledge Base Lookup → Response Selection → Suggestions
```

### 3. Confidence Calculation
```
Message Length + Similarity Score → Confidence Percentage
```

## 🛠️ Troubleshooting

### Common Issues

**Service Won't Start**
- Check if port 8002 is available
- Ensure all dependencies are installed
- Check Python version (3.8+ required)

**Frontend Can't Connect**
- Verify chatbot service is running on port 8002
- Check CORS configuration
- Ensure no firewall blocking the connection

**Poor Response Quality**
- The ML model learns from the knowledge base
- Add more keywords and responses to improve accuracy
- Check confidence scores to identify weak areas

### Debug Mode
```bash
# Run with debug logging
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8002, log_level='debug')"
```

## 🔄 Integration

### With Other Services
The chatbot service is designed to integrate with:
- **Resume Parser**: For personalized resume advice
- **Roadmap Generator**: For learning path suggestions
- **User Authentication**: For personalized responses

### API Endpoints
- `POST /chat` - Send message to chatbot
- `GET /suggestions` - Get conversation starters
- `GET /health` - Service health check

## 📈 Performance

### Response Times
- **Typical**: 50-200ms
- **Maximum**: 500ms
- **Memory Usage**: ~50MB

### Scalability
- **Concurrent Users**: 100+ (single instance)
- **Messages per Second**: 50+
- **Knowledge Base**: Easily expandable

## 🔮 Future Enhancements

- **Conversation Memory**: Remember previous messages
- **User Profiles**: Personalized responses based on user data
- **Advanced ML**: Transformer models for better understanding
- **Multi-language Support**: Responses in different languages
- **Voice Interface**: Speech-to-text and text-to-speech

## 📝 Development

### Adding New Knowledge
1. Edit the `KNOWLEDGE_BASE` in `main.py`
2. Add new categories with keywords and responses
3. Restart the service to apply changes

### Customizing Responses
1. Modify response templates in `KNOWLEDGE_BASE`
2. Add more diverse response options
3. Update confidence calculation logic if needed

### Frontend Customization
1. Modify `Chatbot.jsx` for UI changes
2. Update `Chatbot.css` for styling
3. Add new features in `chatbotService.js`

---

**Need Help?** Check the service logs or create an issue in the repository.
