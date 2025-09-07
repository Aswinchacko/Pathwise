from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import re
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from datetime import datetime
import pymongo
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI(title="PathWise Chatbot Service", version="1.0.0")

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/pathwise")
USE_MONGODB = False
chats_collection = None

try:
    client = MongoClient(MONGODB_URI)
    # Test the connection
    client.admin.command('ping')
    db = client.pathwise
    chats_collection = db.chats
    USE_MONGODB = True
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("🔄 Using in-memory storage as fallback")
    USE_MONGODB = False

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"
    chat_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str] = []
    confidence: float = 0.0
    chat_id: str
    message_id: str

class ChatHistory(BaseModel):
    chat_id: str
    title: str
    last_message_at: datetime
    message_count: int

class NewChatRequest(BaseModel):
    user_id: str
    title: Optional[str] = "New Chat"

# Knowledge base for career guidance
KNOWLEDGE_BASE = {
    "career_guidance": {
        "keywords": ["career", "job", "profession", "work", "employment", "career path", "future"],
        "responses": [
            "I'd be happy to help with career guidance! What specific area are you interested in? Are you looking to start a new career, switch fields, or advance in your current role?",
            "Career guidance is one of my specialties! Tell me about your current situation - are you a student, recent graduate, or looking to make a career change?",
            "Let's explore your career options together! What skills do you currently have, and what type of work environment appeals to you most?"
        ]
    },
    "skill_assessment": {
        "keywords": ["skills", "ability", "competency", "assessment", "evaluate", "strengths", "weaknesses"],
        "responses": [
            "I can help you assess your skills! What field are you interested in? I can help identify your strengths and areas for improvement.",
            "Skill assessment is crucial for career growth. Tell me about your current technical skills, soft skills, and what you'd like to develop further.",
            "Let's evaluate your skills together! What programming languages, tools, or technologies are you familiar with?"
        ]
    },
    "project_ideas": {
        "keywords": ["project", "portfolio", "build", "create", "develop", "practice", "ideas"],
        "responses": [
            "Great question! Project ideas depend on your interests and skill level. What programming languages or technologies are you comfortable with?",
            "I love helping with project ideas! Are you looking for beginner, intermediate, or advanced projects? What's your main area of interest?",
            "Let's brainstorm some project ideas! Tell me about your current skill level and what type of projects excite you most."
        ]
    },
    "learning_path": {
        "keywords": ["learn", "study", "course", "tutorial", "education", "training", "roadmap"],
        "responses": [
            "I can help create a learning path for you! What specific technology or skill do you want to master?",
            "Learning paths are essential for structured growth. What's your current level, and what's your target goal?",
            "Let's design a learning roadmap! Tell me about your learning style and how much time you can dedicate daily."
        ]
    },
    "resume_help": {
        "keywords": ["resume", "cv", "application", "interview", "job search", "hiring"],
        "responses": [
            "I can help with resume advice! What type of position are you applying for, and what's your experience level?",
            "Resume optimization is key to landing interviews. Tell me about your background and the roles you're targeting.",
            "Let's improve your resume! What specific sections would you like help with - formatting, content, or keywords?"
        ]
    },
    "general": {
        "keywords": ["hello", "hi", "help", "what", "how", "why", "when", "where"],
        "responses": [
            "Hello! I'm your AI career assistant. I can help with career guidance, skill assessment, project ideas, learning paths, and resume advice. What would you like to know?",
            "Hi there! I'm here to help you with your career journey. Feel free to ask me anything about career development, skills, or professional growth!",
            "Welcome! I specialize in career guidance and professional development. How can I assist you today?"
        ]
    }
}

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
knowledge_texts = []
knowledge_labels = []

# Prepare training data
for category, data in KNOWLEDGE_BASE.items():
    for keyword in data["keywords"]:
        knowledge_texts.append(keyword)
        knowledge_labels.append(category)

# Fit the vectorizer
if knowledge_texts:
    vectorizer.fit(knowledge_texts)

