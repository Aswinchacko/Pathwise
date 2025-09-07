const mongoose = require('mongoose')

const commentSchema = new mongoose.Schema({
  text: {
    type: String,
    required: [true, 'Comment text is required'],
    trim: true
  },
  author: {
    type: String,
    required: [true, 'Author is required'],
    trim: true
  },
  authorId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  likes: {
    type: Number,
    default: 0
  }
}, {
  timestamps: true
})

const discussionSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Title is required'],
    trim: true
  },
  description: {
    type: String,
    required: [true, 'Description is required'],
    trim: true
  },
  author: {
    type: String,
    required: [true, 'Author is required'],
    trim: true
  },
  authorId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  category: {
    type: String,
    required: [true, 'Category is required'],
    enum: ['Web Development', 'Data Science', 'Career Advice', 'Development', 'Mobile Development', 'DevOps'],
    default: 'Web Development'
  },
  views: {
    type: Number,
    default: 0
  },
  likes: {
    type: Number,
    default: 0
  },
  comments: [commentSchema]
}, {
  timestamps: true,
  collection: 'discussions'
})

// Virtual for replies count
discussionSchema.virtual('replies').get(function() {
  return this.comments.length
})

// Ensure virtual fields are serialized
discussionSchema.set('toJSON', { virtuals: true })

module.exports = mongoose.model('Discussion', discussionSchema)
