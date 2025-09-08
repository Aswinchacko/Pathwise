// Quick test for the resources service
import resourcesService from './dashboard/src/services/resourcesService.js';

console.log('Testing Resources Service...\n');

// Test 1: Get all resources
console.log('1. Testing getAllResources():');
const allResources = resourcesService.getAllResources();
console.log(`Found ${allResources.length} total resources`);

// Test 2: Get resources for a specific skill
console.log('\n2. Testing getResourcesForSkill("React"):');
const reactResources = resourcesService.getResourcesForSkill('React');
console.log(`Found ${reactResources.length} React resources:`);
reactResources.forEach(resource => {
  console.log(`  - ${resource.title} (${resource.type})`);
});

// Test 3: Search resources
console.log('\n3. Testing searchResources("JavaScript"):');
const jsResources = resourcesService.searchResources('JavaScript');
console.log(`Found ${jsResources.length} JavaScript resources`);

// Test 4: Get resources by type
console.log('\n4. Testing getResourcesByType("Tutorial"):');
const tutorials = resourcesService.getResourcesByType('Tutorial');
console.log(`Found ${tutorials.length} tutorials`);

// Test 5: Get resources by difficulty
console.log('\n5. Testing getResourcesByDifficulty("Beginner"):');
const beginnerResources = resourcesService.getResourcesByDifficulty('Beginner');
console.log(`Found ${beginnerResources.length} beginner resources`);

// Test 6: Get resource statistics
console.log('\n6. Testing getResourceStats():');
const stats = resourcesService.getResourceStats();
console.log('Resource Statistics:');
console.log(`  Total: ${stats.total}`);
console.log(`  By Type:`, stats.byType);
console.log(`  By Difficulty:`, stats.byDifficulty);
console.log(`  By Duration:`, stats.byDuration);

console.log('\n✅ Resources service test completed successfully!');
