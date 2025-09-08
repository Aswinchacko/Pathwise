# 🤖 PathWise Web Scraping System

## Overview

The PathWise Web Scraping System is an AI-powered solution that automatically discovers and collects learning resources from across the web. It integrates seamlessly with the Resources page to provide users with fresh, relevant educational content.

## 🚀 Features

### Multi-Source Scraping
- **GitHub**: Open source repositories and projects
- **freeCodeCamp**: Free coding tutorials and articles  
- **MDN Web Docs**: Web development documentation
- **Coursera**: Online courses and specializations
- **YouTube**: Video tutorials and lectures
- **Medium**: Articles and blog posts

### Smart Content Extraction
- **Automatic Title & Description**: Extracts meaningful titles and descriptions
- **Content Classification**: Automatically categorizes resources by type and difficulty
- **Metadata Enrichment**: Adds tags, duration estimates, and source information
- **Duplicate Detection**: Prevents duplicate resources from being stored

### Advanced Search Capabilities
- **Query-Based Scraping**: Search for resources by topic or skill
- **URL-Specific Scraping**: Extract content from specific URLs
- **Bulk Operations**: Process multiple queries simultaneously
- **Domain Filtering**: Focus scraping on specific technology domains

## 🏗️ Architecture

### Backend Components

#### 1. WebScrapingService (`resources_service/services/WebScrapingService.js`)
Core service that handles all web scraping operations:
- Multi-source scraping with configurable sources
- Puppeteer integration for dynamic content
- Rate limiting and error handling
- Content processing and normalization

#### 2. Scraping Routes (`resources_service/routes/scraping.js`)
REST API endpoints for scraping operations:
- `POST /api/scraping/resources` - Scrape resources by query
- `POST /api/scraping/url` - Scrape specific URL
- `POST /api/scraping/bulk` - Bulk scrape multiple queries
- `GET /api/scraping/sources` - Get available sources
- `GET /api/scraping/stats` - Get scraping statistics

#### 3. Resource Model (`resources_service/models/Resource.js`)
MongoDB schema for storing scraped resources:
- Comprehensive resource metadata
- Indexing for fast queries
- Validation and data integrity

### Frontend Components

#### 1. Enhanced Resources Page (`dashboard/src/pages/Resources.jsx`)
- **Tabbed Interface**: Browse existing resources or initiate new scraping
- **Real-time Scraping**: Interactive scraping with progress feedback
- **Combined Results**: Seamlessly blend local and scraped resources
- **Advanced Filtering**: Filter by source, type, difficulty, and domain

#### 2. Updated Resources Service (`dashboard/src/services/resourcesService.js`)
- **Scraping Integration**: Methods for all scraping operations
- **Resource Combination**: Merge local and scraped resources
- **Search Enhancement**: Search across both local and remote resources

## 🔧 Setup & Configuration

### 1. Backend Setup

```bash
cd resources_service
npm install
cp env.example .env
# Configure your .env file
npm start
```

### 2. Environment Variables

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/pathwise_resources

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379

# API Configuration
PORT=8001
NODE_ENV=development

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=200

# CORS Configuration
CORS_ORIGIN=http://localhost:5173

# Scraping Configuration
USER_AGENT=Mozilla/5.0 (compatible; PathWise-Bot/1.0)
SCRAPING_DELAY=2000
MAX_CONCURRENT_REQUESTS=5
```

### 3. Frontend Configuration

Add to your dashboard `.env`:
```env
VITE_RESOURCES_API_URL=http://localhost:8001
```

## 📖 Usage Guide

### 1. Basic Scraping

**Query-based scraping:**
```javascript
// Frontend example
const result = await resourcesService.scrapeResourcesForQuery(
  'React hooks', 
  'Frontend Development', 
  { maxResults: 50 }
);
```

**URL-specific scraping:**
```javascript
const result = await resourcesService.scrapeSpecificUrl(
  'https://example.com/tutorial',
  'Web Development',
  'JavaScript'
);
```

### 2. API Examples

**Scrape resources by topic:**
```bash
curl -X POST http://localhost:8001/api/scraping/resources \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning python",
    "domain": "Data Science & AI",
    "maxResults": 30
  }'
```

**Scrape specific URL:**
```bash
curl -X POST http://localhost:8001/api/scraping/url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://python.org/tutorial",
    "domain": "Programming",
    "skill": "Python Basics"
  }'
