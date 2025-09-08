// Quick test to verify chatbot connection
const axios = require('axios');

async function testChatbotConnection() {
    console.log('🧪 Testing Chatbot Connection...');
    
    try {
        // Test health endpoint
        const healthResponse = await axios.get('http://localhost:8004/health');
        console.log('✅ Health check passed:', healthResponse.data);
        
        // Test chat endpoint
        const chatResponse = await axios.post('http://localhost:8004/chat', {
            message: 'Hello, test message',
            user_id: 'test_user'
        });
        
        console.log('✅ Chat test passed:', {
            response: chatResponse.data.response.substring(0, 50) + '...',
            confidence: chatResponse.data.confidence,
            suggestions: chatResponse.data.suggestions.length
        });
        
        console.log('🎉 Chatbot is working correctly!');
        
    } catch (error) {
        console.error('❌ Chatbot test failed:', error.message);
        console.log('💡 Make sure the chatbot service is running on port 8004');
    }
}

testChatbotConnection();
