/**
 * Test Settings Integration
 * Tests the optimized and dynamic Settings component
 */

const axios = require('axios')

// Configuration
const AUTH_API_URL = 'http://localhost:5000/api/auth'
const RESUME_API_URL = 'http://127.0.0.1:8001'

// Test user data
const testUser = {
  firstName: 'John',
  lastName: 'Doe',
  email: 'john.doe.settings@test.com',
  password: 'testpass123'
}

// Sample resume data
const sampleResumeData = {
  name: 'John Doe',
  email: 'john.doe.settings@test.com',
  phone: '+1-555-123-4567',
  location: 'San Francisco, CA',
  summary: 'Experienced full-stack developer with 5+ years in web technologies',
  skills: ['JavaScript', 'React', 'Node.js', 'Python', 'MongoDB', 'AWS'],
  education: [
    {
      degree: 'Bachelor of Science in Computer Science',
      institution: 'Stanford University',
      year_start: '2016',
      year_end: '2020',
      gpa: '3.8'
    }
  ],
  experience: [
    {
      title: 'Senior Software Engineer',
      company: 'TechCorp Inc.',
      year_start: '2022',
      year_end: 'Present',
      description: 'Lead development of scalable web applications using React and Node.js'
    },
    {
      title: 'Software Developer',
      company: 'StartupXYZ',
      year_start: '2020',
      year_end: '2022',
      description: 'Developed and maintained full-stack applications'
    }
  ],
  projects: [
    {
      title: 'E-commerce Platform',
      description: 'Built a full-featured e-commerce platform with React and Node.js',
      technologies: ['React', 'Node.js', 'MongoDB', 'Stripe API']
    }
  ],
  certifications: ['AWS Certified Developer', 'MongoDB Certified Developer'],
  languages: ['English (Native)', 'Spanish (Conversational)']
}

let authToken = null
let userId = null

