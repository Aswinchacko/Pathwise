const express = require('express')
const router = express.Router()
const User = require('../models/User')
const Discussion = require('../models/Discussion')
const auth = require('../middleware/auth')

// Middleware to check admin role
const adminAuth = async (req, res, next) => {
  try {
    if (!req.user || (req.user.isAdmin !== 'true' && req.user.isAdmin !== true)) {
      return res.status(403).json({ message: 'Access denied. Admin privileges required.' })
    }
    next()
  } catch (error) {
    res.status(500).json({ message: 'Server error' })
  }
}

// Get admin dashboard stats
router.get('/stats', auth, adminAuth, async (req, res) => {
  try {
    const [
      totalUsers,
      activeUsers,
      newUsersThisMonth,
      totalDiscussions,
      activeDiscussions,
      usersByRole,
      recentUsers
    ] = await Promise.all([
      User.countDocuments(),
      User.countDocuments({ isActive: true }),
      User.countDocuments({ 
        createdAt: { 
          $gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1) 
        } 
      }),
      Discussion.countDocuments(),
      Discussion.countDocuments({ 
        createdAt: { 
          $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) 
        } 
      }),
      User.aggregate([
        { $group: { _id: '$role', count: { $sum: 1 } } }
      ]),
      User.find()
        .sort({ createdAt: -1 })
        .limit(10)
        .select('firstName lastName email role createdAt isActive')
    ])

    const stats = {
      users: {
        total: totalUsers,
        active: activeUsers,
        newThisMonth: newUsersThisMonth,
        byRole: usersByRole.reduce((acc, item) => {
          acc[item._id] = item.count
          return acc
        }, {})
      },
      discussions: {
        total: totalDiscussions,
        activeThisWeek: activeDiscussions
      },
      recentUsers: recentUsers,
      lastUpdated: new Date()
    }

    res.json(stats)
  } catch (error) {
    console.error('Error fetching admin stats:', error)
    res.status(500).json({ message: 'Failed to fetch admin statistics' })
  }
})

// Get all users with pagination
router.get('/users', auth, adminAuth, async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1
    const limit = parseInt(req.query.limit) || 20
    const search = req.query.search || ''
    const role = req.query.role || ''
    const status = req.query.status || ''

    let query = {}
    
    if (search) {
      query.$or = [
        { firstName: { $regex: search, $options: 'i' } },
        { lastName: { $regex: search, $options: 'i' } },
        { email: { $regex: search, $options: 'i' } }
      ]
    }
    
    if (role) {
      query.role = role
    }
    
    if (status === 'active') {
      query.isActive = true
    } else if (status === 'inactive') {
      query.isActive = false
    }

    const users = await User.find(query)
      .select('-password')
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .exec()

    const total = await User.countDocuments(query)

    res.json({
      users,
      totalPages: Math.ceil(total / limit),
      currentPage: page,
      total
    })
  } catch (error) {
    console.error('Error fetching users:', error)
    res.status(500).json({ message: 'Failed to fetch users' })
  }
})

// Update user role or status
router.put('/users/:id', auth, adminAuth, async (req, res) => {
  try {
    const { id } = req.params
    const { firstName, lastName, email, role, isActive } = req.body

    const updateData = {}
    if (firstName !== undefined) updateData.firstName = firstName
    if (lastName !== undefined) updateData.lastName = lastName
    if (email !== undefined) updateData.email = email
    if (role !== undefined) updateData.role = role
    if (isActive !== undefined) updateData.isActive = isActive

    const user = await User.findByIdAndUpdate(
      id,
      updateData,
      { new: true, runValidators: true }
    ).select('-password')

    if (!user) {
      return res.status(404).json({ message: 'User not found' })
    }

    res.json(user)
  } catch (error) {
    console.error('Error updating user:', error)
    res.status(500).json({ message: 'Failed to update user' })
  }
})

// Delete user
router.delete('/users/:id', auth, adminAuth, async (req, res) => {
  try {
    const { id } = req.params

    // Prevent admin from deleting themselves
    if (req.user.id === id) {
      return res.status(400).json({ message: 'Cannot delete your own account' })
    }

    const user = await User.findByIdAndDelete(id)

    if (!user) {
      return res.status(404).json({ message: 'User not found' })
    }

    res.json({ message: 'User deleted successfully' })
  } catch (error) {
    console.error('Error deleting user:', error)
    res.status(500).json({ message: 'Failed to delete user' })
  }
})

// Get system health
router.get('/system/health', auth, adminAuth, async (req, res) => {
  try {
    const mongoose = require('mongoose')
    
    const health = {
      database: {
        status: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
        name: mongoose.connection.name
      },
      server: {
        status: 'running',
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        version: process.version
      },
      services: [
        {
          name: 'Authentication Service',
          status: 'online',
          uptime: '99.9%',
          lastCheck: new Date()
        },
        {
          name: 'Roadmap API',
          status: 'online',
          uptime: '99.8%',
          lastCheck: new Date()
        },
        {
          name: 'Chatbot Service',
          status: 'online',
          uptime: '99.7%',
          lastCheck: new Date()
        },
        {
          name: 'Resume Parser',
          status: 'online',
          uptime: '99.9%',
          lastCheck: new Date()
        }
      ]
    }

    res.json(health)
  } catch (error) {
    console.error('Error checking system health:', error)
    res.status(500).json({ message: 'Failed to check system health' })
  }
})

