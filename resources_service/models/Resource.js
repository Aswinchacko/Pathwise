const mongoose = require('mongoose');

const resourceSchema = new mongoose.Schema({
  id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  title: {
    type: String,
    required: true,
    trim: true,
    maxlength: 200
  },
  description: {
    type: String,
    required: true,
    trim: true,
    maxlength: 1000
  },
  url: {
    type: String,
    required: true,
    validate: {
      validator: function(v) {
        return /^https?:\/\/.+/.test(v);
      },
      message: 'URL must be a valid HTTP/HTTPS link'
    }
  },
  type: {
    type: String,
    required: true,
    enum: ['Tutorial', 'Course', 'Documentation', 'Interactive', 'Book', 'Guide', 'Project', 'Video', 'Article', 'Tool'],
    index: true
  },
  difficulty: {
    type: String,
    required: true,
    enum: ['Beginner', 'Intermediate', 'Advanced'],
    index: true
  },
  duration: {
    type: String,
    required: true,
    trim: true
  },
  domain: {
    type: String,
    required: true,
    trim: true,
    index: true
  },
  skill: {
    type: String,
    required: true,
    trim: true,
    index: true
  },
  color: {
    type: String,
    default: '#3B82F6'
  },
  source: {
    type: String,
    required: true,
    trim: true
  },
  tags: [{
    type: String,
    trim: true
  }],
  rating: {
    type: Number,
    min: 0,
    max: 5,
    default: 0
  },
  views: {
    type: Number,
    default: 0
  },
  isActive: {
    type: Boolean,
    default: true,
    index: true
  },
  lastScraped: {
    type: Date,
    default: Date.now
  },
  metadata: {
    author: String,
    language: String,
    lastUpdated: Date,
    price: String,
    prerequisites: [String],
    learningOutcomes: [String]
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes for better query performance
resourceSchema.index({ domain: 1, skill: 1 });
resourceSchema.index({ type: 1, difficulty: 1 });
resourceSchema.index({ title: 'text', description: 'text' });
resourceSchema.index({ isActive: 1, domain: 1 });

// Virtual for formatted duration
resourceSchema.virtual('formattedDuration').get(function() {
  return this.duration;
});

// Pre-save middleware to generate ID if not provided
resourceSchema.pre('save', function(next) {
  if (!this.id) {
    this.id = `${this.domain.toLowerCase().replace(/\s+/g, '-')}-${this.skill.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`;
  }
  next();
});

// Static method to find resources by domain
resourceSchema.statics.findByDomain = function(domain) {
  return this.find({ domain: new RegExp(domain, 'i'), isActive: true });
};

// Static method to find resources by skill
resourceSchema.statics.findBySkill = function(skill) {
  return this.find({ skill: new RegExp(skill, 'i'), isActive: true });
};

// Static method to search resources
resourceSchema.statics.search = function(query, filters = {}) {
  const searchQuery = {
    isActive: true,
    ...filters
  };

  if (query) {
    searchQuery.$text = { $search: query };
  }

  return this.find(searchQuery, { score: { $meta: 'textScore' } })
    .sort({ score: { $meta: 'textScore' } });
};

// Instance method to increment views
resourceSchema.methods.incrementViews = function() {
  this.views += 1;
  return this.save();
};

module.exports = mongoose.model('Resource', resourceSchema);

