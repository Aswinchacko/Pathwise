# PathWise Setup Guide

## Complete Authentication System with React Dashboard

This project includes a complete authentication system with:
- **FastAPI Backend** (AUTH_test/) - Email + OAuth authentication
- **Landing Page** (landing-page/) - Login/Register with beautiful UI
- **React Dashboard** (dashboard/) - Professional dashboard with user management

## 🚀 Quick Start

### 1. Backend Setup (FastAPI)

```bash
cd AUTH_test

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp env.example .env

# Edit .env with your OAuth credentials
# MONGO_URI=mongodb://localhost:27017
# SECRET_KEY=your-super-secret-key-change-this-in-production
# GOOGLE_CLIENT_ID=your-google-client-id
# GOOGLE_CLIENT_SECRET=your-google-client-secret
# ... (add other OAuth credentials)

# Start the backend server
uvicorn main:app --reload
```

**Backend will run on: http://localhost:8000**
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend Dashboard Setup (React + Vite)

```bash
cd dashboard

# Install dependencies (already done)
npm install

# Start development server
npm run dev
```

**Dashboard will run on: http://localhost:5173**

### 3. Landing Page

The landing page is ready at: `landing-page/index.html`
- Login: `landing-page/login.html`
- Register: `landing-page/register.html`

## 🔧 Features Implemented

### ✅ Backend Features (FastAPI)
- **Email/Password Authentication** with JWT tokens
- **Google OAuth** integration
- **LinkedIn OAuth** integration  
- **GitHub OAuth** integration
- **MongoDB** user storage
- **Password hashing** with bcrypt
- **CORS** support for frontend
- **Automatic API docs** with Swagger

### ✅ Frontend Features (React Dashboard)
- **Professional Dashboard** with sidebar navigation
- **User Authentication** flow
- **JWT Token Management** 
- **User Profile Display** with registered names
- **Statistics Cards** showing user metrics
- **Recent Activity** showing new registrations
- **OAuth Login** buttons for social auth
- **Responsive Design** for all screen sizes
- **Modern UI** with gradients and animations

### ✅ Landing Page Features
- **Beautiful Login/Register Pages** with PathWise branding
- **OAuth Social Buttons** (Google, LinkedIn, GitHub, Facebook)
- **Form Validation** and password strength indicator
- **Integration with Backend** API
- **Automatic Redirect** to dashboard after login

## 🎯 How It Works

### Authentication Flow:
1. **User visits** `landing-page/login.html` or `landing-page/register.html`
2. **Submits form** → Sends request to FastAPI backend
3. **Backend validates** credentials and returns JWT token
4. **Frontend stores** token in localStorage
5. **Redirects to** React dashboard at `http://localhost:5173/dashboard`
6. **Dashboard fetches** user info using the JWT token
7. **Displays** user profile and dashboard data

### OAuth Flow:
1. **User clicks** social login button
2. **Redirects to** OAuth provider (Google/LinkedIn/GitHub)
3. **User authorizes** application
4. **Provider redirects** back with auth code
5. **Backend exchanges** code for access token
6. **Backend creates/finds** user and returns JWT
7. **User redirected** to dashboard with authentication

## 📊 Dashboard Features

### Overview Tab:
- **User Statistics**: Total users, new users today, active users, verified users
- **Recent Registrations**: Shows newly registered users with their names, providers, and status
- **Quick Actions**: Buttons for managing users, courses, analytics, settings

### User Display:
- **User Profile** in sidebar showing logged-in user's name and email
- **Recent Users List** showing registered user names and details
- **Provider Icons** showing how users registered (Google, LinkedIn, GitHub, Email)
- **Verification Status** showing which users are verified

### Navigation:
- **Sidebar Navigation** with Overview, Users, Courses, Analytics, Settings
- **Search Bar** for finding users and content
- **Notifications** bell with badge counter
- **User Avatar** with first letter of name/email

## 🎨 Design Theme

The entire system uses a consistent design theme:
- **Primary Color**: #43b97e (Green)
- **Secondary Color**: #2e8b5f (Dark Green)
- **Fonts**: Inter (dashboard), Glory + Lato (landing pages)
- **Modern UI**: Rounded corners, shadows, gradients
- **Responsive**: Works on desktop, tablet, mobile

## 🛠 Next Steps

You can now:
1. **Setup OAuth apps** for Google, LinkedIn, GitHub
2. **Configure MongoDB** connection
3. **Customize the dashboard** with more features
4. **Add more pages** to the dashboard (Users, Courses, Analytics)
5. **Deploy to production** with proper environment variables

## 📱 Screenshots

The system includes:
- **Landing Page** with university theme
- **Login/Register** with OAuth icons
- **Professional Dashboard** with statistics
- **User Management** features
- **Responsive Design** for all devices

## 🔐 Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Environment variable security
- Input validation with Pydantic
- OAuth 2.0 security

All registered user names and information are displayed in the dashboard overview, showing a complete user management system!