/**
 * Test script for PathWise Web Scraping System
 * Run with: node test_web_scraping.js
 */

const axios = require('axios');

const RESOURCES_API_URL = 'http://localhost:8001';

// Test configuration
const testConfig = {
  baseURL: RESOURCES_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
};

async function testHealthCheck() {
  console.log('🏥 Testing health check...');
  try {
    const response = await axios.get(`${RESOURCES_API_URL}/health`);
    console.log('✅ Health check passed:', response.data);
    return true;
  } catch (error) {
    console.log('❌ Health check failed:', error.message);
    return false;
  }
}

async function testScrapingSources() {
  console.log('🔍 Testing scraping sources...');
  try {
    const response = await axios.get(`${RESOURCES_API_URL}/api/scraping/sources`);
    console.log('✅ Scraping sources:', response.data.data.sources.length, 'sources available');
    response.data.data.sources.forEach(source => {
      console.log(`   - ${source.name}: ${source.description}`);
    });
    return true;
  } catch (error) {
    console.log('❌ Scraping sources failed:', error.message);
    return false;
  }
}

async function testQueryScraping() {
  console.log('🤖 Testing query-based scraping...');
  try {
    const response = await axios.post(`${RESOURCES_API_URL}/api/scraping/resources`, {
      query: 'React hooks tutorial',
      domain: 'Frontend Development',
      maxResults: 5
    }, testConfig);
    
    console.log('✅ Query scraping completed:', response.data.message);
    console.log(`   Resources found: ${response.data.data.resourcesFound}`);
    if (response.data.data.resources && response.data.data.resources.length > 0) {
      console.log('   Sample resources:');
      response.data.data.resources.slice(0, 3).forEach((resource, index) => {
        console.log(`   ${index + 1}. ${resource.title} (${resource.type})`);
      });
    }
    return true;
  } catch (error) {
    console.log('❌ Query scraping failed:', error.response?.data?.message || error.message);
    return false;
  }
}

async function testURLScraping() {
  console.log('🔗 Testing URL scraping...');
  try {
    const response = await axios.post(`${RESOURCES_API_URL}/api/scraping/url`, {
      url: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
      domain: 'Web Development',
      skill: 'JavaScript'
    }, testConfig);
    
    console.log('✅ URL scraping completed:', response.data.message);
    console.log(`   Resources found: ${response.data.data.resourcesFound}`);
    return true;
  } catch (error) {
    console.log('❌ URL scraping failed:', error.response?.data?.message || error.message);
    return false;
  }
}

async function testResourcesAPI() {
  console.log('📚 Testing resources API...');
  try {
    const response = await axios.get(`${RESOURCES_API_URL}/api/resources?limit=5`);
    const resources = response.data.resources || response.data || [];
    console.log('✅ Resources API working:', resources.length, 'resources retrieved');
    if (resources.length > 0) {
      console.log('   Sample resources:');
      resources.slice(0, 3).forEach((resource, index) => {
        console.log(`   ${index + 1}. ${resource.title} - ${resource.source || 'Local'}`);
      });
    }
    return true;
  } catch (error) {
    console.log('❌ Resources API failed:', error.message);
    return false;
  }
}

async function testScrapingStats() {
  console.log('📊 Testing scraping statistics...');
  try {
    const response = await axios.get(`${RESOURCES_API_URL}/api/scraping/stats`);
    console.log('✅ Scraping stats:', response.data.data);
    return true;
  } catch (error) {
    console.log('❌ Scraping stats failed:', error.message);
    return false;
  }
}

async function runAllTests() {
  console.log('🚀 Starting PathWise Web Scraping System Tests\n');
  
  const tests = [
    { name: 'Health Check', fn: testHealthCheck },
    { name: 'Scraping Sources', fn: testScrapingSources },
    { name: 'Resources API', fn: testResourcesAPI },
    { name: 'Scraping Stats', fn: testScrapingStats },
    { name: 'Query Scraping', fn: testQueryScraping },
    { name: 'URL Scraping', fn: testURLScraping }
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    console.log(`\n--- ${test.name} ---`);
    try {
      const result = await test.fn();
      if (result) {
        passed++;
      } else {
        failed++;
      }
    } catch (error) {
      console.log(`❌ ${test.name} threw an error:`, error.message);
      failed++;
    }
    
    // Add delay between tests to respect rate limits
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('🎯 Test Results Summary');
  console.log('='.repeat(50));
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📊 Total:  ${tests.length}`);
  console.log(`🎉 Success Rate: ${Math.round((passed / tests.length) * 100)}%`);
  
  if (failed === 0) {
    console.log('\n🎉 All tests passed! Web scraping system is working correctly.');
  } else {
    console.log('\n⚠️  Some tests failed. Check the logs above for details.');
    console.log('💡 Make sure the resources service is running on port 8001');
    console.log('💡 Check your MongoDB connection and environment variables');
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runAllTests().catch(error => {
    console.error('💥 Test runner crashed:', error);
    process.exit(1);
  });
}

module.exports = {
  testHealthCheck,
  testScrapingSources,
  testQueryScraping,
  testURLScraping,
  testResourcesAPI,
  testScrapingStats,
  runAllTests
};
