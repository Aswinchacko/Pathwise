# Resume Parser Integration Setup Guide

This guide will help you set up the complete Resume Parser integration between your FastAPI backend and React dashboard.

## 🚀 Quick Start

### 1. Backend Setup (FastAPI)

```bash
# Navigate to resume parser directory
cd resume_parser

# Install dependencies
pip install -r requirements.txt

# Install spacy model (required for NLP processing)
python -m spacy download en_core_web_sm

# Start the server
python start_server.py
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup (React Dashboard)

```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`

### 3. Test the Integration

1. Open `http://localhost:5173/resume-parser` in your browser
2. Upload a PDF or DOCX resume file
3. View the extracted data in a clean, formatted display

## 📁 File Structure

```
PathWise/
├── resume_parser/                 # FastAPI Backend
│   ├── main.py                   # Main FastAPI app with CORS
│   ├── parsers.py                # Resume parsing logic
│   ├── start_server.py           # Server startup script
│   ├── test_api.py              # API testing script
│   ├── requirements.txt          # Python dependencies
│   └── README.md                # Backend documentation
├── dashboard/                    # React Frontend
│   └── src/
│       ├── components/
│       │   ├── ResumeUpload.jsx  # File upload component
│       │   ├── ResumeUpload.css  # Upload component styles
│       │   ├── ResumeDisplay.jsx # Data display component
│       │   └── ResumeDisplay.css # Display component styles
│       ├── pages/
│       │   ├── ResumeParser.jsx  # Main parser page
│       │   └── ResumeParser.css  # Parser page styles
│       ├── services/
│       │   └── resumeService.js  # API service layer
│       └── App.jsx              # Updated with new route
```

## 🔧 Configuration

### Backend Configuration

The FastAPI server is configured with:
- **Port**: 8000
- **CORS**: Enabled for localhost:5173 and localhost:3000
- **File Support**: PDF and DOCX
- **Max File Size**: 10MB
- **Auto-cleanup**: Temporary files are deleted after processing

### Frontend Configuration

The React service is configured to:
- **API Base URL**: http://localhost:8000
- **Timeout**: 30 seconds for file uploads
- **File Validation**: Client-side type and size validation
- **Error Handling**: Comprehensive error messages

## 🧪 Testing

### Test the API directly:

```bash
# Test health check
curl http://localhost:8000/health

# Test file upload
curl -X POST "http://localhost:8000/upload-resume" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/resume.pdf"
```

### Test with Python script:

```bash
cd resume_parser
python test_api.py path/to/your/resume.pdf
```

## 🎯 Features

### Backend Features
- ✅ CORS configuration for frontend integration
- ✅ File type validation (PDF, DOCX only)
- ✅ File size validation (10MB max)
- ✅ Comprehensive error handling
- ✅ Automatic file cleanup
- ✅ Structured JSON response
- ✅ Health check endpoint
- ✅ Detailed logging

### Frontend Features
- ✅ Drag-and-drop file upload
- ✅ File type and size validation
- ✅ Loading states and progress indicators
- ✅ Error handling with user-friendly messages
- ✅ Clean, responsive data display
- ✅ Reusable service layer
- ✅ Modern UI with animations

### Data Extraction
- ✅ Personal information (name, email, phone, location)
- ✅ Professional summary
- ✅ Skills list
- ✅ Work experience with dates and companies
- ✅ Education history with degrees and institutions
- ✅ Social links (LinkedIn, GitHub)

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure the FastAPI server is running on port 8000
   - Check that CORS origins include your frontend URL

2. **Spacy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **File Upload Fails**
   - Check file size (must be < 10MB)
   - Ensure file is PDF or DOCX
   - Check browser console for errors

4. **API Connection Issues**
   - Verify FastAPI server is running
   - Check the API_BASE_URL in resumeService.js
   - Test with curl or the test script

### Debug Mode

Enable debug logging in FastAPI by setting the log level to debug in `start_server.py`:

```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="debug"  # Change from "info" to "debug"
)
```

## 📚 API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## 🔄 Next Steps

1. **Production Deployment**: Update CORS origins for production domains
2. **File Storage**: Consider using cloud storage for uploaded files
3. **Database Integration**: Store parsed resume data in your database
4. **Authentication**: Add authentication to the API endpoints
5. **Rate Limiting**: Implement rate limiting for file uploads
6. **File Processing Queue**: Add background job processing for large files

## 📞 Support

If you encounter any issues:
1. Check the console logs in both frontend and backend
2. Verify all dependencies are installed correctly
3. Test the API endpoints directly with curl
4. Check the browser network tab for failed requests
