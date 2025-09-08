const express = require('express');
const { body, query, validationResult } = require('express-validator');
const WebScrapingService = require('../services/WebScrapingService');
const Resource = require('../models/Resource');
const logger = require('../utils/logger');

const router = express.Router();
const scrapingService = new WebScrapingService();

// POST /api/scraping/resources - Scrape resources for a query
router.post('/resources', [
  body('query').notEmpty().trim().isLength({ min: 2, max: 100 }),
  body('domain').optional().trim().isLength({ max: 50 }),
  body('maxResults').optional().isInt({ min: 1, max: 100 }),
  body('includeVideo').optional().isBoolean(),
  body('includeArticles').optional().isBoolean()
], async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const { query, domain, maxResults = 50, includeVideo = true, includeArticles = true } = req.body;

    logger.info(`🔍 Starting resource scraping for query: ${query}`);

    const resources = await scrapingService.scrapeResourcesFromQuery(query, domain, {
      maxResults,
      includeVideo,
      includeArticles
    });

    res.json({
      success: true,
      message: `Successfully scraped ${resources.length} resources`,
      data: {
        query,
        domain,
        resourcesFound: resources.length,
        resources: resources.slice(0, 20) // Return first 20 for preview
      }
    });

  } catch (error) {
    logger.error('Resource scraping error:', error);
    next(error);
  }
});

// POST /api/scraping/url - Scrape a specific URL
router.post('/url', [
  body('url').isURL().withMessage('Must be a valid URL'),
  body('domain').optional().trim().isLength({ max: 50 }),
  body('skill').optional().trim().isLength({ max: 100 })
], async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const { url, domain, skill } = req.body;

    logger.info(`🔗 Scraping specific URL: ${url}`);

    const resources = await scrapingService.scrapeSpecificUrl(url, domain, skill);

    res.json({
      success: true,
      message: 'Successfully scraped URL',
      data: {
        url,
        resourcesFound: resources.length,
        resources
      }
    });

  } catch (error) {
    logger.error('URL scraping error:', error);
    next(error);
  }
});

// GET /api/scraping/bulk - Bulk scrape resources for multiple queries
router.post('/bulk', [
  body('queries').isArray({ min: 1, max: 10 }).withMessage('Must provide 1-10 queries'),
  body('queries.*').notEmpty().trim().isLength({ min: 2, max: 100 }),
  body('domain').optional().trim().isLength({ max: 50 }),
  body('maxResultsPerQuery').optional().isInt({ min: 1, max: 50 })
], async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const { queries, domain, maxResultsPerQuery = 20 } = req.body;

    logger.info(`🔍 Starting bulk resource scraping for ${queries.length} queries`);

    const results = [];
    let totalResources = 0;

    for (const query of queries) {
      try {
        const resources = await scrapingService.scrapeResourcesFromQuery(query, domain, {
          maxResults: maxResultsPerQuery
        });

        results.push({
          query,
          resourcesFound: resources.length,
          resources: resources.slice(0, 5) // Preview only
        });

        totalResources += resources.length;

        // Small delay between queries
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        logger.error(`Error scraping query "${query}":`, error.message);
        results.push({
          query,
          error: error.message,
          resourcesFound: 0,
          resources: []
        });
      }
    }

    res.json({
      success: true,
      message: `Bulk scraping completed. Found ${totalResources} total resources`,
      data: {
        totalQueries: queries.length,
        totalResourcesFound: totalResources,
        results
      }
    });

  } catch (error) {
    logger.error('Bulk scraping error:', error);
    next(error);
  }
});

// GET /api/scraping/sources - Get available scraping sources
router.get('/sources', (req, res) => {
  const sources = [
    {
      name: 'GitHub',
      description: 'Open source repositories and projects',
      types: ['Project', 'Tutorial'],
      active: true
    },
    {
      name: 'freeCodeCamp',
      description: 'Free coding tutorials and articles',
      types: ['Tutorial', 'Article'],
      active: true
    },
    {
      name: 'MDN Web Docs',
      description: 'Web development documentation',
      types: ['Documentation'],
      active: true
    },
    {
      name: 'Coursera',
      description: 'Online courses and specializations',
      types: ['Course'],
      active: true
    },
    {
      name: 'YouTube',
      description: 'Video tutorials and lectures',
      types: ['Video'],
      active: true
    },
    {
      name: 'Medium',
      description: 'Articles and blog posts',
      types: ['Article'],
      active: true
    }
  ];

  res.json({
    success: true,
    data: { sources }
  });
});

// GET /api/scraping/stats - Get scraping statistics
router.get('/stats', async (req, res, next) => {
  try {
    const stats = await Resource.aggregate([
      {
        $group: {
          _id: '$source',
          count: { $sum: 1 },
          lastScraped: { $max: '$lastScraped' }
        }
      },
      {
        $sort: { count: -1 }
      }
    ]);

    const totalResources = await Resource.countDocuments({ isActive: true });
    const recentlyScraped = await Resource.countDocuments({
      lastScraped: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    });

    res.json({
      success: true,
      data: {
        totalResources,
        recentlyScraped,
        sourceStats: stats
      }
    });

  } catch (error) {
    logger.error('Stats error:', error);
    next(error);
  }
});

// DELETE /api/scraping/cleanup - Clean up old/inactive resources
router.delete('/cleanup', [
  query('olderThan').optional().isInt({ min: 1, max: 365 }).withMessage('Must be between 1-365 days'),
  query('dryRun').optional().isBoolean()
], async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const { olderThan = 30, dryRun = false } = req.query;
    const cutoffDate = new Date(Date.now() - olderThan * 24 * 60 * 60 * 1000);

    const query = {
      $or: [
        { isActive: false },
        { lastScraped: { $lt: cutoffDate } }
      ]
    };

    if (dryRun === 'true') {
      const count = await Resource.countDocuments(query);
      res.json({
        success: true,
        message: `Would delete ${count} resources (dry run)`,
        data: { count, cutoffDate, dryRun: true }
      });
    } else {
      const result = await Resource.deleteMany(query);
      res.json({
        success: true,
        message: `Deleted ${result.deletedCount} old/inactive resources`,
        data: { deletedCount: result.deletedCount, cutoffDate }
      });
    }

  } catch (error) {
    logger.error('Cleanup error:', error);
    next(error);
  }
});

module.exports = router;