const express = require('express')
const Discussion = require('../models/Discussion')
const auth = require('../middleware/auth')

const router = express.Router()

// GET /api/discussions - Get all discussions
router.get('/', async (req, res) => {
  try {
    const { category } = req.query
    const filter = category ? { category } : {}
    
    const discussions = await Discussion.find(filter)
      .populate('authorId', 'firstName lastName email')
      .sort({ createdAt: -1 })
      .lean()
    
    // Format the response to match frontend expectations
    const formattedDiscussions = discussions.map(discussion => ({
      id: discussion._id,
      title: discussion.title,
      description: discussion.description,
      author: discussion.author,
      replies: discussion.replies,
      views: discussion.views,
      category: discussion.category,
      likes: discussion.likes,
      comments: discussion.comments || [],
      createdAt: discussion.createdAt
    }))
    
    res.json(formattedDiscussions)
  } catch (error) {
    console.error('Error fetching discussions:', error)
    res.status(500).json({ error: 'Failed to fetch discussions' })
  }
})

// GET /api/discussions/:id - Get single discussion
router.get('/:id', async (req, res) => {
  try {
    const discussion = await Discussion.findById(req.params.id)
      .populate('authorId', 'firstName lastName email')
      .lean()
    
    if (!discussion) {
      return res.status(404).json({ error: 'Discussion not found' })
    }
    
    // Increment views
    await Discussion.findByIdAndUpdate(req.params.id, { $inc: { views: 1 } })
    
    const formattedDiscussion = {
      id: discussion._id,
      title: discussion.title,
      description: discussion.description,
      author: discussion.author,
      replies: discussion.comments?.length || 0,
      views: discussion.views + 1,
      category: discussion.category,
      likes: discussion.likes,
      comments: discussion.comments || [],
      createdAt: discussion.createdAt
    }
    
    res.json(formattedDiscussion)
  } catch (error) {
    console.error('Error fetching discussion:', error)
    res.status(500).json({ error: 'Failed to fetch discussion' })
  }
})

// POST /api/discussions - Create new discussion
router.post('/', auth, async (req, res) => {
  try {
    const { title, description, category } = req.body
    
    if (!title || !description) {
      return res.status(400).json({ error: 'Title and description are required' })
    }
    
    const discussion = new Discussion({
      title,
      description,
      category: category || 'Web Development',
      author: req.user.firstName + ' ' + req.user.lastName,
      authorId: req.user._id
    })
    
    await discussion.save()
    
    const formattedDiscussion = {
      id: discussion._id,
      title: discussion.title,
      description: discussion.description,
      author: discussion.author,
      replies: 0,
      views: 0,
      category: discussion.category,
      likes: 0,
      comments: [],
      createdAt: discussion.createdAt
    }
    
    res.status(201).json(formattedDiscussion)
  } catch (error) {
    console.error('Error creating discussion:', error)
    res.status(500).json({ error: 'Failed to create discussion' })
  }
})

// POST /api/discussions/:id/comments - Add comment to discussion
router.post('/:id/comments', auth, async (req, res) => {
  try {
    const { text } = req.body
    
    if (!text) {
      return res.status(400).json({ error: 'Comment text is required' })
    }
    
    const discussion = await Discussion.findById(req.params.id)
    if (!discussion) {
      return res.status(404).json({ error: 'Discussion not found' })
    }
    
    const comment = {
      text,
      author: req.user.firstName + ' ' + req.user.lastName,
      authorId: req.user._id
    }
    
    discussion.comments.push(comment)
    await discussion.save()
    
    const newComment = discussion.comments[discussion.comments.length - 1]
    res.status(201).json({
      id: newComment._id,
      text: newComment.text,
      author: newComment.author,
      createdAt: newComment.createdAt,
      likes: newComment.likes
    })
  } catch (error) {
    console.error('Error adding comment:', error)
    res.status(500).json({ error: 'Failed to add comment' })
  }
})

// PUT /api/discussions/:id/like - Like a discussion
router.put('/:id/like', auth, async (req, res) => {
  try {
    const discussion = await Discussion.findByIdAndUpdate(
      req.params.id,
      { $inc: { likes: 1 } },
      { new: true }
    )
    
    if (!discussion) {
      return res.status(404).json({ error: 'Discussion not found' })
    }
    
    res.json({ likes: discussion.likes })
  } catch (error) {
    console.error('Error liking discussion:', error)
    res.status(500).json({ error: 'Failed to like discussion' })
  }
})

module.exports = router
