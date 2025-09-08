const WebScraper = require('./WebScraper');
const Resource = require('../models/Resource');
const ScrapingJob = require('../models/ScrapingJob');
const logger = require('../utils/logger');

class ResourceScraper {
  constructor() {
    this.webScraper = new WebScraper();
    this.scrapingSources = [
      {
        name: 'MDN Web Docs',
        baseUrl: 'https://developer.mozilla.org',
        searchUrl: 'https://developer.mozilla.org/en-US/search?q=',
        type: 'Documentation',
        difficulty: 'Beginner',
        domain: 'Web Development'
      },
      {
        name: 'freeCodeCamp',
        baseUrl: 'https://www.freecodecamp.org',
        searchUrl: 'https://www.freecodecamp.org/news/search/',
        type: 'Course',
        difficulty: 'Beginner',
        domain: 'Programming'
      },
      {
        name: 'Stack Overflow',
        baseUrl: 'https://stackoverflow.com',
        searchUrl: 'https://stackoverflow.com/questions/tagged/',
        type: 'Article',
        difficulty: 'Intermediate',
        domain: 'Programming'
      },
      {
        name: 'GitHub',
        baseUrl: 'https://github.com',
        searchUrl: 'https://github.com/search?q=',
        type: 'Project',
        difficulty: 'Intermediate',
        domain: 'Programming'
      },
      {
        name: 'YouTube',
        baseUrl: 'https://www.youtube.com',
        searchUrl: 'https://www.youtube.com/results?search_query=',
        type: 'Video',
        difficulty: 'Beginner',
        domain: 'Programming'
      }
    ];
  }

  async init() {
    await this.webScraper.init();
  }

  async close() {
    await this.webScraper.close();
  }

  async scrapeResources(query, domain = null, options = {}) {
    const job = new ScrapingJob({
      source: 'multi-source',
      configuration: {
        maxPages: options.maxPages || 10,
        delay: options.delay || 2000,
        userAgent: process.env.USER_AGENT,
        timeout: 30000
      }
    });

    try {
      await job.save();
      job.status = 'running';
      await job.save();

      logger.info(`🔍 Starting resource scraping for query: ${query}`);

      const allResources = [];
      const errors = [];

      for (const source of this.scrapingSources) {
        try {
          logger.info(`📡 Scraping from ${source.name}...`);
          
          const resources = await this.scrapeFromSource(source, query, domain, options);
          allResources.push(...resources);
          
          job.resourcesFound += resources.length;
          logger.info(`✅ Found ${resources.length} resources from ${source.name}`);

          // Add delay between sources
          await this.webScraper.delay(1000);
        } catch (error) {
          logger.error(`❌ Error scraping ${source.name}:`, error);
          errors.push({
            source: source.name,
            error: error.message,
            timestamp: new Date()
          });
          job.addError(`Failed to scrape ${source.name}: ${error.message}`);
        }
      }

      // Process and save resources
      const processedResources = await this.processResources(allResources, domain);
      
      job.resourcesAdded = processedResources.added;
      job.resourcesUpdated = processedResources.updated;
      job.metadata = {
        totalPages: this.scrapingSources.length,
        processedPages: this.scrapingSources.length - errors.length,
        skippedPages: errors.length,
        duplicateResources: allResources.length - processedResources.added - processedResources.updated
      };

      await job.markCompleted();
      
      logger.info(`🎉 Scraping completed: ${processedResources.added} added, ${processedResources.updated} updated`);

      return {
        success: true,
        jobId: job.id,
        resourcesAdded: processedResources.added,
        resourcesUpdated: processedResources.updated,
        totalFound: allResources.length,
        errors: errors.length
      };

    } catch (error) {
      logger.error('Scraping job failed:', error);
      await job.markFailed(error);
      
      return {
        success: false,
        jobId: job.id,
        error: error.message
      };
    }
  }

