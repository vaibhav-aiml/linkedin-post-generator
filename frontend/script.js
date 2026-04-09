// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend loaded successfully');
    checkBackendHealth();
    displayFavorites();
    loadHistory();
    
    const postForm = document.getElementById('postForm');
    const messageForm = document.getElementById('messageForm');
    
    if (postForm) postForm.addEventListener('submit', handlePostGeneration);
    if (messageForm) messageForm.addEventListener('submit', handleMessageGeneration);
    
    setupDarkMode();
    setupCharacterCounter();
});

// Dark Mode Setup
function setupDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) return;
    
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

// Character Counter
function setupCharacterCounter() {
    const topicInput = document.getElementById('topic');
    const charCount = document.getElementById('charCount');
    const charProgress = document.getElementById('charProgress');
    
    if (topicInput) {
        topicInput.addEventListener('input', function() {
            const length = this.value.length;
            charCount.textContent = length;
            const percentage = Math.min((length / 100) * 100, 100);
            charProgress.style.width = percentage + '%';
            charProgress.classList.remove('warning', 'danger');
            if (length > 80) charProgress.classList.add('warning');
            if (length > 95) charProgress.classList.add('danger');
        });
    }
}

// Check backend health
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('Backend is healthy:', data);
    } catch (error) {
        console.error('Backend not reachable:', error);
        showAlert('⚠️ Backend server is not running', 'error');
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
        const response = await fetch(`${API_BASE_URL}/generate-post`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: topic, type: postType })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('postContent').innerHTML = data.post.content.replace(/\n/g, '<br>');
            
            const hashtagsContainer = document.getElementById('postHashtags');
            if (hashtagsContainer && data.post.suggested_hashtags) {
                hashtagsContainer.innerHTML = '';
                data.post.suggested_hashtags.forEach(tag => {
                    const span = document.createElement('span');
                    span.textContent = tag;
                    hashtagsContainer.appendChild(span);
                });
            }
            
            document.getElementById('postResult').style.display = 'block';
            document.getElementById('postResult').scrollIntoView({ behavior: 'smooth' });
            showAlert('Post generated successfully!', 'success');
            loadHistory();
        } else {
            showAlert(data.error || 'Failed to generate post', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Failed to connect to backend. Make sure it\'s running on port 5000', 'error');
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
        const response = await fetch(`${API_BASE_URL}/generate-message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipient_name: recipientName, context: context, purpose: purpose })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('messageContent').innerHTML = data.message.replace(/\n/g, '<br>');
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

// Analyze text
async function analyzeText() {
    const text = document.getElementById('textToAnalyze').value;
    if (!text.trim()) {
        showAlert('Please paste some text to analyze', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze-text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
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

function displayAnalysis(analysis) {
    const analysisDiv = document.getElementById('analysisResult');
    analysisDiv.innerHTML = `
        <div class="analysis-stats">
            <div class="stat-box"><div class="stat-value">${analysis.word_count}</div><div class="stat-label">Words</div></div>
            <div class="stat-box"><div class="stat-value">${analysis.has_question ? 'Yes' : 'No'}</div><div class="stat-label">Question?</div></div>
            <div class="stat-box"><div class="stat-value">${analysis.has_hashtags ? 'Yes' : 'No'}</div><div class="stat-label">Hashtags?</div></div>
        </div>
        ${analysis.suggestions && analysis.suggestions.length > 0 ? 
            `<h4>💡 Suggestions:</h4><ul>${analysis.suggestions.map(s => `<li>${s}</li>`).join('')}</ul>` : 
            '<p>✅ Great post!</p>'}
    `;
    analysisDiv.classList.add('show');
}

// FAVORITE TEMPLATES
function saveCurrentTemplate() {
    const topic = document.getElementById('topic').value;
    const postType = document.getElementById('postType').value;
    
    if (!topic) {
        showAlert('Please enter a topic first', 'error');
        return;
    }
    
    let favorites = JSON.parse(localStorage.getItem('postTemplates') || '[]');
    favorites.push({
        id: Date.now(),
        topic: topic,
        type: postType,
        date: new Date().toLocaleDateString()
    });
    
    if (favorites.length > 10) favorites = favorites.slice(-10);
    localStorage.setItem('postTemplates', JSON.stringify(favorites));
    showAlert('Template saved to favorites!', 'success');
    displayFavorites();
}

function displayFavorites() {
    const favorites = JSON.parse(localStorage.getItem('postTemplates') || '[]');
    const container = document.getElementById('favoritesList');
    
    if (!container) return;
    
    if (favorites.length === 0) {
        container.innerHTML = '<p class="text-muted">No saved templates yet. Save your first template!</p>';
        return;
    }
    
    container.innerHTML = favorites.map(fav => `
        <div class="favorite-item" onclick="loadFavorite(${fav.id})">
            <div><strong>${escapeHtml(fav.topic)}</strong><small>${fav.type}</small></div>
            <span class="favorite-date">${fav.date}</span>
        </div>
    `).join('');
}

function loadFavorite(id) {
    const favorites = JSON.parse(localStorage.getItem('postTemplates') || '[]');
    const favorite = favorites.find(f => f.id === id);
    
    if (favorite) {
        document.getElementById('topic').value = favorite.topic;
        document.getElementById('postType').value = favorite.type;
        showAlert('Template loaded! Click Generate Post', 'success');
        const event = new Event('input');
        document.getElementById('topic').dispatchEvent(event);
    }
}

// POST HISTORY
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
        // Show demo analytics if backend not available
        updateAnalytics(null);
    }
}

function displayHistory(history) {
    const historyList = document.getElementById('historyList');
    if (!historyList) return;
    
    if (!history || history.length === 0) {
        historyList.innerHTML = '<p class="text-muted">No posts yet. Generate your first post!</p>';
        return;
    }
    
    historyList.innerHTML = history.map(post => `
        <div class="history-item" onclick="viewPost(${post.id})">
            <div class="history-item-header">
                <span class="history-topic">${escapeHtml(post.topic)}</span>
                <span class="history-date">${post.date}</span>
            </div>
            <div class="history-preview">${escapeHtml(post.content.substring(0, 100))}...</div>
        </div>
    `).join('');
}

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
        showAlert('Failed to load post', 'error');
    }
}

async function clearHistory() {
    if (confirm('Are you sure you want to clear all history?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/delete-history`, { method: 'DELETE' });
            const data = await response.json();
            if (data.success) {
                showAlert('History cleared!', 'success');
                loadHistory();
            }
        } catch (error) {
            showAlert('Failed to clear history', 'error');
        }
    }
}

