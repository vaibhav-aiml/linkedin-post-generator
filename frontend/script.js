// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend loaded successfully');
    checkBackendHealth();
    
    // Setup form handlers
    const postForm = document.getElementById('postForm');
    const messageForm = document.getElementById('messageForm');
    
    if (postForm) {
        postForm.addEventListener('submit', handlePostGeneration);
    }
    
    if (messageForm) {
        messageForm.addEventListener('submit', handleMessageGeneration);
    }
    
    // Setup dark mode
    setupDarkMode();
});

// Dark Mode Setup
function setupDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) return;
    
    // Check for saved preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    darkModeToggle.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', isDark);
        this.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    });
}

// Check if backend is running
async function checkBackendHealth() {
    try {
        console.log('Checking backend health...');
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('Backend is healthy:', data);
        showAlert('Backend connected successfully!', 'success');
    } catch (error) {
        console.error('Backend not reachable:', error);
        showAlert('⚠️ Backend server is not running. Please start the backend with "python app.py"', 'error');
    }
}

// Handle post generation
async function handlePostGeneration(e) {
    e.preventDefault();
    
    const topic = document.getElementById('topic').value;
    const postType = document.getElementById('postType').value;
    
    if (!topic) {
        showAlert('Please enter a topic', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        console.log('Generating post for topic:', topic, 'type:', postType);
        
        const response = await fetch(`${API_BASE_URL}/generate-post`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                type: postType
            })
        });
        
        const data = await response.json();
        console.log('Response:', data);
        
        if (data.success) {
            // Display the post
            const postContent = document.getElementById('postContent');
            postContent.innerHTML = data.post.content.replace(/\n/g, '<br>');
            
            // Display hashtags
            const hashtagsContainer = document.getElementById('postHashtags');
            if (hashtagsContainer && data.post.suggested_hashtags) {
                hashtagsContainer.innerHTML = '';
                data.post.suggested_hashtags.forEach(tag => {
                    const span = document.createElement('span');
                    span.textContent = tag;
                    hashtagsContainer.appendChild(span);
                });
            }
            
            // Show result
            document.getElementById('postResult').style.display = 'block';
            document.getElementById('postResult').scrollIntoView({ behavior: 'smooth' });
            
            showAlert('Post generated successfully!', 'success');
        } else {
            showAlert(data.error || 'Failed to generate post', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Failed to connect to backend. Make sure it\'s running on http://localhost:5000', 'error');
    } finally {
        showLoading(false);
    }
}

