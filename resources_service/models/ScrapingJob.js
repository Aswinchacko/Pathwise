const mongoose = require('mongoose');

const scrapingJobSchema = new mongoose.Schema({
  id: {
    type: String,
    required: true,
    unique: true
  },
  source: {
    type: String,
    required: true,
    trim: true
  },
  status: {
    type: String,
    enum: ['pending', 'running', 'completed', 'failed', 'cancelled'],
    default: 'pending',
    index: true
  },
  startedAt: {
    type: Date,
    default: Date.now
  },
  completedAt: {
    type: Date
  },
  duration: {
    type: Number // in milliseconds
  },
  resourcesFound: {
    type: Number,
    default: 0
  },
  resourcesAdded: {
    type: Number,
    default: 0
  },
  resourcesUpdated: {
    type: Number,
    default: 0
  },
  errors: [{
    message: String,
    timestamp: {
      type: Date,
      default: Date.now
    },
    url: String
  }],
  configuration: {
    maxPages: Number,
    delay: Number,
    userAgent: String,
    timeout: Number
  },
  metadata: {
    totalPages: Number,
    processedPages: Number,
    skippedPages: Number,
    duplicateResources: Number
  }
}, {
  timestamps: true
});

// Indexes
scrapingJobSchema.index({ status: 1, startedAt: -1 });
scrapingJobSchema.index({ source: 1, status: 1 });

// Pre-save middleware to generate ID
scrapingJobSchema.pre('save', function(next) {
  if (!this.id) {
    this.id = `job-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  next();
});

// Method to mark job as completed
scrapingJobSchema.methods.markCompleted = function() {
  this.status = 'completed';
  this.completedAt = new Date();
  this.duration = this.completedAt - this.startedAt;
  return this.save();
};

// Method to mark job as failed
scrapingJobSchema.methods.markFailed = function(error) {
  this.status = 'failed';
  this.completedAt = new Date();
  this.duration = this.completedAt - this.startedAt;
  this.errors.push({
    message: error.message || error,
    timestamp: new Date()
  });
  return this.save();
};

// Method to add error
scrapingJobSchema.methods.addError = function(message, url = null) {
  this.errors.push({
    message,
    url,
    timestamp: new Date()
  });
  return this.save();
};

// Static method to get job statistics
scrapingJobSchema.statics.getStats = function() {
  return this.aggregate([
    {
      $group: {
        _id: '$status',
        count: { $sum: 1 },
        avgDuration: { $avg: '$duration' },
        totalResources: { $sum: '$resourcesAdded' }
      }
    }
  ]);
};

module.exports = mongoose.model('ScrapingJob', scrapingJobSchema);

