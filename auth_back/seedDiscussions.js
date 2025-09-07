const mongoose = require('mongoose')
const Discussion = require('./models/Discussion')
require('dotenv').config()

const sampleDiscussions = [
  {
    title: 'Best practices for React state management',
    description: 'Share your experiences with different state management solutions in React applications.',
    author: 'Sarah Chen',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Web Development',
    views: 234,
    likes: 24,
    comments: []
  },
  {
    title: 'Getting started with Machine Learning',
    description: 'Tips and resources for beginners in machine learning and data science.',
    author: 'Alex Rodriguez',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Data Science',
    views: 156,
    likes: 10,
    comments: []
  },
  {
    title: 'Career transition from non-tech to tech',
    description: 'Experiences and advice for professionals transitioning into tech roles.',
    author: 'Maria Garcia',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Career Advice',
    views: 342,
    likes: 30,
    comments: []
  },
  {
    title: 'Interview preparation strategies',
    description: 'How to prepare effectively for technical interviews and coding challenges.',
    author: 'David Kim',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Career Advice',
    views: 189,
    likes: 15,
    comments: []
  },
  {
    title: 'Building a portfolio website',
    description: 'Design and development tips for creating an impressive portfolio.',
    author: 'Emily Johnson',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Web Development',
    views: 267,
    likes: 20,
    comments: []
  },
  {
    title: 'Open source contribution guide',
    description: 'How to start contributing to open source projects as a beginner.',
    author: 'Michael Brown',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Development',
    views: 198,
    likes: 18,
    comments: []
  }
]

async function seedDiscussions() {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/pathwise')
    console.log('Connected to MongoDB')

    // Clear existing discussions
    await Discussion.deleteMany({})
    console.log('Cleared existing discussions')

    // Insert sample discussions
    await Discussion.insertMany(sampleDiscussions)
    console.log('Seeded discussions successfully')

    process.exit(0)
  } catch (error) {
    console.error('Error seeding discussions:', error)
    process.exit(1)
  }
}

seedDiscussions()
