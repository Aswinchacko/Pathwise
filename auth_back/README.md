# Auth Backend

A simple authentication backend for the PathWise dashboard with MongoDB integration and Google OAuth support.

## Features

- User registration and login
- Google OAuth authentication
- JWT token authentication
- Password hashing with bcrypt
- MongoDB integration with Mongoose
- Protected routes middleware
- User profile management

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (copy from `env.example`):
```bash
cp env.example .env
```

3. Update `.env` with your configuration:
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/pathwise_auth
JWT_SECRET=your_jwt_secret_key_here_change_in_production
JWT_EXPIRE=24h

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here
```

4. Set up Google OAuth:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google+ API
   - Go to Credentials → Create Credentials → OAuth 2.0 Client ID
   - Set authorized JavaScript origins to your frontend URL (e.g., `http://localhost:3000`)
   - Copy the Client ID to your `.env` file

5. Start MongoDB (make sure MongoDB is running locally)

6. Run the server:
```bash
# Development
npm run dev

# Production
npm start
```

## API Endpoints

### Authentication

#### POST `/api/auth/register`
Register a new user.

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com"
  }
}
```

#### POST `/api/auth/login`
Login with existing credentials.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com"
  }
}
```

#### POST `/api/auth/google`
Login with Google OAuth.

**Request Body:**
```json
{
  "token": "google_id_token_here"
}
```

**Response:**
```json
{
  "message": "Google login successful",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@gmail.com"
  }
}
```

### Protected Routes (require Authorization header)

#### GET `/api/auth/profile`
Get current user profile.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "user": {
    "id": "user_id",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "lastLogin": "2024-01-01T00:00:00.000Z",
    "createdAt": "2024-01-01T00:00:00.000Z"
  }
}
```

#### PUT `/api/auth/profile`
Update user profile.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "firstName": "Jane",
  "lastName": "Smith"
}
```

**Response:**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": "user_id",
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "john@example.com"
  }
}
```

### Health Check

#### GET `/api/health`
Check if the server is running.

**Response:**
```json
{
  "status": "OK",
  "message": "Auth backend is running"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

- `400` - Bad Request (validation errors, invalid credentials)
- `401` - Unauthorized (invalid/missing token)
- `500` - Internal Server Error

## Frontend Integration

### Regular Login/Register
To connect your React frontend to this backend:

1. Update your login/register forms to make API calls to these endpoints
2. Store the JWT token in localStorage or secure storage
3. Include the token in the Authorization header for protected requests
4. Handle token expiration and refresh as needed

Example frontend API call:
```javascript
const login = async (email, password) => {
  const response = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })
  
  const data = await response.json()
  if (response.ok) {
    localStorage.setItem('token', data.token)
    return data
  } else {
    throw new Error(data.message)
  }
}
```

### Google OAuth Integration
For Google OAuth, you'll need to:

1. Add Google Sign-In to your frontend
2. Get the ID token from Google
3. Send it to your backend

Example frontend Google OAuth:
```javascript
// After Google Sign-In success
const handleGoogleLogin = async (googleResponse) => {
  const response = await fetch('http://localhost:5000/api/auth/google', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      token: googleResponse.credential 
    }),
  })
  
  const data = await response.json()
  if (response.ok) {
    localStorage.setItem('token', data.token)
    return data
  } else {
    throw new Error(data.message)
  }
}
``` 