// Handle message generation
async function handleMessageGeneration(e) {
    e.preventDefault();
    
    const recipientName = document.getElementById('recipientName').value;
    const context = document.getElementById('messageContext').value;
    const purpose = document.getElementById('messagePurpose').value;
    
    if (!recipientName || !context) {
        showAlert('Please fill in recipient name and context', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        console.log('Generating message...');
        
        const response = await fetch(`${API_BASE_URL}/generate-message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                recipient_name: recipientName,
                context: context,
                purpose: purpose
            })
        });
        
        const data = await response.json();
        console.log('Response:', data);
        
        if (data.success) {
            // Display the message
            const messageContent = document.getElementById('messageContent');
            messageContent.innerHTML = data.message.replace(/\n/g, '<br>');
            
            // Show result
            document.getElementById('messageResult').style.display = 'block';
            document.getElementById('messageResult').scrollIntoView({ behavior: 'smooth' });
            
            showAlert('Message generated successfully!', 'success');
        } else {
            showAlert(data.error || 'Failed to generate message', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Failed to connect to backend', 'error');
    } finally {
        showLoading(false);
    }
}

// Analyze text function
async function analyzeText() {
    const text = document.getElementById('textToAnalyze').value;
    
    if (!text.trim()) {
        showAlert('Please paste some text to analyze', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        console.log('Analyzing text...');
        
        const response = await fetch(`${API_BASE_URL}/analyze-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        console.log('Analysis:', data);
        
        if (data.success) {
            displayAnalysis(data.analysis);
            showAlert('Analysis complete!', 'success');
        } else {
            showAlert(data.error || 'Failed to analyze text', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Failed to analyze text', 'error');
    } finally {
        showLoading(false);
    }
}

// Display analysis results
function displayAnalysis(analysis) {
    const analysisDiv = document.getElementById('analysisResult');
    
    if (!analysisDiv) return;
    
    analysisDiv.innerHTML = `
        <div class="analysis-stats">
            <div class="stat-box">
                <div class="stat-value">${analysis.word_count}</div>
                <div class="stat-label">Word Count</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analysis.has_question ? 'Yes' : 'No'}</div>
                <div class="stat-label">Has Question?</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analysis.has_hashtags ? 'Yes' : 'No'}</div>
                <div class="stat-label">Has Hashtags?</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analysis.is_optimal ? '✅' : '⚠️'}</div>
                <div class="stat-label">Optimal Length</div>
            </div>
        </div>
        ${analysis.suggestions && analysis.suggestions.length > 0 ? `
            <h4 style="margin-top: 15px;">💡 Suggestions for Improvement:</h4>
            <ul class="suggestions-list">
                ${analysis.suggestions.map(s => `<li>• ${s}</li>`).join('')}
            </ul>
        ` : '<p style="margin-top: 15px;">✅ Great post! No major issues found.</p>'}
    `;
    
    analysisDiv.classList.add('show');
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = show ? 'flex' : 'none';
    }
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${message}`;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Copy to clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const content = element.innerText;
    
    navigator.clipboard.writeText(content).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy', 'error');
    });
}

// Make functions global
window.copyToClipboard = copyToClipboard;
window.analyzeText = analyzeText;
// Load post history
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/get-history`);
        const data = await response.json();
        
        if (data.success) {
            displayHistory(data.history);
            updateAnalytics(data.history);
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Display history
function displayHistory(history) {
    const historyList = document.getElementById('historyList');
    
    if (!historyList) return;
    
    if (history.length === 0) {
        historyList.innerHTML = '<p class="text-muted">No posts yet. Generate your first post!</p>';
        return;
    }
    
    historyList.innerHTML = history.map(post => `
        <div class="history-item" onclick="viewPost(${post.id})">
            <div class="history-item-header">
                <span class="history-topic">${post.topic}</span>
                <span class="history-date">${post.date}</span>
            </div>
            <div class="history-preview">${post.content.substring(0, 100)}...</div>
        </div>
    `).join('');
}

// View specific post
async function viewPost(postId) {
    try {
        const response = await fetch(`${API_BASE_URL}/get-post/${postId}`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('postContent').innerHTML = data.post.content.replace(/\n/g, '<br>');
            document.getElementById('postResult').style.display = 'block';
            document.getElementById('postResult').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (error) {
        console.error('Error loading post:', error);
    }
}

// Clear history
async function clearHistory() {
    if (confirm('Are you sure you want to clear all history?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/delete-history`, {
                method: 'DELETE'
            });
            const data = await response.json();
            
            if (data.success) {
                showAlert('History cleared!', 'success');
                loadHistory();
                updateAnalytics([]);
            }
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    }
}

// Share to LinkedIn
async function shareToLinkedIn() {
    const postContent = document.getElementById('postContent').innerText;
    
    try {
        const response = await fetch(`${API_BASE_URL}/share-to-linkedin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: postContent })
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.open(data.share_url, '_blank');
            showAlert('Opening LinkedIn share dialog...', 'success');
        }
    } catch (error) {
        console.error('Error sharing:', error);
        showAlert('Failed to share', 'error');
    }
}

// Update analytics dashboard
function updateAnalytics(history) {
    if (!history || history.length === 0) {
        document.getElementById('totalPosts').textContent = '0';
        document.getElementById('mostUsedTopic').textContent = '-';
        document.getElementById('popularType').textContent = '-';
        document.getElementById('avgLength').textContent = '0';
        return;
    }
    
    // Total posts
    document.getElementById('totalPosts').textContent = history.length;
    
    // Most used topic
    const topics = {};
    const types = {};
    let totalLength = 0;
    
    history.forEach(post => {
        topics[post.topic] = (topics[post.topic] || 0) + 1;
        types[post.type] = (types[post.type] || 0) + 1;
        totalLength += post.content.length;
    });
    
    const mostUsedTopic = Object.keys(topics).reduce((a, b) => topics[a] > topics[b] ? a : b, Object.keys(topics)[0]);
    const popularType = Object.keys(types).reduce((a, b) => types[a] > types[b] ? a : b, Object.keys(types)[0]);
    const avgLength = Math.round(totalLength / history.length);
    
    document.getElementById('mostUsedTopic').textContent = mostUsedTopic;
    document.getElementById('popularType').textContent = popularType;
    document.getElementById('avgLength').textContent = avgLength;
    
    // Create charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        createCharts(types, history);
    }
}

// Create charts (requires Chart.js library)
function createCharts(types, history) {
    // Add Chart.js library if not present
    if (!document.querySelector('script[src="https://cdn.jsdelivr.net/npm/chart.js"]')) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => renderCharts(types, history);
        document.head.appendChild(script);
    } else {
        renderCharts(types, history);
    }
}

function renderCharts(types, history) {
    // Posts by type chart
    const typeCtx = document.getElementById('postsByTypeChart');
    if (typeCtx) {
        new Chart(typeCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(types),
                datasets: [{
                    data: Object.values(types),
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
                }]
            }
        });
    }
    
    // Timeline chart
    const timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx) {
        const last7Days = history.slice(0, 7).reverse();
        new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: last7Days.map(p => p.date.split(' ')[0]),
                datasets: [{
                    label: 'Posts',
                    data: last7Days.map((_, i) => i + 1),
                    borderColor: '#667eea',
                    tension: 0.4
                }]
            }
        });
    }
}

// Call loadHistory on page load
document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...
    loadHistory();
});

// Make new functions global
window.shareToLinkedIn = shareToLinkedIn;
window.clearHistory = clearHistory;
window.viewPost = viewPost;