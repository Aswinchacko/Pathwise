# Resume-to-Profile Integration

This document explains how resume data from the resume parser service is integrated with user profiles in the Settings page.

## Architecture Overview

```
User uploads resume → Resume Parser Service → MongoDB (resume collection) 
                                          ↓
Settings.jsx ← Profile Service ← Auth Backend ← User Profile (users collection)
```

## Data Flow

1. **Resume Upload**: User uploads resume file in Settings.jsx
2. **Parsing**: Resume parser service extracts structured data 
3. **Storage**: Parsed resume stored in `resume` collection with user_id
4. **Profile Update**: Parsed data automatically updates user profile in `users` collection
5. **UI Update**: Settings page reflects the updated profile data

## Backend Changes

### Extended User Model (`auth_back/models/User.js`)
Added fields to support resume data:
```javascript
phone: String,
location: String, 
summary: String,
skills: [String],
education: [{
  degree: String,
  institution: String,
  year_start: String,
  year_end: String,
  dates: String,
  gpa: String
}],
experience: [{
  role: String,
  title: String, // Support both 'role' and 'title'
  company: String,
  year_start: String,
  year_end: String,
  dates: String,
  description: String
}],
projects: [{
  title: String,
  description: String,
  technologies: [String],
  url: String
}],
certifications: [String],
languages: [String]
```

### New API Endpoints (`auth_back/routes/auth.js`)

#### GET `/api/auth/profile`
Returns extended profile data including resume fields.

#### PUT `/api/auth/profile` 
Updates profile with all extended fields.

#### PUT `/api/auth/profile/from-resume`
**New endpoint** specifically for updating profile from parsed resume data.

## Frontend Integration

### Services Updated

#### `profileService.js`
- `updateProfileFromResume()` - Uses new `/profile/from-resume` endpoint
- `getProfile()` - Returns extended profile data
- `updateProfile()` - Supports all resume fields

#### `resumeStorageService.js`
- Existing service for resume CRUD operations
- Used in Settings.jsx for resume management

### Settings.jsx Integration

Key functions:
```javascript
handleResumeUpload() // Uploads and parses resume
updateProfileFromResume() // Updates profile with parsed data
loadProfile() // Loads extended profile data
handleApplyResumeToProfile() // Apply specific resume to profile
```

## Usage Flow

1. **Upload Resume**: User clicks "Upload Resume" in Settings
2. **Auto-Update**: Profile automatically updates with parsed data
3. **Manual Edit**: User can manually edit any profile fields
4. **Apply Resume**: User can apply different saved resumes to profile
5. **Save Changes**: Manual profile changes saved via regular update endpoint

## Data Mapping

Resume parser output → User profile fields:

| Resume Field | Profile Field | Notes |
|-------------|---------------|--------|
| `name` | `firstName`, `lastName`, `full_name` | Split on space |
| `email` | `email` | Direct mapping |
| `phone` | `phone` | Direct mapping |
| `location` | `location` | Direct mapping |
| `summary` | `summary` | Direct mapping |
| `skills` | `skills` | Array mapping |
| `education` | `education` | Array with nested objects |
| `experience` | `experience` | Array, handles both `role` and `title` |
| `projects` | `projects` | Array with nested objects |
| `certifications` | `certifications` | Array mapping |
| `languages` | `languages` | Array mapping |

## Error Handling

- Resume upload failures show error messages
- Profile update failures are logged and displayed
- Network errors are handled gracefully
- Invalid resume formats are rejected

## Testing

Run the integration test:
```bash
python test_resume_profile_integration.py
```

This tests:
- Service connectivity
- User creation/login
- Resume upload and parsing
- Profile update from resume data
- Regular profile updates

## MongoDB Collections

### `resume` Collection
Stores parsed resume data with user association:
```javascript
{
  user_id: ObjectId,
  parsed_data: { /* resume fields */ },
  file_name: String,
  file_type: String,
  created_at: Date,
  updated_at: Date
}
```

### `users` Collection  
Extended with resume fields for unified profile storage:
```javascript
{
  // Basic auth fields
  firstName: String,
  lastName: String,
  email: String,
  // Extended resume fields
  phone: String,
  location: String,
  summary: String,
  skills: [String],
  education: [Object],
  experience: [Object],
  projects: [Object],
  certifications: [String],
  languages: [String]
}
```

## Benefits

1. **Unified Profile**: All user data in one place
2. **Auto-Population**: Resume data automatically fills profile
3. **Flexibility**: Users can edit auto-populated data
4. **Multiple Resumes**: Users can store and apply different resumes
5. **Data Persistence**: Profile data survives resume deletions
6. **Consistent API**: Single profile endpoint for all user data

## Future Enhancements

- Profile completeness scoring
- Resume comparison and merging
- Skill validation and suggestions
- Export profile as resume
- Integration with recommendation engine using profile data