async function testSettingsIntegration() {
  console.log('🧪 Testing Settings Integration...\n')

  try {
    // Test 1: Register user
    console.log('1️⃣ Testing user registration...')
    const registerResponse = await axios.post(`${AUTH_API_URL}/register`, testUser)
    
    if (registerResponse.data.token && registerResponse.data.user) {
      authToken = registerResponse.data.token
      userId = registerResponse.data.user.id
      console.log('✅ User registered successfully')
      console.log(`   User ID: ${userId}`)
    } else {
      throw new Error('Registration failed')
    }

    // Test 2: Get initial profile
    console.log('\n2️⃣ Testing profile retrieval...')
    const profileResponse = await axios.get(`${AUTH_API_URL}/profile`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
    
    if (profileResponse.data.user) {
      console.log('✅ Profile retrieved successfully')
      console.log(`   Name: ${profileResponse.data.user.firstName} ${profileResponse.data.user.lastName}`)
      console.log(`   Skills: ${(profileResponse.data.user.skills || []).length} skills`)
      console.log(`   Experience: ${(profileResponse.data.user.experience || []).length} positions`)
    } else {
      throw new Error('Profile retrieval failed')
    }

    // Test 3: Update profile from resume data
    console.log('\n3️⃣ Testing profile update from resume...')
    const resumeUpdateResponse = await axios.put(`${AUTH_API_URL}/profile/from-resume`, sampleResumeData, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
    
    if (resumeUpdateResponse.data.user) {
      const user = resumeUpdateResponse.data.user
      console.log('✅ Profile updated from resume successfully')
      console.log(`   Full Name: ${user.full_name}`)
      console.log(`   Phone: ${user.phone}`)
      console.log(`   Location: ${user.location}`)
      console.log(`   Skills: ${user.skills.length} skills`)
      console.log(`   Education: ${user.education.length} degrees`)
      console.log(`   Experience: ${user.experience.length} positions`)
      console.log(`   Projects: ${user.projects.length} projects`)
      console.log(`   Certifications: ${user.certifications.length} certifications`)
    } else {
      throw new Error('Resume profile update failed')
    }

    // Test 4: Manual profile update
    console.log('\n4️⃣ Testing manual profile update...')
    const manualUpdate = {
      summary: 'Updated summary: Passionate software developer with expertise in modern web technologies',
      skills: [...sampleResumeData.skills, 'Docker', 'Kubernetes'],
      preferences: {
        emailNotifications: false,
        weeklyReports: true,
        theme: 'dark'
      }
    }
    
    const manualUpdateResponse = await axios.put(`${AUTH_API_URL}/profile`, manualUpdate, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
    
    if (manualUpdateResponse.data.user) {
      const user = manualUpdateResponse.data.user
      console.log('✅ Manual profile update successful')
      console.log(`   Updated Summary: ${user.summary.substring(0, 50)}...`)
      console.log(`   Updated Skills Count: ${user.skills.length}`)
      console.log(`   Email Notifications: ${user.preferences.emailNotifications}`)
      console.log(`   Weekly Reports: ${user.preferences.weeklyReports}`)
      console.log(`   Theme: ${user.preferences.theme}`)
    } else {
      throw new Error('Manual profile update failed')
    }

    // Test 5: Get updated profile
    console.log('\n5️⃣ Testing updated profile retrieval...')
    const updatedProfileResponse = await axios.get(`${AUTH_API_URL}/profile`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
    
    if (updatedProfileResponse.data.user) {
      const user = updatedProfileResponse.data.user
      console.log('✅ Updated profile retrieved successfully')
      console.log('\n📊 Complete Profile Data:')
      console.log(`   Basic Info: ${user.full_name} (${user.email})`)
      console.log(`   Contact: ${user.phone}, ${user.location}`)
      console.log(`   Skills: ${user.skills.join(', ')}`)
      console.log(`   Experience: ${user.experience.length} positions`)
      console.log(`   Education: ${user.education.length} degrees`)
      console.log(`   Projects: ${user.projects.length} projects`)
      console.log(`   Certifications: ${user.certifications.join(', ')}`)
      console.log(`   Languages: ${user.languages.join(', ')}`)
      console.log(`   Preferences: Notifications=${user.preferences.emailNotifications}, Reports=${user.preferences.weeklyReports}, Theme=${user.preferences.theme}`)
    } else {
      throw new Error('Updated profile retrieval failed')
    }

    // Test 6: Authentication persistence
    console.log('\n6️⃣ Testing authentication persistence...')
    const authCheckResponse = await axios.get(`${AUTH_API_URL}/profile`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
    
    if (authCheckResponse.data.user && authCheckResponse.data.user.id === userId) {
      console.log('✅ Authentication persistence verified')
      console.log(`   Token valid for user: ${authCheckResponse.data.user.firstName} ${authCheckResponse.data.user.lastName}`)
    } else {
      throw new Error('Authentication persistence failed')
    }

    console.log('\n🎉 All Settings Integration Tests Passed!')
    console.log('\n📋 Summary:')
    console.log('   ✅ User registration and authentication')
    console.log('   ✅ Profile data retrieval')
    console.log('   ✅ Resume-to-profile integration')
    console.log('   ✅ Manual profile updates')
    console.log('   ✅ Preference management')
    console.log('   ✅ Authentication persistence')
    console.log('\n🚀 The Settings component is ready for dynamic, database-driven operation!')

  } catch (error) {
    console.error('\n❌ Settings Integration Test Failed:')
    if (error.response) {
      console.error(`   Status: ${error.response.status}`)
      console.error(`   Message: ${error.response.data.message || error.response.data}`)
    } else {
      console.error(`   Error: ${error.message}`)
    }
    console.error('\n🔧 Troubleshooting:')
    console.error('   - Ensure auth backend is running on port 5000')
    console.error('   - Ensure MongoDB is running and connected')
    console.error('   - Check network connectivity')
    console.error('   - Verify API endpoints are properly configured')
    
    process.exit(1)
  }
}

// Run the test
if (require.main === module) {
  testSettingsIntegration()
}

module.exports = { testSettingsIntegration }