// ANALYTICS DASHBOARD WITH WORKING GRAPHS
function updateAnalytics(history) {
    console.log("Updating analytics with history:", history);
    
    const totalPostsElem = document.getElementById('totalPosts');
    const mostUsedTopicElem = document.getElementById('mostUsedTopic');
    const popularTypeElem = document.getElementById('popularType');
    const avgLengthElem = document.getElementById('avgLength');
    
    // Use demo data if no history
    let displayHistory = history;
    let useDemo = false;
    
    if (!history || history.length === 0) {
        console.log("No history, using demo data for graphs");
        useDemo = true;
        displayHistory = [
            { id: 1, topic: "Artificial Intelligence", type: "tech", content: "AI content...", date: "2024-04-07" },
            { id: 2, topic: "Digital Marketing", type: "marketing", content: "Marketing content...", date: "2024-04-06" },
            { id: 3, topic: "Leadership Skills", type: "leadership", content: "Leadership content...", date: "2024-04-05" },
            { id: 4, topic: "Remote Work", type: "professional", content: "Remote work content...", date: "2024-04-04" },
            { id: 5, topic: "Career Growth", type: "career", content: "Career content...", date: "2024-04-03" }
        ];
    }
    
    if (totalPostsElem) totalPostsElem.textContent = displayHistory.length;
    
    // Count topics and types
    const topics = {};
    const types = {};
    let totalLength = 0;
    
    displayHistory.forEach(post => {
        const topic = post.topic || 'Unknown';
        const type = post.type || 'professional';
        topics[topic] = (topics[topic] || 0) + 1;
        types[type] = (types[type] || 0) + 1;
        totalLength += (post.content || '').length;
    });
    
    console.log("Types found:", types);
    
    // Most used topic
    let mostUsedTopic = '-';
    let maxCount = 0;
    for (const [topic, count] of Object.entries(topics)) {
        if (count > maxCount) {
            maxCount = count;
            mostUsedTopic = topic;
        }
    }
    
    // Popular type
    const typeNames = {
        'professional': 'Professional', 'networking': 'Networking', 'achievement': 'Achievement',
        'tech': 'Technology', 'marketing': 'Marketing', 'leadership': 'Leadership', 'career': 'Career'
    };
    
    let popularType = '-';
    maxCount = 0;
    for (const [type, count] of Object.entries(types)) {
        if (count > maxCount) {
            maxCount = count;
            popularType = typeNames[type] || type;
        }
    }
    
    const avgLength = displayHistory.length > 0 ? Math.round(totalLength / displayHistory.length) : 0;
    
    if (mostUsedTopicElem) mostUsedTopicElem.textContent = mostUsedTopic;
    if (popularTypeElem) popularTypeElem.textContent = popularType;
    if (avgLengthElem) avgLengthElem.textContent = avgLength;
    
    // Create charts
    createCharts(types, displayHistory);
}