  async scrapeFromSource(source, query, domain, options) {
    const resources = [];
    const searchQuery = `${query} ${domain || ''}`.trim();
    const searchUrl = `${source.searchUrl}${encodeURIComponent(searchQuery)}`;

    try {
      const $ = await this.webScraper.scrapeWithAxios(searchUrl);
      
      // Extract resource links based on source
      const links = this.extractLinksFromSource($, source);
      
      // Limit the number of links to process
      const limitedLinks = links.slice(0, options.maxPages || 5);
      
      for (const link of limitedLinks) {
        try {
          const resourceData = await this.webScraper.scrapeResource(link);
          
          if (resourceData) {
            // Enhance with source-specific data
            resourceData.domain = domain || source.domain;
            resourceData.skill = query;
            resourceData.type = source.type;
            resourceData.difficulty = source.difficulty;
            resourceData.source = source.name;
            resourceData.color = this.getColorForType(source.type);
            
            resources.push(resourceData);
          }

          // Add delay between requests
          await this.webScraper.delay(500);
        } catch (error) {
          logger.warn(`Failed to scrape resource ${link}:`, error.message);
        }
      }
    } catch (error) {
      logger.error(`Failed to scrape from ${source.name}:`, error);
      throw error;
    }

    return resources;
  }

  extractLinksFromSource($, source) {
    const links = [];

    switch (source.name) {
      case 'MDN Web Docs':
        $('a[href*="/en-US/docs/"]').each((i, el) => {
          const href = $(el).attr('href');
          if (href && !href.startsWith('http')) {
            links.push(`${source.baseUrl}${href}`);
          }
        });
        break;

      case 'freeCodeCamp':
        $('a[href*="/news/"]').each((i, el) => {
          const href = $(el).attr('href');
          if (href && !href.startsWith('http')) {
            links.push(`${source.baseUrl}${href}`);
          }
        });
        break;

      case 'Stack Overflow':
        $('a[href*="/questions/"]').each((i, el) => {
          const href = $(el).attr('href');
          if (href && !href.startsWith('http')) {
            links.push(`${source.baseUrl}${href}`);
          }
        });
        break;

      case 'GitHub':
        $('a[href*="/"]').each((i, el) => {
          const href = $(el).attr('href');
          if (href && !href.startsWith('http') && href.includes('/')) {
            links.push(`${source.baseUrl}${href}`);
          }
        });
        break;

      case 'YouTube':
        $('a[href*="/watch"]').each((i, el) => {
          const href = $(el).attr('href');
          if (href && !href.startsWith('http')) {
            links.push(`${source.baseUrl}${href}`);
          }
        });
        break;

      default:
        $('a[href]').each((i, el) => {
          const href = $(el).attr('href');
          if (href && href.startsWith('http')) {
            links.push(href);
          }
        });
    }

    return [...new Set(links)]; // Remove duplicates
  }

  async processResources(resources, domain) {
    let added = 0;
    let updated = 0;

    for (const resourceData of resources) {
      try {
        // Check if resource already exists
        const existingResource = await Resource.findOne({ url: resourceData.url });
        
        if (existingResource) {
          // Update existing resource
          Object.assign(existingResource, resourceData);
          existingResource.lastScraped = new Date();
          await existingResource.save();
          updated++;
        } else {
          // Create new resource
          const resource = new Resource({
            ...resourceData,
            id: this.generateResourceId(resourceData),
            domain: domain || resourceData.domain,
            skill: resourceData.skill || 'General',
            isActive: true
          });
          
          await resource.save();
          added++;
        }
      } catch (error) {
        logger.error('Failed to process resource:', error);
      }
    }

    return { added, updated };
  }

  generateResourceId(resourceData) {
    const domain = resourceData.domain?.toLowerCase().replace(/\s+/g, '-') || 'general';
    const skill = resourceData.skill?.toLowerCase().replace(/\s+/g, '-') || 'resource';
    const timestamp = Date.now();
    const random = Math.random().toString(36).substr(2, 5);
    
    return `${domain}-${skill}-${timestamp}-${random}`;
  }

  getColorForType(type) {
    const colors = {
      'Tutorial': '#3B82F6',
      'Course': '#10B981',
      'Documentation': '#8B5CF6',
      'Interactive': '#F59E0B',
      'Book': '#EF4444',
      'Guide': '#06B6D4',
      'Project': '#84CC16',
      'Video': '#EC4899',
      'Article': '#6B7280',
      'Tool': '#F97316'
    };
    
    return colors[type] || '#3B82F6';
  }

  async getScrapingStats() {
    try {
      const stats = await ScrapingJob.getStats();
      const totalResources = await Resource.countDocuments({ isActive: true });
      const recentJobs = await ScrapingJob.find()
        .sort({ startedAt: -1 })
        .limit(10)
        .select('id status startedAt completedAt resourcesAdded resourcesFound');

      return {
        totalResources,
        jobStats: stats,
        recentJobs
      };
    } catch (error) {
      logger.error('Failed to get scraping stats:', error);
      throw error;
    }
  }
}

module.exports = ResourceScraper;