```

### 3. Bulk Scraping

```bash
curl -X POST http://localhost:8001/api/scraping/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["React hooks", "Vue composition API", "Angular signals"],
    "domain": "Frontend Development",
    "maxResultsPerQuery": 20
  }'
```

## 🎯 Scraping Sources Configuration

Each scraping source is configured with specific strategies:

### GitHub Scraper
- Searches repositories by topic
- Extracts project metadata
- Infers difficulty from stars and description
- Focuses on educational repositories

### freeCodeCamp Scraper
- Searches articles and tutorials
- Extracts reading time estimates
- Categorizes as beginner-friendly
- High-quality curated content

### MDN Scraper
- Focuses on web development documentation
- Authoritative source for web standards
- Comprehensive technical documentation
- Intermediate to advanced level

### Coursera Scraper
- Searches structured courses
- Extracts course duration and ratings
- University-level content
- Professional certifications

### YouTube Scraper
- Searches educational videos
- Extracts video duration and view counts
- Filters for tutorial content
- Visual learning resources

### Medium Scraper
- Searches technical articles
- Extracts reading time and author info
- Developer community content
- Practical insights and tutorials

## 🔍 Content Processing Pipeline

### 1. Data Extraction
- **Title Normalization**: Clean and standardize titles
- **Description Processing**: Extract meaningful descriptions
- **URL Validation**: Ensure valid and accessible URLs
- **Metadata Extraction**: Gather additional context

### 2. Content Classification
- **Type Detection**: Automatically categorize resource types
- **Difficulty Assessment**: Analyze content complexity
- **Domain Mapping**: Assign to appropriate technology domains
- **Tag Generation**: Create relevant tags for searchability

### 3. Quality Assurance
- **Duplicate Detection**: Prevent duplicate resources
- **Content Validation**: Ensure resource accessibility
- **Relevance Scoring**: Rank resources by relevance
- **Data Cleaning**: Remove invalid or broken resources

## 📊 Monitoring & Analytics

### Scraping Statistics
- Total resources scraped
- Success/failure rates by source
- Recent scraping activity
- Resource distribution by type/domain

### Performance Metrics
- Scraping speed and efficiency
- Resource discovery rates
- User engagement with scraped content
- System resource usage

## 🛡️ Rate Limiting & Ethics

### Respectful Scraping
- **Rate Limiting**: Configurable delays between requests
- **User Agent**: Identifies scraping bot appropriately  
- **Robots.txt Compliance**: Respects site scraping policies
- **Error Handling**: Graceful failure handling

### Resource Management
- **Connection Pooling**: Efficient HTTP connections
- **Memory Management**: Prevents memory leaks
- **Concurrent Limits**: Controls simultaneous requests
- **Timeout Handling**: Prevents hanging requests

## 🚀 Quick Start

1. **Start the Resources Service:**
   ```bash
   ./start_resources_service.bat
   ```

2. **Open the Dashboard:**
   Navigate to the Resources page in your PathWise dashboard

3. **Start Scraping:**
   - Click the "Web Scraping" tab
   - Enter a topic like "React hooks"
   - Click "Scrape Resources"
   - Watch as resources are discovered and added!

4. **Browse Results:**
   - Switch back to "Browse Resources" tab
   - Enable "Scraped Data" toggle
   - Search and filter your newly discovered resources

## 🔧 Troubleshooting

### Common Issues

**Service won't start:**
- Check MongoDB is running
- Verify environment variables
- Check port 8001 is available

**No results from scraping:**
- Check internet connection
- Verify target sites are accessible
- Check rate limiting settings

**Performance issues:**
- Reduce concurrent requests
- Increase delays between requests
- Monitor system resources

### Debug Mode

Enable debug logging:
```env
LOG_LEVEL=debug
NODE_ENV=development
```

## 🔮 Future Enhancements

- **AI-Powered Content Analysis**: Use LLMs to better categorize content
- **Custom Source Configuration**: Allow users to add their own sources
- **Scheduled Scraping**: Automatic periodic resource updates
- **Content Freshness**: Track and update outdated resources
- **Advanced Filtering**: More sophisticated content filtering
- **Collaborative Curation**: User ratings and reviews for scraped content

---

The PathWise Web Scraping System transforms static resource libraries into dynamic, ever-growing collections of educational content, ensuring users always have access to the latest and most relevant learning materials.
