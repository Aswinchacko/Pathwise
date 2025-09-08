const axios = require('axios');
const cheerio = require('cheerio');
const puppeteer = require('puppeteer');
const Resource = require('../models/Resource');
const logger = require('../utils/logger');

class WebScrapingService {
  constructor() {
    this.browser = null;
    this.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36';
    this.delay = 2000; // 2 seconds between requests
    this.maxRetries = 3;
    
    // Predefined sources for different types of resources
    this.scrapingSources = {
      github: {
        name: 'GitHub',
        baseUrl: 'https://github.com/search',
        scraper: this.scrapeGitHub.bind(this)
      },
      freeCodeCamp: {
        name: 'freeCodeCamp',
        baseUrl: 'https://www.freecodecamp.org',
        scraper: this.scrapeFreeCodeCamp.bind(this)
      },
      mdn: {
        name: 'MDN Web Docs',
        baseUrl: 'https://developer.mozilla.org',
        scraper: this.scrapeMDN.bind(this)
      },
      coursera: {
        name: 'Coursera',
        baseUrl: 'https://www.coursera.org',
        scraper: this.scrapeCoursera.bind(this)
      },
      youtube: {
        name: 'YouTube',
        baseUrl: 'https://www.youtube.com',
        scraper: this.scrapeYouTube.bind(this)
      },
      medium: {
        name: 'Medium',
        baseUrl: 'https://medium.com',
        scraper: this.scrapeMedium.bind(this)
      }
    };
  }

