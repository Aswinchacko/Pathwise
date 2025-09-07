const mongoose = require('mongoose')

const messageSchema = new mongoose.Schema({
  role: {
    type: String,
    enum: ['user', 'assistant'],
    required: true
  },
  content: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  metadata: {
    confidence: Number,
    intent: String,
    suggestions: [String]
  }
})

const chatSchema = new mongoose.Schema({
  userId: {
    type: String,
    required: true,
    index: true
  },
  title: {
    type: String,
    default: 'New Chat'
  },
  messages: [messageSchema],
  isActive: {
    type: Boolean,
    default: true
  },
  lastMessageAt: {
    type: Date,
    default: Date.now
  },
  context: {
    currentIntent: String,
    conversationHistory: [String],
    userPreferences: {
      preferredTopics: [String],
      skillLevel: String,
      careerGoals: [String]
    }
  }
}, {
  timestamps: true,
  collection: 'chats'
})

// Index for efficient queries
chatSchema.index({ userId: 1, lastMessageAt: -1 })
chatSchema.index({ userId: 1, isActive: 1 })

// Method to add a message
chatSchema.methods.addMessage = function(role, content, metadata = {}) {
  this.messages.push({
    role,
    content,
    metadata
  })
  this.lastMessageAt = new Date()
  return this.save()
}

// Method to get conversation context
chatSchema.methods.getContext = function(maxMessages = 10) {
  const recentMessages = this.messages.slice(-maxMessages)
  return recentMessages.map(msg => ({
    role: msg.role,
    content: msg.content
  }))
}

// Method to update context
chatSchema.methods.updateContext = function(intent, suggestions = []) {
  this.context.currentIntent = intent
  this.context.conversationHistory = this.messages
    .slice(-5)
    .map(msg => msg.content)
  
  return this.save()
}

// Static method to find or create active chat
chatSchema.statics.findOrCreateActiveChat = async function(userId) {
  let chat = await this.findOne({ userId, isActive: true })
  
  if (!chat) {
    chat = new this({
      userId,
      title: 'New Chat',
      messages: [],
      context: {
        currentIntent: 'general',
        conversationHistory: [],
        userPreferences: {
          preferredTopics: [],
          skillLevel: 'beginner',
          careerGoals: []
        }
      }
    })
    await chat.save()
  }
  
  return chat
}

// Static method to get user's chat history
chatSchema.statics.getUserChats = async function(userId, limit = 20) {
  return this.find({ userId })
    .select('title lastMessageAt createdAt messages')
    .sort({ lastMessageAt: -1 })
    .limit(limit)
}

module.exports = mongoose.model('Chat', chatSchema)