function createCharts(types, history) {
    console.log("Creating charts...");
    
    // Wait for Chart.js to load
    if (typeof Chart === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => {
            console.log("Chart.js loaded, rendering charts");
            renderAllCharts(types, history);
        };
        document.head.appendChild(script);
    } else {
        console.log("Chart.js already loaded, rendering charts");
        renderAllCharts(types, history);
    }
}

function renderAllCharts(types, history) {
    console.log("Rendering all charts with types:", types);
    
    const typeNames = {
        'professional': 'Professional', 'networking': 'Networking', 'achievement': 'Achievement',
        'tech': 'Technology', 'marketing': 'Marketing', 'leadership': 'Leadership', 'career': 'Career'
    };
    const colors = ['#8E2DE2', '#4A00E0', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b'];
    
    // Use demo data if no types
    let chartTypes = types;
    if (!types || Object.keys(types).length === 0) {
        console.log("No types data, using sample data for pie chart");
        chartTypes = {
            'tech': 3,
            'marketing': 2,
            'leadership': 2,
            'professional': 1,
            'career': 1
        };
    }
    
    // PIE CHART - Posts by Type
    const typeCtx = document.getElementById('postsByTypeChart');
    if (typeCtx) {
        if (window.postsByTypeChart) {
            window.postsByTypeChart.destroy();
        }
        
        const labels = Object.keys(chartTypes).map(t => typeNames[t] || t);
        const data = Object.values(chartTypes);
        
        window.postsByTypeChart = new Chart(typeCtx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'bottom', labels: { font: { size: 11 } } },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} posts (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
        console.log("Pie chart created successfully");
    }
    
    // LINE CHART - Timeline
    const timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx) {
        if (window.timelineChart) {
            window.timelineChart.destroy();
        }
        
        // Use history or create sample timeline
        let timelineData = history;
        if (!history || history.length === 0) {
            timelineData = [
                { date: "Apr 3", type: "tech" },
                { date: "Apr 4", type: "marketing" },
                { date: "Apr 5", type: "leadership" },
                { date: "Apr 6", type: "tech" },
                { date: "Apr 7", type: "professional" }
            ];
        }
        
        // Group by date
        const postsByDate = {};
        timelineData.forEach(post => {
            let date = post.date;
            if (date && date.includes('-')) {
                const parts = date.split('-');
                date = `${parts[1]}/${parts[2]}`;
            }
            postsByDate[date] = (postsByDate[date] || 0) + 1;
        });
        
        const dates = Object.keys(postsByDate).slice(-7);
        const counts = dates.map(d => postsByDate[d]);
        
        window.timelineChart = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Posts Created',
                    data: counts,
                    borderColor: '#8E2DE2',
                    backgroundColor: 'rgba(142, 45, 226, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#8E2DE2',
                    pointBorderColor: '#fff',
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: { callbacks: { label: (ctx) => `${ctx.raw} posts` } }
                },
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                }
            }
        });
        console.log("Timeline chart created successfully");
    }
}

// Utility functions
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.style.display = show ? 'flex' : 'none';
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${message}`;
    document.body.appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 3000);
}

function copyToClipboard(elementId) {
    const content = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(content).then(() => showAlert('Copied to clipboard!', 'success'));
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Share to LinkedIn
function shareToLinkedIn() {
    const content = document.getElementById('postContent').innerText;
    if (content && content.trim()) {
        window.open(`https://www.linkedin.com/sharing/share-offsite/?text=${encodeURIComponent(content)}`, '_blank');
        showAlert('Opening LinkedIn...', 'success');
    } else {
        showAlert('Generate a post first!', 'error');
    }
}

function exportAsPDF() {
    showAlert('PDF export coming soon!', 'info');
}

function exportAsImage() {
    showAlert('Image export coming soon!', 'info');
}

// Export functions
window.copyToClipboard = copyToClipboard;
window.analyzeText = analyzeText;
window.saveCurrentTemplate = saveCurrentTemplate;
window.loadFavorite = loadFavorite;
window.clearHistory = clearHistory;
window.viewPost = viewPost;
window.exportAsPDF = exportAsPDF;
window.exportAsImage = exportAsImage;
window.shareToLinkedIn = shareToLinkedIn;