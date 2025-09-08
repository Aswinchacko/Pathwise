# Resume Parser MongoDB Integration

## Overview
This document describes the integration of the Resume Parser service with MongoDB to store and manage parsed resume data in the "resume" collection.

## Changes Made

### 1. Resume Parser Service (`resume_parser/main.py`)
- **Collection Name**: Changed from `db.resumes` to `db.resume` to match the specified collection name
- **MongoDB Integration**: Already had full CRUD operations for resume storage
- **User Association**: Resumes are stored with optional `user_id` field for user-specific data

### 2. Dashboard Resume Service (`dashboard/src/services/resumeService.js`)
- **User ID Support**: Added `userId` parameter to `parseResume()` method
- **New Methods Added**:
  - `getResumes(userId)` - Retrieve all resumes for a user or all resumes
  - `getResume(resumeId)` - Get a specific resume by ID
  - `deleteResume(resumeId)` - Delete a resume by ID
- **Enhanced Error Handling**: Improved error handling for all API calls

### 3. Resume Parser Component (`dashboard/src/pages/ResumeParser.jsx`)
- **User Authentication**: Integrated with `authService` to get current user
- **State Management**: Added state for user, saved resumes, and loading status
- **New Features**:
  - Display saved resumes for authenticated users
  - Load previously saved resumes
  - Delete saved resumes
  - User-specific resume storage
- **Enhanced UI**: Added saved resumes section with load/delete functionality

### 4. Resume Upload Component (`dashboard/src/components/ResumeUpload.jsx`)
- **User ID Integration**: Accepts and passes `userId` to the resume service
- **Enhanced Functionality**: Resumes are now associated with the logged-in user

### 5. Styling (`dashboard/src/pages/ResumeParser.css`)
- **New Styles**: Added comprehensive styling for saved resumes section
- **Responsive Design**: Mobile-friendly layout for all new components
- **Interactive Elements**: Hover effects and button states for better UX

## MongoDB Schema

The resume data is stored in the `resume` collection with the following structure:

```javascript
{
  _id: ObjectId,
  user_id: String, // Optional - for user-specific resumes
  parsed_data: {
    name: String,
    email: String,
    phone: String,
    location: String,
    summary: String,
    experience: [{
      title: String,
      company: String,
      dates: String,
      description: String
    }],
    education: [{
      degree: String,
      institution: String,
      dates: String,
      gpa: String
    }],
    skills: [String],
    languages: [String],
    certifications: [String],
    projects: [{
      title: String,
      description: String,
      technologies: [String]
    }],
    raw_text: String
  },
  created_at: Date,
  updated_at: Date,
  file_name: String,
  file_type: String
}
```

## API Endpoints

### Resume Parser Service (Port 8001)
- `POST /parse` - Upload and parse resume file (with optional user_id)
- `POST /parse-text` - Parse resume text directly
- `GET /resumes` - Get all resumes (with optional user_id filter)
- `GET /resumes/{resume_id}` - Get specific resume by ID
- `DELETE /resumes/{resume_id}` - Delete resume by ID
- `GET /health` - Health check

## Testing

### 1. Start the Services
```bash
# Start Resume Parser Service
cd resume_parser
python main.py

# Start Dashboard (in another terminal)
cd dashboard
npm run dev
```

### 2. Test MongoDB Integration
```bash
# Run the comprehensive test
cd resume_parser
python test_mongodb_integration.py
```

### 3. Manual Testing
1. Open the dashboard at `http://localhost:5173`
2. Navigate to the Resume Parser page
3. Upload a resume file (PDF, DOCX, or TXT)
4. Verify the resume is parsed and displayed
5. Check that the resume appears in the "Your Saved Resumes" section
6. Test loading and deleting saved resumes

## Features

### For Authenticated Users
- ✅ Resume parsing and storage with user association
- ✅ View all saved resumes
- ✅ Load previously saved resumes
- ✅ Delete saved resumes
- ✅ User-specific resume management

### For Anonymous Users
- ✅ Resume parsing (without user association)
- ✅ View parsed resume data
- ❌ Resume storage and management (requires authentication)

## Error Handling
- Comprehensive error handling for all API calls
- User-friendly error messages
- Graceful fallbacks for service unavailability
- Loading states for better UX

## Security Considerations
- User authentication required for resume storage
- User-specific data isolation
- Input validation and sanitization
- File type and size validation

## Future Enhancements
- Resume versioning and history
- Resume sharing capabilities
- Advanced search and filtering
- Resume templates and formatting
- Export functionality (PDF, Word, etc.)
- Resume analytics and insights

## Troubleshooting

### Common Issues
1. **MongoDB Connection Failed**: Ensure MongoDB is running and accessible
2. **Resume Not Saving**: Check if user is authenticated
3. **File Upload Fails**: Verify file type and size limits
4. **API Errors**: Check service logs for detailed error information

### Debug Steps
1. Check service health endpoints
2. Verify MongoDB connection
3. Check browser console for errors
4. Review service logs
5. Test with the provided test script
