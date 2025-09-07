# Community Feature Setup

## Overview
The Community feature has been made dynamic with MongoDB integration. Users can now create, view, like, and comment on discussions that are stored in the database.

## Backend Changes

### New Files Created:
1. **`auth_back/models/Discussion.js`** - MongoDB schema for discussions and comments
2. **`auth_back/routes/discussions.js`** - API endpoints for discussion operations
3. **`auth_back/seedDiscussions.js`** - Script to seed initial discussion data

### Modified Files:
1. **`auth_back/server.js`** - Added discussion routes

### API Endpoints:
- `GET /api/discussions` - Get all discussions (with optional category filter)
- `GET /api/discussions/:id` - Get single discussion (increments view count)
- `POST /api/discussions` - Create new discussion (requires auth)
- `POST /api/discussions/:id/comments` - Add comment to discussion (requires auth)
- `PUT /api/discussions/:id/like` - Like a discussion (requires auth)

## Frontend Changes

### New Files Created:
1. **`dashboard/src/services/discussionService.js`** - Service for API communication

### Modified Files:
1. **`dashboard/src/pages/Community.jsx`** - Updated to use API instead of static data
2. **`dashboard/src/pages/Community.css`** - Added loading and error state styles

### Features Added:
- Dynamic data fetching from MongoDB
- Loading states while fetching data
- Error handling with retry functionality
- Real-time updates for likes and comments
- Category filtering on the backend

## Database Schema

### Discussions Collection:
```javascript
{
  title: String (required),
  description: String (required),
  author: String (required),
  authorId: ObjectId (ref: User),
  category: String (enum: Web Development, Data Science, etc.),
  views: Number (default: 0),
  likes: Number (default: 0),
  comments: [CommentSchema],
  createdAt: Date,
  updatedAt: Date
}
```

### Comments (embedded in discussions):
```javascript
{
  text: String (required),
  author: String (required),
  authorId: ObjectId (ref: User),
  likes: Number (default: 0),
  createdAt: Date,
  updatedAt: Date
}
```

## Setup Instructions

1. **Start the backend server:**
   ```bash
   cd auth_back
   npm start
   ```

2. **Seed initial data (optional):**
   ```bash
   cd auth_back
   node seedDiscussions.js
   ```

3. **Start the frontend:**
   ```bash
   cd dashboard
   npm run dev
   ```

## Authentication
All discussion creation, commenting, and liking requires authentication. The JWT token from localStorage is sent with API requests.

## Error Handling
- Network errors are caught and displayed to users
- Retry functionality for failed requests
- Loading states during API calls
- Form validation for required fields
