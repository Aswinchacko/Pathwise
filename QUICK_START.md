# PathWise OAuth Backend - Quick Start Guide

## 🚀 Quick Setup

### 1. Backend Setup
```bash
cd backend
npm install
node setup.js
```

### 2. Configure OAuth Credentials
Edit `backend/.env` file with your credentials:

```env
# Generate a strong JWT secret
JWT_SECRET=your_very_strong_secret_key_here

# Google OAuth (get from https://console.cloud.google.com/)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# GitHub OAuth (get from https://github.com/settings/developers)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Facebook OAuth (get from https://developers.facebook.com/)
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### 3. Start Backend Server
```bash
cd backend
npm run dev
```

Server will start on `http://localhost:5000`

### 4. Test Backend
Visit: `http://localhost:5000/api/health`

## 🎯 Frontend Integration

### 1. Add OAuth Login Component
```jsx
// In your React app
import OAuthLogin from './components/OAuthLogin';

function LoginPage() {
  return <OAuthLogin />;
}
```

### 2. Add Auth Success Handler
```jsx
// In your React Router
import AuthSuccess from './components/AuthSuccess';

<Route path="/auth-success" element={<AuthSuccess />} />
```

### 3. Use Auth Service
```jsx
import authService from './services/authService';

// Check if authenticated
if (authService.isAuthenticated()) {
  // User is logged in
}

// Logout
await authService.logout();
```

## 🔧 OAuth Provider Setup

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google+ API
3. Credentials → Create OAuth 2.0 Client ID
4. Set redirect URI: `http://localhost:5000/api/auth/google/callback`

### GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. New OAuth App
3. Set callback URL: `http://localhost:5000/api/auth/github/callback`

### Facebook OAuth
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create app → Add Facebook Login
3. Set redirect URI: `http://localhost:5000/api/auth/facebook/callback`

## 📁 Project Structure
```
backend/
├── server.js              # Main server file
├── routes/auth.js         # OAuth routes
├── config/passport.js     # Passport strategies
├── package.json           # Dependencies
├── .env                   # Environment variables
└── README.md             # Detailed documentation

dashboard/
├── src/
│   ├── components/
│   │   ├── OAuthLogin.jsx    # OAuth login component
│   │   ├── OAuthLogin.css    # Login styles
│   │   ├── AuthSuccess.jsx   # Auth success handler
│   │   └── AuthSuccess.css   # Success styles
│   └── services/
│       └── authService.js    # Auth service
```

## 🧪 Testing

1. Start backend: `cd backend && npm run dev`
2. Start frontend: `cd dashboard && npm run dev`
3. Visit login page
4. Click OAuth button
5. Complete OAuth flow
6. Check token in localStorage

## 🔒 Security Notes

- Use strong JWT_SECRET
- Enable HTTPS in production
- Configure CORS properly
- Never commit .env file
- Consider httpOnly cookies for tokens

## 🆘 Troubleshooting

- **CORS errors**: Check FRONTEND_URL in .env
- **OAuth errors**: Verify credentials and callback URLs
- **Port conflicts**: Change PORT in .env
- **Token issues**: Check JWT_SECRET is set

## 📞 Support

Check the detailed README.md in the backend folder for complete documentation. 