def classify_intent(message: str) -> str:
    """Classify user intent using TF-IDF and cosine similarity"""
    if not knowledge_texts:
        return "general"
    
    message_vector = vectorizer.transform([message.lower()])
    similarities = []
    
    for i, text in enumerate(knowledge_texts):
        text_vector = vectorizer.transform([text])
        similarity = cosine_similarity(message_vector, text_vector)[0][0]
        similarities.append((similarity, knowledge_labels[i]))
    
    # Get the best match
    similarities.sort(key=lambda x: x[0], reverse=True)
    best_match = similarities[0]
    
    # Return the category if similarity is above threshold
    if best_match[0] > 0.1:
        return best_match[1]
    return "general"

# In-memory storage fallback
in_memory_chats = {}

# MongoDB helper functions
async def get_or_create_chat(user_id: str, chat_id: Optional[str] = None) -> Dict[str, Any]:
    """Get existing chat or create new one"""
    if not USE_MONGODB:
        # Use in-memory storage
        if chat_id and chat_id in in_memory_chats:
            return in_memory_chats[chat_id]
        
        # Create new chat in memory
        new_chat = {
            "_id": f"chat_{len(in_memory_chats) + 1}",
            "userId": user_id,
            "title": "New Chat",
            "messages": [],
            "isActive": True,
            "lastMessageAt": datetime.now(),
            "context": {
                "currentIntent": "general",
                "conversationHistory": [],
                "userPreferences": {
                    "preferredTopics": [],
                    "skillLevel": "beginner",
                    "careerGoals": []
                }
            },
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
        }
        in_memory_chats[new_chat["_id"]] = new_chat
        return new_chat
    
    # MongoDB storage
    if chat_id:
        try:
            chat = chats_collection.find_one({"_id": ObjectId(chat_id), "userId": user_id})
            if chat:
                chat["_id"] = str(chat["_id"])
                return chat
        except:
            pass
    
    # Create new chat
    new_chat = {
        "userId": user_id,
        "title": "New Chat",
        "messages": [],
        "isActive": True,
        "lastMessageAt": datetime.now(),
        "context": {
            "currentIntent": "general",
            "conversationHistory": [],
            "userPreferences": {
                "preferredTopics": [],
                "skillLevel": "beginner",
                "careerGoals": []
            }
        },
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
    
    result = chats_collection.insert_one(new_chat)
    new_chat["_id"] = str(result.inserted_id)
    return new_chat

async def save_message(chat_id: str, role: str, content: str, metadata: Dict[str, Any] = None) -> str:
    """Save message to chat"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now(),
        "metadata": metadata or {}
    }
    
    if not USE_MONGODB:
        # In-memory storage
        if chat_id in in_memory_chats:
            in_memory_chats[chat_id]["messages"].append(message)
            in_memory_chats[chat_id]["lastMessageAt"] = datetime.now()
            in_memory_chats[chat_id]["updatedAt"] = datetime.now()
        return str(message["timestamp"])
    
    # MongoDB storage
    try:
        chats_collection.update_one(
            {"_id": ObjectId(chat_id)},
            {
                "$push": {"messages": message},
                "$set": {"lastMessageAt": datetime.now(), "updatedAt": datetime.now()}
            }
        )
    except:
        # Fallback to in-memory if MongoDB fails
        if chat_id in in_memory_chats:
            in_memory_chats[chat_id]["messages"].append(message)
            in_memory_chats[chat_id]["lastMessageAt"] = datetime.now()
            in_memory_chats[chat_id]["updatedAt"] = datetime.now()
    
    return str(message["timestamp"])

async def get_conversation_context(chat_id: str, max_messages: int = 10) -> List[Dict[str, str]]:
    """Get recent conversation context"""
    if not USE_MONGODB:
        # In-memory storage
        if chat_id in in_memory_chats:
            recent_messages = in_memory_chats[chat_id].get("messages", [])[-max_messages:]
            return [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]
        return []
    
    # MongoDB storage
    try:
        chat = chats_collection.find_one({"_id": ObjectId(chat_id)})
        if not chat:
            return []
        
        recent_messages = chat.get("messages", [])[-max_messages:]
        return [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]
    except:
        # Fallback to in-memory
        if chat_id in in_memory_chats:
            recent_messages = in_memory_chats[chat_id].get("messages", [])[-max_messages:]
            return [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]
        return []

def generate_response(intent: str, message: str, context: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """Generate response based on classified intent and conversation context"""
    category_data = KNOWLEDGE_BASE.get(intent, KNOWLEDGE_BASE["general"])
    
    # Use context to make responses more relevant
    context_text = ""
    if context:
        recent_user_messages = [msg["content"] for msg in context[-3:] if msg["role"] == "user"]
        if recent_user_messages:
            context_text = " ".join(recent_user_messages)
    
    # Select a response that considers context
    responses = category_data["responses"]
    if context_text and len(context) > 1:
        # Try to find a response that relates to the conversation
        for response in responses:
            if any(word in response.lower() for word in context_text.lower().split()[:5]):
                selected_response = response
                break
        else:
            selected_response = responses[0]
    else:
        import random
        selected_response = random.choice(responses)
    
    # Generate contextual suggestions
    suggestions = generate_contextual_suggestions(intent, context_text)
    
    # Calculate confidence based on similarity and context
    base_confidence = min(0.9, max(0.3, len(message.split()) / 10))
    context_boost = 0.1 if context_text else 0
    confidence = min(0.95, base_confidence + context_boost)
    
    return {
        "response": selected_response,
        "suggestions": suggestions[:3],
        "confidence": confidence
    }

def generate_contextual_suggestions(intent: str, context: str = "") -> List[str]:
    """Generate suggestions based on intent and conversation context"""
    base_suggestions = {
        "career_guidance": [
            "What skills should I develop for tech careers?",
            "How do I transition from non-tech to tech?",
            "What are the highest paying tech roles?",
            "What career paths are available in software development?",
            "How do I choose between different tech specializations?"
        ],
        "skill_assessment": [
            "How do I assess my programming skills?",
            "What soft skills are most important?",
            "How can I identify skill gaps?",
            "What's the best way to practice coding?",
            "How do I measure my progress in learning?"
        ],
        "project_ideas": [
            "What projects should I build for my portfolio?",
            "How do I choose the right project complexity?",
            "What makes a project stand out to employers?",
            "What are some beginner-friendly project ideas?",
            "How do I document my projects effectively?"
        ],
        "learning_path": [
            "How do I create a learning roadmap?",
            "What's the best way to learn programming?",
            "How long does it take to learn a new skill?",
            "What resources should I use for learning?",
            "How do I stay motivated while learning?"
        ],
        "resume_help": [
            "How do I write a tech resume?",
            "What keywords should I include?",
            "How do I format my resume for ATS?",
            "What projects should I highlight?",
            "How do I write effective bullet points?"
        ]
    }
    
    suggestions = base_suggestions.get(intent, [
        "Tell me about career guidance",
        "Help me assess my skills",
        "Suggest some project ideas"
    ])
    
    # Filter suggestions based on context if available
    if context:
        context_words = set(context.lower().split())
        filtered_suggestions = []
        for suggestion in suggestions:
            if any(word in suggestion.lower() for word in context_words):
                filtered_suggestions.append(suggestion)
        
        if filtered_suggestions:
            suggestions = filtered_suggestions
    
    return suggestions

@app.get("/")
async def root():
    return {"message": "PathWise Chatbot Service is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chatbot"}

@app.get("/debug/storage")
async def debug_storage():
    """Debug endpoint to check storage status"""
    if not USE_MONGODB:
        return {
            "storage_type": "in_memory",
            "total_chats": len(in_memory_chats),
            "chats": list(in_memory_chats.keys())
        }
    else:
        try:
            total_chats = chats_collection.count_documents({})
            return {
                "storage_type": "mongodb",
                "total_chats": total_chats,
                "connection": "active"
            }
        except Exception as e:
            return {
                "storage_type": "mongodb",
                "error": str(e),
                "connection": "failed"
            }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        # Get or create chat
        chat = await get_or_create_chat(message.user_id, message.chat_id)
        chat_id = str(chat["_id"])
        
        # Get conversation context
        context = await get_conversation_context(chat_id)
        
        # Classify the user's intent
        intent = classify_intent(message.message)
        
        # Generate response with context
        result = generate_response(intent, message.message, context)
        
        # Save user message
        user_message_id = await save_message(
            chat_id, 
            "user", 
            message.message, 
            {"intent": intent, "confidence": result["confidence"]}
        )
        
        # Save bot response
        bot_message_id = await save_message(
            chat_id, 
            "assistant", 
            result["response"], 
            {
                "intent": intent, 
                "confidence": result["confidence"],
                "suggestions": result["suggestions"]
            }
        )
        
        # Update chat title if it's the first message
        if len(chat.get("messages", [])) == 0:
            title = message.message[:50] + "..." if len(message.message) > 50 else message.message
            chats_collection.update_one(
                {"_id": chat_id},
                {"$set": {"title": title}}
            )
        
        return ChatResponse(
            response=result["response"],
            suggestions=result["suggestions"],
            confidence=result["confidence"],
            chat_id=chat_id,
            message_id=bot_message_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/suggestions")
async def get_suggestions():
    """Get general conversation starters"""
    return {
        "suggestions": [
            "Help me plan my career path",
            "Assess my current skills",
            "Suggest project ideas for my portfolio",
            "Create a learning roadmap for Python",
            "Review my resume for tech jobs",
            "What are the best programming languages to learn?",
            "How do I prepare for technical interviews?",
            "What soft skills are important for developers?"
        ]
    }

@app.post("/chats/new")
async def create_new_chat(request: NewChatRequest):
    """Create a new chat session"""
    try:
        chat = await get_or_create_chat(request.user_id)
        return {
            "chat_id": str(chat["_id"]),
            "title": chat["title"],
            "created_at": chat["createdAt"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat: {str(e)}")

@app.get("/chats/{user_id}")
async def get_user_chats(user_id: str, limit: int = 20):
    """Get user's chat history"""
    try:
        if not USE_MONGODB:
            # In-memory storage
            user_chats = [chat for chat in in_memory_chats.values() if chat["userId"] == user_id]
            user_chats.sort(key=lambda x: x["lastMessageAt"], reverse=True)
            user_chats = user_chats[:limit]
            
            chat_history = []
            for chat in user_chats:
                chat_history.append(ChatHistory(
                    chat_id=chat["_id"],
                    title=chat["title"],
                    last_message_at=chat["lastMessageAt"],
                    message_count=len(chat.get("messages", []))
                ))
            
            return {"chats": chat_history}
        
        # MongoDB storage
        chats = list(chats_collection.find(
            {"userId": user_id},
            {"title": 1, "lastMessageAt": 1, "createdAt": 1, "messages": {"$slice": 1}}
        ).sort("lastMessageAt", -1).limit(limit))
        
        chat_history = []
        for chat in chats:
            chat_history.append(ChatHistory(
                chat_id=str(chat["_id"]),
                title=chat["title"],
                last_message_at=chat["lastMessageAt"],
                message_count=len(chat.get("messages", []))
            ))
        
        return {"chats": chat_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

@app.get("/chats/{user_id}/{chat_id}")
async def get_chat_messages(user_id: str, chat_id: str):
    """Get messages for a specific chat"""
    try:
        if not USE_MONGODB:
            # In-memory storage
            if chat_id not in in_memory_chats or in_memory_chats[chat_id]["userId"] != user_id:
                raise HTTPException(status_code=404, detail="Chat not found")
            
            chat = in_memory_chats[chat_id]
            messages = []
            for msg in chat.get("messages", []):
                messages.append({
                    "id": str(msg["timestamp"]),
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"],
                    "metadata": msg.get("metadata", {})
                })
            
            return {
                "chat_id": chat_id,
                "title": chat["title"],
                "messages": messages
            }
        
        # MongoDB storage
        try:
            chat = chats_collection.find_one({"_id": ObjectId(chat_id), "userId": user_id})
        except:
            chat = None
            
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        messages = []
        for msg in chat.get("messages", []):
            messages.append({
                "id": str(msg["timestamp"]),
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["timestamp"],
                "metadata": msg.get("metadata", {})
            })
        
        return {
            "chat_id": chat_id,
            "title": chat["title"],
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@app.delete("/chats/{user_id}/{chat_id}")
async def delete_chat(user_id: str, chat_id: str):
    """Delete a chat"""
    try:
        result = chats_collection.delete_one({"_id": chat_id, "userId": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        return {"message": "Chat deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")

@app.put("/chats/{user_id}/{chat_id}/title")
async def update_chat_title(user_id: str, chat_id: str, title: str):
    """Update chat title"""
    try:
        result = chats_collection.update_one(
            {"_id": chat_id, "userId": user_id},
            {"$set": {"title": title, "updatedAt": datetime.now()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        return {"message": "Title updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating title: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