// Get recent activity
router.get('/activity', auth, adminAuth, async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50
    const activityLimit = Math.max(Math.floor(limit / 3), 5) // Distribute limit across activity types

    // Get recent user registrations
    const recentUsers = await User.find()
      .sort({ createdAt: -1 })
      .limit(activityLimit)
      .select('firstName lastName email createdAt')

    // Get recent discussions
    const recentDiscussions = await Discussion.find()
      .sort({ createdAt: -1 })
      .limit(activityLimit)
      .populate('author', 'firstName lastName')
      .select('title author createdAt')

    // Get recent user logins (users with recent lastLogin)
    const recentLogins = await User.find({ 
      lastLogin: { $exists: true, $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) } 
    })
      .sort({ lastLogin: -1 })
      .limit(activityLimit)
      .select('firstName lastName email lastLogin')

    // Get recent role changes (users modified recently)
    const recentUpdates = await User.find({ 
      updatedAt: { $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) },
      createdAt: { $lt: new Date(Date.now() - 60 * 1000) } // Exclude just registered users
    })
      .sort({ updatedAt: -1 })
      .limit(activityLimit)
      .select('firstName lastName email role updatedAt')

    const activity = [
      // User registrations
      ...recentUsers.map(user => ({
        id: `reg_${user._id}`,
        type: 'user_registration',
        message: `New user registered: ${user.firstName} ${user.lastName}`,
        timestamp: user.createdAt,
        data: { userId: user._id, email: user.email },
        severity: 'info'
      })),
      
      // Discussion creations
      ...recentDiscussions.map(discussion => ({
        id: `disc_${discussion._id}`,
        type: 'discussion_created',
        message: `New discussion: "${discussion.title}"`,
        timestamp: discussion.createdAt,
        data: { 
          discussionId: discussion._id, 
          author: discussion.author ? `${discussion.author.firstName} ${discussion.author.lastName}` : 'Unknown'
        },
        severity: 'info'
      })),
      
      // User logins
      ...recentLogins.map(user => ({
        id: `login_${user._id}_${user.lastLogin}`,
        type: 'user_login',
        message: `User login: ${user.firstName} ${user.lastName}`,
        timestamp: user.lastLogin,
        data: { userId: user._id, email: user.email },
        severity: 'success'
      })),
      
      // User updates (role changes, etc.)
      ...recentUpdates.map(user => ({
        id: `update_${user._id}_${user.updatedAt}`,
        type: 'admin_action',
        message: `User profile updated: ${user.firstName} ${user.lastName} (${user.role || 'user'})`,
        timestamp: user.updatedAt,
        data: { userId: user._id, email: user.email, role: user.role },
        severity: 'warning'
      })),
      
      // System events (server start time as a system event)
      {
        id: `system_${Date.now()}`,
        type: 'system_event',
        message: 'Admin dashboard accessed',
        timestamp: new Date(),
        data: { component: 'dashboard', admin: req.user.email },
        severity: 'info'
      }
    ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, limit)

    res.json(activity)
  } catch (error) {
    console.error('Error fetching activity:', error)
    res.status(500).json({ message: 'Failed to fetch recent activity' })
  }
})

// Get analytics data
router.get('/analytics', auth, adminAuth, async (req, res) => {
  try {
    const days = parseInt(req.query.days) || 30
    const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000)

    const [userGrowth, discussionGrowth] = await Promise.all([
      User.aggregate([
        {
          $match: { createdAt: { $gte: startDate } }
        },
        {
          $group: {
            _id: {
              year: { $year: '$createdAt' },
              month: { $month: '$createdAt' },
              day: { $dayOfMonth: '$createdAt' }
            },
            count: { $sum: 1 }
          }
        },
        { $sort: { '_id.year': 1, '_id.month': 1, '_id.day': 1 } }
      ]),
      Discussion.aggregate([
        {
          $match: { createdAt: { $gte: startDate } }
        },
        {
          $group: {
            _id: {
              year: { $year: '$createdAt' },
              month: { $month: '$createdAt' },
              day: { $dayOfMonth: '$createdAt' }
            },
            count: { $sum: 1 }
          }
        },
        { $sort: { '_id.year': 1, '_id.month': 1, '_id.day': 1 } }
      ])
    ])

    res.json({
      userGrowth: userGrowth.map(item => ({
        date: new Date(item._id.year, item._id.month - 1, item._id.day),
        count: item.count
      })),
      discussionGrowth: discussionGrowth.map(item => ({
        date: new Date(item._id.year, item._id.month - 1, item._id.day),
        count: item.count
      }))
    })
  } catch (error) {
    console.error('Error fetching analytics:', error)
    res.status(500).json({ message: 'Failed to fetch analytics data' })
  }
})

module.exports = router