  async initBrowser() {
    if (!this.browser) {
      this.browser = await puppeteer.launch({
        headless: true,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--no-first-run',
          '--no-zygote',
          '--disable-gpu'
        ]
      });
    }
    return this.browser;
  }

  async closeBrowser() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }

  async makeRequest(url, options = {}) {
    const config = {
      method: 'GET',
      url,
      headers: {
        'User-Agent': this.userAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
      },
      timeout: 10000,
      ...options
    };

    try {
      const response = await axios(config);
      return response.data;
    } catch (error) {
      logger.error(`Request failed for ${url}:`, error.message);
      throw error;
    }
  }

  async scrapeWithPuppeteer(url, selector = null) {
    const browser = await this.initBrowser();
    const page = await browser.newPage();
    
    try {
      await page.setUserAgent(this.userAgent);
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      
      if (selector) {
        await page.waitForSelector(selector, { timeout: 10000 });
      }
      
      const content = await page.content();
      return content;
    } finally {
      await page.close();
    }
  }

  async scrapeResourcesFromQuery(query, domain = null, options = {}) {
    const { maxResults = 50, includeVideo = true, includeArticles = true } = options;
    const allResources = [];
    
    logger.info(`🔍 Starting resource scraping for: ${query}`);

    // Scrape from multiple sources
    for (const [sourceName, sourceConfig] of Object.entries(this.scrapingSources)) {
      try {
        logger.info(`📡 Scraping from ${sourceConfig.name}...`);
        
        const resources = await sourceConfig.scraper(query, domain, {
          maxResults: Math.ceil(maxResults / Object.keys(this.scrapingSources).length)
        });
        
        allResources.push(...resources);
        logger.info(`✅ Found ${resources.length} resources from ${sourceConfig.name}`);
        
        // Delay between sources
        await this.sleep(this.delay);
      } catch (error) {
        logger.error(`❌ Error scraping ${sourceConfig.name}:`, error.message);
      }
    }

    // Process and deduplicate resources
    const processedResources = await this.processAndSaveResources(allResources, domain);
    
    logger.info(`🎉 Scraping completed: ${processedResources.length} unique resources found`);
    return processedResources;
  }

  async scrapeGitHub(query, domain, options = {}) {
    const resources = [];
    const searchUrl = `https://github.com/search?q=${encodeURIComponent(query)}&type=repositories`;
    
    try {
      const html = await this.scrapeWithPuppeteer(searchUrl, '.repo-list-item');
      const $ = cheerio.load(html);
      
      $('.repo-list-item').each((index, element) => {
        if (index >= options.maxResults) return false;
        
        const $item = $(element);
        const title = $item.find('h3 a').text().trim();
        const description = $item.find('p').text().trim();
        const url = 'https://github.com' + $item.find('h3 a').attr('href');
        const stars = $item.find('[aria-label*="star"]').text().trim();
        
        if (title && url) {
          resources.push({
            title,
            description: description || `GitHub repository for ${title}`,
            url,
            type: 'Project',
            difficulty: this.inferDifficulty(description, stars),
            duration: 'Variable',
            source: 'GitHub',
            domain: domain || this.inferDomain(title, description),
            skill: query,
            metadata: {
              stars: stars,
              author: title.split('/')[0],
              language: 'Multiple'
            }
          });
        }
      });
    } catch (error) {
      logger.error('GitHub scraping error:', error.message);
    }
    
    return resources;
  }

  async scrapeFreeCodeCamp(query, domain, options = {}) {
    const resources = [];
    
    try {
      // Search freeCodeCamp curriculum and articles
      const searchUrl = `https://www.freecodecamp.org/news/search/?query=${encodeURIComponent(query)}`;
      const html = await this.makeRequest(searchUrl);
      const $ = cheerio.load(html);
      
      $('.post-card').each((index, element) => {
        if (index >= options.maxResults) return false;
        
        const $item = $(element);
        const title = $item.find('.post-card-title').text().trim();
        const description = $item.find('.post-card-excerpt').text().trim();
        const url = 'https://www.freecodecamp.org' + $item.find('a').attr('href');
        const readTime = $item.find('.post-card-meta time').text().trim();
        
        if (title && url) {
          resources.push({
            title,
            description: description || `freeCodeCamp article about ${query}`,
            url,
            type: 'Tutorial',
            difficulty: 'Beginner',
            duration: readTime || '10 min',
            source: 'freeCodeCamp',
            domain: domain || this.inferDomain(title, description),
            skill: query,
            metadata: {
              author: 'freeCodeCamp',
              language: 'English'
            }
          });
        }
      });
    } catch (error) {
      logger.error('freeCodeCamp scraping error:', error.message);
    }
    
    return resources;
  }

  async scrapeMDN(query, domain, options = {}) {
    const resources = [];
    
    try {
      const searchUrl = `https://developer.mozilla.org/en-US/search?q=${encodeURIComponent(query)}`;
      const html = await this.makeRequest(searchUrl);
      const $ = cheerio.load(html);
      
      $('.result-item').each((index, element) => {
        if (index >= options.maxResults) return false;
        
        const $item = $(element);
        const title = $item.find('h2 a').text().trim();
        const description = $item.find('.result-excerpt').text().trim();
        const url = $item.find('h2 a').attr('href');
        
        if (title && url) {
          const fullUrl = url.startsWith('http') ? url : `https://developer.mozilla.org${url}`;
          
          resources.push({
            title,
            description: description || `MDN documentation for ${query}`,
            url: fullUrl,
            type: 'Documentation',
            difficulty: 'Intermediate',
            duration: '30 min',
            source: 'MDN Web Docs',
            domain: domain || 'Web Development',
            skill: query,
            metadata: {
              author: 'Mozilla',
              language: 'English'
            }
          });
        }
      });
    } catch (error) {
      logger.error('MDN scraping error:', error.message);
    }
    
    return resources;
  }

  async scrapeCoursera(query, domain, options = {}) {
    const resources = [];
    
    try {
      const searchUrl = `https://www.coursera.org/search?query=${encodeURIComponent(query)}`;
      const html = await this.scrapeWithPuppeteer(searchUrl, '[data-testid="search-results"]');
      const $ = cheerio.load(html);
      
      $('[data-testid="search-filter-group-PRODUCTS"] [data-click-key="search.click.result"]').each((index, element) => {
        if (index >= options.maxResults) return false;
        
        const $item = $(element);
        const title = $item.find('h3').text().trim();
        const description = $item.find('p').first().text().trim();
        const url = $item.attr('href');
        const rating = $item.find('[aria-label*="stars"]').length;
        
        if (title && url) {
          const fullUrl = url.startsWith('http') ? url : `https://www.coursera.org${url}`;
          
          resources.push({
            title,
            description: description || `Coursera course about ${query}`,
            url: fullUrl,
            type: 'Course',
            difficulty: 'Intermediate',
            duration: '4-6 weeks',
            source: 'Coursera',
            domain: domain || this.inferDomain(title, description),
            skill: query,
            rating: rating,
            metadata: {
              platform: 'Coursera',
              language: 'English'
            }
          });
        }
      });
    } catch (error) {
      logger.error('Coursera scraping error:', error.message);
    }
    
    return resources;
  }

  async scrapeYouTube(query, domain, options = {}) {
    const resources = [];
    
    try {
      // Note: YouTube requires API key for proper search
      // This is a simplified version using direct URL construction
      const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(query + ' tutorial')}`;
      const html = await this.scrapeWithPuppeteer(searchUrl, '#contents');
      const $ = cheerio.load(html);
      
      // Extract video data from script tags (YouTube uses dynamic loading)
      const scriptTags = $('script').toArray();
      
      for (const script of scriptTags) {
        const content = $(script).html();
        if (content && content.includes('videoRenderer')) {
          try {
            // Parse video data from YouTube's JSON
            const videoMatches = content.match(/"videoRenderer":\{[^}]+\}/g);
            if (videoMatches) {
              videoMatches.slice(0, options.maxResults).forEach(match => {
                try {
                  const videoData = JSON.parse('{' + match.substring(1) + '}');
                  const videoRenderer = videoData.videoRenderer;
                  
                  if (videoRenderer) {
                    const title = videoRenderer.title?.runs?.[0]?.text;
                    const videoId = videoRenderer.videoId;
                    const duration = videoRenderer.lengthText?.simpleText;
                    const viewCount = videoRenderer.viewCountText?.simpleText;
                    
                    if (title && videoId) {
                      resources.push({
                        title,
                        description: `YouTube tutorial about ${query}`,
                        url: `https://www.youtube.com/watch?v=${videoId}`,
                        type: 'Video',
                        difficulty: 'Beginner',
                        duration: duration || '10 min',
                        source: 'YouTube',
                        domain: domain || this.inferDomain(title, ''),
                        skill: query,
                        metadata: {
                          views: viewCount,
                          platform: 'YouTube'
                        }
                      });
                    }
                  }
                } catch (parseError) {
                  // Skip malformed data
                }
              });
            }
          } catch (error) {
            // Continue with other scripts
          }
        }
      }
    } catch (error) {
      logger.error('YouTube scraping error:', error.message);
    }
    
    return resources;
  }

  async scrapeMedium(query, domain, options = {}) {
    const resources = [];
    
    try {
      const searchUrl = `https://medium.com/search?q=${encodeURIComponent(query)}`;
      const html = await this.makeRequest(searchUrl);
      const $ = cheerio.load(html);
      
      $('article').each((index, element) => {
        if (index >= options.maxResults) return false;
        
        const $item = $(element);
        const title = $item.find('h2').text().trim();
        const description = $item.find('p').first().text().trim();
        const url = $item.find('a').attr('href');
        const readTime = $item.find('[data-testid="storyReadTime"]').text().trim();
        const author = $item.find('[data-testid="authorName"]').text().trim();
        
        if (title && url) {
          const fullUrl = url.startsWith('http') ? url : `https://medium.com${url}`;
          
          resources.push({
            title,
            description: description || `Medium article about ${query}`,
            url: fullUrl,
            type: 'Article',
            difficulty: 'Intermediate',
            duration: readTime || '5 min read',
            source: 'Medium',
            domain: domain || this.inferDomain(title, description),
            skill: query,
            metadata: {
              author: author || 'Medium Author',
              platform: 'Medium'
            }
          });
        }
      });
    } catch (error) {
      logger.error('Medium scraping error:', error.message);
    }
    
    return resources;
  }

  async processAndSaveResources(resources, domain) {
    const processedResources = [];
    const seenUrls = new Set();
    
    for (const resource of resources) {
      // Skip duplicates
      if (seenUrls.has(resource.url)) continue;
      seenUrls.add(resource.url);
      
      // Generate unique ID
      const id = this.generateResourceId(resource.title, resource.source);
      
      // Validate and clean data
      const processedResource = {
        id,
        title: this.cleanTitle(resource.title),
        description: this.cleanDescription(resource.description),
        url: resource.url,
        type: resource.type || 'Tutorial',
        difficulty: resource.difficulty || 'Beginner',
        duration: resource.duration || '30 min',
        domain: resource.domain || domain || 'General',
        skill: resource.skill,
        source: resource.source,
        color: this.getColorForType(resource.type),
        tags: this.extractTags(resource.title, resource.description),
        rating: resource.rating || 0,
        isActive: true,
        lastScraped: new Date(),
        metadata: resource.metadata || {}
      };
      
      try {
        // Check if resource already exists
        const existingResource = await Resource.findOne({ url: resource.url });
        
        if (existingResource) {
          // Update existing resource
          await Resource.findByIdAndUpdate(existingResource._id, {
            ...processedResource,
            lastScraped: new Date()
          });
        } else {
          // Create new resource
          const newResource = new Resource(processedResource);
          await newResource.save();
          processedResources.push(processedResource);
        }
      } catch (error) {
        logger.error(`Error saving resource ${resource.title}:`, error.message);
      }
    }
    
    return processedResources;
  }

  // Helper methods
  generateResourceId(title, source) {
    const cleanTitle = title.toLowerCase().replace(/[^a-z0-9]/g, '-');
    const cleanSource = source.toLowerCase().replace(/[^a-z0-9]/g, '-');
    return `${cleanSource}-${cleanTitle}-${Date.now()}`;
  }

  cleanTitle(title) {
    return title.trim().substring(0, 200);
  }

  cleanDescription(description) {
    return description.trim().substring(0, 1000);
  }

  inferDifficulty(description, stars = '') {
    const text = (description + ' ' + stars).toLowerCase();
    
    if (text.includes('beginner') || text.includes('intro') || text.includes('basic') || text.includes('getting started')) {
      return 'Beginner';
    }
    
    if (text.includes('advanced') || text.includes('expert') || text.includes('master') || text.includes('deep dive')) {
      return 'Advanced';
    }
    
    return 'Intermediate';
  }

  inferDomain(title, description) {
    const text = (title + ' ' + description).toLowerCase();
    
    if (text.includes('react') || text.includes('vue') || text.includes('angular') || text.includes('frontend') || text.includes('css') || text.includes('html') || text.includes('javascript')) {
      return 'Frontend Development';
    }
    
    if (text.includes('node') || text.includes('express') || text.includes('backend') || text.includes('api') || text.includes('server')) {
      return 'Backend Development';
    }
    
    if (text.includes('python') || text.includes('machine learning') || text.includes('data science') || text.includes('ai')) {
      return 'Data Science & AI';
    }
    
    if (text.includes('mobile') || text.includes('android') || text.includes('ios') || text.includes('react native') || text.includes('flutter')) {
      return 'Mobile Development';
    }
    
    if (text.includes('devops') || text.includes('docker') || text.includes('kubernetes') || text.includes('aws') || text.includes('cloud')) {
      return 'DevOps & Cloud';
    }
    
    return 'General';
  }

  getColorForType(type) {
    const colors = {
      'Tutorial': '#10B981',
      'Course': '#3B82F6',
      'Documentation': '#6366F1',
      'Interactive': '#F59E0B',
      'Book': '#8B5CF6',
      'Guide': '#06B6D4',
      'Project': '#EF4444',
      'Video': '#EC4899',
      'Article': '#84CC16'
    };
    
    return colors[type] || '#6B7280';
  }

  extractTags(title, description) {
    const text = (title + ' ' + description).toLowerCase();
    const tags = [];
    
    const commonTags = [
      'javascript', 'python', 'react', 'node.js', 'css', 'html', 'vue', 'angular',
      'machine learning', 'data science', 'api', 'database', 'mongodb', 'sql',
      'docker', 'kubernetes', 'aws', 'cloud', 'mobile', 'android', 'ios',
      'tutorial', 'beginner', 'advanced', 'guide', 'course'
    ];
    
    for (const tag of commonTags) {
      if (text.includes(tag)) {
        tags.push(tag);
      }
    }
    
    return tags.slice(0, 5); // Limit to 5 tags
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Public method to scrape specific URL
  async scrapeSpecificUrl(url, domain = null, skill = null) {
    try {
      const html = await this.makeRequest(url);
      const $ = cheerio.load(html);
      
      const title = $('title').text().trim() || $('h1').first().text().trim();
      const description = $('meta[name="description"]').attr('content') || 
                         $('meta[property="og:description"]').attr('content') || 
                         $('p').first().text().trim();
      
      const resource = {
        title: title || 'Untitled Resource',
        description: description || 'No description available',
        url,
        type: 'Article',
        difficulty: 'Intermediate',
        duration: '10 min',
        source: new URL(url).hostname,
        domain: domain || this.inferDomain(title, description),
        skill: skill || 'General',
        metadata: {
          scrapedAt: new Date(),
          directScrape: true
        }
      };
      
      return await this.processAndSaveResources([resource], domain);
    } catch (error) {
      logger.error(`Error scraping URL ${url}:`, error.message);
      throw error;
    }
  }
}

module.exports = WebScrapingService;
