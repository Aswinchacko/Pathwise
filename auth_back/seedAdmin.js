const mongoose = require('mongoose')
const User = require('./models/User')
require('dotenv').config()

const seedAdmin = async () => {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/pathwise')
    console.log('Connected to MongoDB')

    // Check if admin user already exists
    const existingAdmin = await User.findOne({ role: 'admin' })
    if (existingAdmin) {
      console.log('Admin user already exists:', existingAdmin.email)
      process.exit(0)
    }

    // Create admin user
    const adminUser = new User({
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin@pathwise.com',
      password: 'admin123', // This will be hashed automatically
      role: 'admin',
      isActive: true
    })

    await adminUser.save()
    console.log('Admin user created successfully!')
    console.log('Email: admin@pathwise.com')
    console.log('Password: admin123')
    console.log('Please change the password after first login.')

  } catch (error) {
    console.error('Error creating admin user:', error)
  } finally {
    mongoose.connection.close()
  }
}

seedAdmin()
