const puppeteer = require('puppeteer');
const axios = require('axios');
const cheerio = require('cheerio');
const logger = require('../utils/logger');
const { getRedisClient } = require('../config/redis');

class WebScraper {
  constructor() {
    this.browser = null;
    this.userAgent = process.env.USER_AGENT || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
    this.delay = parseInt(process.env.SCRAPING_DELAY) || 2000;
    this.maxConcurrent = parseInt(process.env.MAX_CONCURRENT_REQUESTS) || 5;
    this.redis = getRedisClient();
  }

  async init() {
    try {
      this.browser = await puppeteer.launch({
        headless: 'new',
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
      logger.info('🌐 WebScraper initialized successfully');
    } catch (error) {
      logger.error('Failed to initialize WebScraper:', error);
      throw error;
    }
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
      logger.info('🌐 WebScraper closed');
    }
  }

  async scrapeWithPuppeteer(url, options = {}) {
    const page = await this.browser.newPage();
    
    try {
      await page.setUserAgent(this.userAgent);
      await page.setViewport({ width: 1920, height: 1080 });
      
      // Set request interception to block unnecessary resources
      await page.setRequestInterception(true);
      page.on('request', (req) => {
        const resourceType = req.resourceType();
        if (['image', 'stylesheet', 'font', 'media'].includes(resourceType)) {
          req.abort();
        } else {
          req.continue();
        }
      });

      await page.goto(url, { 
        waitUntil: 'networkidle2',
        timeout: 30000 
      });

      // Wait for dynamic content to load
      await page.waitForTimeout(2000);

      const content = await page.content();
      return cheerio.load(content);
    } catch (error) {
      logger.error(`Failed to scrape ${url}:`, error);
      throw error;
    } finally {
      await page.close();
    }
  }

  async scrapeWithAxios(url, options = {}) {
    try {
      const response = await axios.get(url, {
        headers: {
          'User-Agent': this.userAgent,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5',
          'Accept-Encoding': 'gzip, deflate',
          'Connection': 'keep-alive',
        },
        timeout: 30000,
        maxRedirects: 5,
        ...options
      });

      return cheerio.load(response.data);
    } catch (error) {
      logger.error(`Failed to scrape ${url} with axios:`, error);
      throw error;
    }
  }

  async scrapeResource(url, usePuppeteer = false) {
    try {
      const $ = usePuppeteer ? 
        await this.scrapeWithPuppeteer(url) : 
        await this.scrapeWithAxios(url);

      return this.extractResourceData($, url);
    } catch (error) {
      logger.error(`Failed to scrape resource from ${url}:`, error);
      return null;
    }
  }

  extractResourceData($, url) {
    const data = {
      url,
      title: '',
      description: '',
      type: 'Article',
      difficulty: 'Beginner',
      duration: 'Unknown',
      source: this.extractDomain(url),
      tags: [],
      metadata: {}
    };

    // Extract title
    data.title = $('title').text().trim() || 
                 $('h1').first().text().trim() ||
                 $('meta[property="og:title"]').attr('content') ||
                 'Untitled Resource';

    // Extract description
    data.description = $('meta[name="description"]').attr('content') ||
                      $('meta[property="og:description"]').attr('content') ||
                      $('p').first().text().trim().substring(0, 200) ||
                      'No description available';

    // Extract type based on content analysis
    data.type = this.detectResourceType($, url);

    // Extract difficulty based on content analysis
    data.difficulty = this.detectDifficulty($);

    // Extract duration
    data.duration = this.extractDuration($);

    // Extract tags
    data.tags = this.extractTags($);

    // Extract metadata
    data.metadata = {
      author: $('meta[name="author"]').attr('content') || 
              $('[rel="author"]').text().trim() ||
              'Unknown',
      language: $('html').attr('lang') || 'en',
      lastUpdated: this.extractLastUpdated($),
      price: this.extractPrice($)
    };

    return data;
  }

  detectResourceType($, url) {
    const urlLower = url.toLowerCase();
    const title = $('title').text().toLowerCase();
    const content = $('body').text().toLowerCase();

    // Check URL patterns
    if (urlLower.includes('course') || urlLower.includes('tutorial')) return 'Course';
    if (urlLower.includes('docs') || urlLower.includes('documentation')) return 'Documentation';
    if (urlLower.includes('book') || urlLower.includes('ebook')) return 'Book';
    if (urlLower.includes('playground') || urlLower.includes('interactive')) return 'Interactive';
    if (urlLower.includes('project') || urlLower.includes('example')) return 'Project';
    if (urlLower.includes('video') || urlLower.includes('youtube')) return 'Video';

    // Check content patterns
    if (content.includes('tutorial') || content.includes('step by step')) return 'Tutorial';
    if (content.includes('course curriculum') || content.includes('modules')) return 'Course';
    if (content.includes('api reference') || content.includes('documentation')) return 'Documentation';
    if (content.includes('interactive') || content.includes('try it')) return 'Interactive';

    return 'Article';
  }

  detectDifficulty($) {
    const content = $('body').text().toLowerCase();
    
    if (content.includes('beginner') || content.includes('basic') || content.includes('introduction')) {
      return 'Beginner';
    }
    if (content.includes('advanced') || content.includes('expert') || content.includes('master')) {
      return 'Advanced';
    }
    if (content.includes('intermediate') || content.includes('medium')) {
      return 'Intermediate';
    }

    return 'Beginner';
  }

  extractDuration($) {
    const content = $('body').text();
    const durationRegex = /(\d+)\s*(hour|hr|minute|min|day|week|month)/gi;
    const matches = content.match(durationRegex);
    
    if (matches && matches.length > 0) {
      return matches[0];
    }

    return 'Unknown';
  }

  extractTags($) {
    const tags = [];
    
    // Extract from meta keywords
    const keywords = $('meta[name="keywords"]').attr('content');
    if (keywords) {
      tags.push(...keywords.split(',').map(tag => tag.trim()));
    }

    // Extract from content
    const content = $('body').text().toLowerCase();
    const commonTags = ['javascript', 'react', 'nodejs', 'python', 'css', 'html', 'tutorial', 'course', 'programming'];
    
    commonTags.forEach(tag => {
      if (content.includes(tag)) {
        tags.push(tag);
      }
    });

    return [...new Set(tags)].slice(0, 10); // Remove duplicates and limit to 10
  }

  extractLastUpdated($) {
    const lastModified = $('meta[http-equiv="last-modified"]').attr('content');
    if (lastModified) {
      return new Date(lastModified);
    }

    const dateRegex = /(last updated|updated|modified):\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i;
    const content = $('body').text();
    const match = content.match(dateRegex);
    
    if (match) {
      return new Date(match[2]);
    }

    return null;
  }

  extractPrice($) {
    const content = $('body').text();
    const priceRegex = /\$(\d+(?:\.\d{2})?)|free|paid/i;
    const match = content.match(priceRegex);
    
    if (match) {
      return match[0].toLowerCase().includes('free') ? 'Free' : match[0];
    }

    return 'Unknown';
  }

  extractDomain(url) {
    try {
      return new URL(url).hostname.replace('www.', '');
    } catch (error) {
      return 'unknown';
    }
  }

  async delay(ms = this.delay) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async getCachedData(key) {
    if (!this.redis) return null;
    
    try {
      const cached = await this.redis.get(key);
      return cached ? JSON.parse(cached) : null;
    } catch (error) {
      logger.error('Redis get error:', error);
      return null;
    }
  }

  async setCachedData(key, data, ttl = 3600) {
    if (!this.redis) return;
    
    try {
      await this.redis.setEx(key, ttl, JSON.stringify(data));
    } catch (error) {
      logger.error('Redis set error:', error);
    }
  }
}

module.exports = WebScraper;

