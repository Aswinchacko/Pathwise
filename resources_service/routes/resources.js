const express = require('express');
const { query } = require('express-validator');
const Resource = require('../models/Resource');

const router = express.Router();

// GET /api/resources - list recent active resources
router.get('/', async (req, res, next) => {
  try {
    const items = await Resource.find({ isActive: true })
      .sort({ lastScraped: -1 })
      .limit(200)
      .lean();
    res.json({ resources: items });
  } catch (err) {
    next(err);
  }
});

// GET /api/resources/search?q=... - text search by title/desc
router.get('/search', query('q').isString().trim().notEmpty(), async (req, res, next) => {
  try {
    const q = req.query.q;
    const items = await Resource.find({
      isActive: true,
      $or: [
        { title: { $regex: q, $options: 'i' } },
        { description: { $regex: q, $options: 'i' } },
      ],
    })
      .sort({ lastScraped: -1 })
      .limit(200)
      .lean();
    res.json({ resources: items });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
