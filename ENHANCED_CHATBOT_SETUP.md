# Enhanced PathWise Chatbot with Roadmap Integration

## Overview

The PathWise Chatbot has been enhanced with powerful roadmap generation capabilities that integrate with the roadmap API. Users can now generate personalized learning roadmaps directly through chat conversations and save them to their MongoDB collection.

## New Features

### 🗺️ Roadmap Generation
- **Natural Language Detection**: Automatically detects when users request roadmaps
- **Smart Goal Extraction**: Extracts learning goals from natural language
- **Personalized Roadmaps**: Generates structured learning paths based on user goals
- **Domain-Specific**: Creates roadmaps tailored to specific technology domains

### 💾 Roadmap Management
- **Save to MongoDB**: Generated roadmaps are automatically saved to user's collection
- **View & Manage**: Users can view, edit, and delete their saved roadmaps
- **Progress Tracking**: Track learning progress through structured roadmaps

### 🎨 Enhanced UI
- **Roadmap Previews**: Beautiful roadmap previews in chat messages
- **Interactive Modals**: Full roadmap view with detailed steps
- **Action Buttons**: Easy "Add to My Roadmaps" functionality
- **Responsive Design**: Works perfectly on all devices

## Setup Instructions

### 1. Prerequisites

Ensure you have the following services running:
- **MongoDB**: Database for storing chats and roadmaps
- **Roadmap API**: Service for generating roadmaps (port 8000)
- **Chatbot Service**: Enhanced chatbot service (port 8004)
- **Dashboard**: Frontend application (port 5173)

### 2. Install Dependencies

```bash
# Install chatbot service dependencies
cd chatbot_service
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `chatbot_service` directory:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/pathwise

# Service Configuration
PORT=8004
HOST=0.0.0.0

# Roadmap API Configuration
ROADMAP_API_URL=http://localhost:8000

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Start Services

#### Start Roadmap API (Terminal 1)
```bash
cd roadmap_api
python main.py
```

#### Start Chatbot Service (Terminal 2)
```bash
cd chatbot_service
python start_server.py
```

#### Start Dashboard (Terminal 3)
```bash
cd dashboard
npm run dev
```

### 5. Verify Installation

Run the integration test:

```bash
cd chatbot_service
python test_roadmap_integration.py
```

## Usage Examples

### Basic Roadmap Generation

Users can request roadmaps using natural language:

```
"Create a roadmap for becoming a full-stack developer"
"Generate a learning path for data science"
"Make a roadmap for mobile app development"
"I want to learn machine learning, create a roadmap"
"Help me plan my career in DevOps"
```

### Advanced Features

1. **Domain-Specific Roadmaps**: Specify domains for more targeted roadmaps
2. **Interactive Previews**: Click on roadmap previews to see full details
3. **Save & Manage**: Add roadmaps to your saved collection
4. **Progress Tracking**: Track your learning journey

## API Endpoints

### Chat Endpoints
- `POST /chat` - Send message and get response (now supports roadmap generation)
- `GET /chats/{user_id}` - Get user's chat history
- `POST /chats/new` - Create new chat
- `DELETE /chats/{user_id}/{chat_id}` - Delete chat

### Roadmap Endpoints
- `POST /roadmap/generate` - Generate a roadmap directly
- `GET /roadmap/user/{user_id}` - Get user's saved roadmaps
- `DELETE /roadmap/{roadmap_id}` - Delete a roadmap
- `GET /roadmap/domains` - Get available domains

## Technical Implementation

### Backend Architecture

1. **Intent Detection**: Uses TF-IDF and cosine similarity to detect roadmap requests
2. **Goal Extraction**: Regex patterns to extract learning goals from messages
3. **Roadmap Generation**: Integrates with roadmap API for personalized roadmaps
4. **MongoDB Storage**: Saves roadmaps to user's collection automatically

### Frontend Components

1. **Roadmap Preview**: Displays roadmap summaries in chat messages
2. **Interactive Modal**: Full roadmap view with detailed steps
3. **Action Buttons**: Easy roadmap management functionality
4. **Responsive Design**: Mobile-friendly interface

### Data Flow

1. User sends message requesting roadmap
2. Chatbot detects roadmap intent
3. Extracts goal from message
4. Calls roadmap API to generate roadmap
5. Displays roadmap preview in chat
6. Saves roadmap to MongoDB
7. User can view full roadmap and manage it

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/pathwise` |
| `ROADMAP_API_URL` | Roadmap API URL | `http://localhost:8000` |
| `PORT` | Chatbot service port | `8004` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:5173` |

### MongoDB Collections

- **chats**: Stores chat conversations and messages
- **roadmap**: Stores generated roadmaps (managed by roadmap API)

## Troubleshooting

### Common Issues

1. **Roadmap API Not Available**
   - Ensure roadmap API is running on port 8000
   - Check `ROADMAP_API_URL` environment variable

2. **MongoDB Connection Issues**
   - Verify MongoDB is running
   - Check `MONGODB_URI` environment variable

3. **CORS Errors**
   - Ensure frontend URL is in `CORS_ORIGINS`
   - Check both services are running

### Debug Endpoints

- `GET /health` - Check chatbot service health
- `GET /debug/storage` - Check MongoDB connection status

## Testing

### Manual Testing

1. Open the dashboard at `http://localhost:5173`
2. Navigate to the Chatbot page
3. Try requesting roadmaps:
   - "Create a roadmap for becoming a Python developer"
   - "Generate a learning path for web development"
4. Click on roadmap previews to see full details
5. Test adding roadmaps to your saved collection

### Automated Testing

```bash
# Run integration tests
cd chatbot_service
python test_roadmap_integration.py
```

## Performance Considerations

- **Caching**: Roadmap API responses are cached for better performance
- **Async Processing**: All API calls are asynchronous
- **Error Handling**: Graceful fallbacks when services are unavailable
- **Rate Limiting**: Built-in protection against excessive requests

## Security

- **Input Validation**: All user inputs are validated and sanitized
- **CORS Protection**: Proper CORS configuration for security
- **Error Handling**: No sensitive information exposed in error messages

## Future Enhancements

- **AI-Powered Suggestions**: More intelligent roadmap recommendations
- **Progress Tracking**: Visual progress indicators for learning goals
- **Collaborative Roadmaps**: Share roadmaps with others
- **Integration**: Connect with learning platforms and resources
- **Analytics**: Track learning patterns and success rates

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at `http://localhost:8004/docs`
3. Run the integration tests to verify functionality
4. Check service logs for detailed error information

---

**Note**: This enhanced chatbot service requires both the roadmap API and MongoDB to be running for full functionality. The service will gracefully degrade if these dependencies are unavailable.

