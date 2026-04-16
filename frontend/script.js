const API_BASE_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend loaded');
    loadHistory();
    loadFavorites();
    
    document.getElementById('postForm').addEventListener('submit', generatePost);
    document.getElementById('messageForm').addEventListener('submit', generateMessage);
    document.getElementById('darkModeToggle').addEventListener('click', toggleDarkMode);
    
    // Character counter
    document.getElementById('topic').addEventListener('input', function() {
        let len = this.value.length;
        document.getElementById('charCount').innerText = len;
        let percent = Math.min((len / 100) * 100, 100);
        document.getElementById('charProgress').style.width = percent + '%';
    });
});

async function generatePost(e) {
    e.preventDefault();
    let topic = document.getElementById('topic').value;
    let type = document.getElementById('postType').value;
    
    if (!topic) {
        alert('Please enter a topic');
        return;
    }
    
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    try {
        let response = await fetch(`${API_BASE_URL}/generate-post`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({topic: topic, type: type})
        });
        
        let data = await response.json();
        
        if (data.success) {
            document.getElementById('postContent').innerHTML = data.post.content.replace(/\n/g, '<br>');
            document.getElementById('postResult').style.display = 'block';
            
            let hashtags = document.getElementById('postHashtags');
            hashtags.innerHTML = '';
            data.post.suggested_hashtags.forEach(tag => {
                let span = document.createElement('span');
                span.textContent = tag;
                hashtags.appendChild(span);
            });
            
            await loadHistory();
            alert('Post generated and saved to history!');
        }
    } catch (error) {
        console.error(error);
        alert('Error: Make sure backend is running');
    }
    
    document.getElementById('loadingOverlay').style.display = 'none';
}

async function generateMessage(e) {
    e.preventDefault();
    let recipient = document.getElementById('recipientName').value;
    let context = document.getElementById('messageContext').value;
    let purpose = document.getElementById('messagePurpose').value;
    
    if (!recipient || !context) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        let response = await fetch(`${API_BASE_URL}/generate-message`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({recipient_name: recipient, context: context, purpose: purpose})
        });
        
        let data = await response.json();
        
        if (data.success) {
            document.getElementById('messageContent').innerHTML = data.message.replace(/\n/g, '<br>');
            document.getElementById('messageResult').style.display = 'block';
        }
    } catch (error) {
        alert('Error generating message');
    }
}

async function analyzeText() {
    let text = document.getElementById('textToAnalyze').value;
    
    if (!text) {
        alert('Please paste some text');
        return;
    }
    
    try {
        let response = await fetch(`${API_BASE_URL}/analyze-text`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        });
        
        let data = await response.json();
        
        if (data.success) {
            let a = data.analysis;
            let scoreColor = a.score >= 85 ? '#28a745' : (a.score >= 70 ? '#ffc107' : (a.score >= 50 ? '#fd7e14' : '#dc3545'));
            
            let html = `
                <div style="text-align:center; padding:20px; background:${scoreColor}15; border-radius:12px; margin-bottom:20px;">
                    <div style="font-size:48px; font-weight:bold; color:${scoreColor};">${a.score}%</div>
                    <div style="font-size:20px; font-weight:bold;">${a.rating}</div>
                    <div style="color:#666;">${a.summary || ''}</div>
                </div>
                <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:20px;">
                    <div style="background:#f8f9fa; padding:12px; text-align:center; border-radius:8px;">
                        <div style="font-size:22px; font-weight:bold; color:#8E2DE2;">${a.word_count}</div>
                        <div style="font-size:12px; color:#666;">Words</div>
                    </div>
                    <div style="background:#f8f9fa; padding:12px; text-align:center; border-radius:8px;">
                        <div style="font-size:22px; font-weight:bold; color:#8E2DE2;">${a.hashtag_count}</div>
                        <div style="font-size:12px; color:#666;">Hashtags</div>
                    </div>
                    <div style="background:#f8f9fa; padding:12px; text-align:center; border-radius:8px;">
                        <div style="font-size:22px; font-weight:bold; color:#8E2DE2;">${a.has_question ? 'Yes' : 'No'}</div>
                        <div style="font-size:12px; color:#666;">Question?</div>
                    </div>
                </div>
                ${a.suggestions.length > 0 ? `
                    <div style="background:#fff3e0; padding:15px; border-radius:10px;">
                        <strong style="color:#e65100;">Suggestions to Improve:</strong>
                        <ul style="margin-top:10px;">${a.suggestions.map(s => `<li style="margin-bottom:5px;">${s}</li>`).join('')}</ul>
                    </div>
                ` : '<div style="background:#d4edda; padding:15px; border-radius:10px; color:#155724;">Great post! Keep up the good work.</div>'}
            `;
            document.getElementById('analysisResult').innerHTML = html;
            document.getElementById('analysisResult').classList.add('show');
        }
    } catch (error) {
        alert('Error analyzing text');
    }
}

async function loadHistory() {
    try {
        let response = await fetch(`${API_BASE_URL}/get-history`);
        let data = await response.json();
        
        console.log('History loaded:', data);
        
        let historyDiv = document.getElementById('historyList');
        
        if (data.history && data.history.length > 0) {
            historyDiv.innerHTML = data.history.map(post => `
                <div class="history-item" onclick="viewPost(${post.id})" style="padding:12px; border-bottom:1px solid #e0e0e0; cursor:pointer;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <strong style="color:#8E2DE2;">${post.topic}</strong>
                        <small style="color:#999;">${post.date}</small>
                    </div>
                    <div style="font-size:12px; color:#666;">${post.content.substring(0, 100)}...</div>
                </div>
            `).join('');
            
            // Update analytics numbers
            document.getElementById('totalPosts').innerText = data.history.length;
            
            // Count topic frequency
            let topics = {};
            let types = {};
            data.history.forEach(post => {
                topics[post.topic] = (topics[post.topic] || 0) + 1;
                types[post.type] = (types[post.type] || 0) + 1;
            });
            
            // Most used topic
            let mostTopic = Object.keys(topics).reduce((a,b) => topics[a] > topics[b] ? a : b, 'None');
            document.getElementById('mostUsedTopic').innerText = mostTopic;
            
            // Popular type
            let typeNames = {'professional':'Professional','networking':'Networking','tech':'Technology','marketing':'Marketing','leadership':'Leadership','career':'Career'};
            let mostType = Object.keys(types).reduce((a,b) => types[a] > types[b] ? a : b, 'professional');
            document.getElementById('popularType').innerText = typeNames[mostType] || mostType;
            
            // Average length
            let totalLen = data.history.reduce((sum, p) => sum + p.content.length, 0);
            let avgLen = Math.round(totalLen / data.history.length);
            document.getElementById('avgLength').innerText = avgLen;
            
            // Create charts with colors
            createCharts(types, data.history);
            
        } else {
            historyDiv.innerHTML = '<p class="text-muted" style="text-align:center; padding:20px;">No posts yet. Generate your first post!</p>';
            document.getElementById('totalPosts').innerText = '0';
            document.getElementById('mostUsedTopic').innerText = '-';
            document.getElementById('popularType').innerText = '-';
            document.getElementById('avgLength').innerText = '0';
            
            // Show empty charts message
            showEmptyCharts();
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function createCharts(types, history) {
    // Wait for Chart.js to be available
    if (typeof Chart === 'undefined') {
        let script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => renderCharts(types, history);
        document.head.appendChild(script);
    } else {
        renderCharts(types, history);
    }
}

function renderCharts(types, history) {
    // Color palette
    const colors = ['#8E2DE2', '#4A00E0', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#fa709a'];
    
    // Type names for display
    const typeNames = {
        'professional': 'Professional',
        'networking': 'Networking',
        'achievement': 'Achievement',
        'tech': 'Technology',
        'marketing': 'Marketing',
        'leadership': 'Leadership',
        'career': 'Career'
    };
    
    // Prepare data for pie chart
    let labels = Object.keys(types).map(t => typeNames[t] || t);
    let data = Object.values(types);
    
    // If no data, use sample data for demo
    if (labels.length === 0) {
        labels = ['Professional', 'Technology', 'Marketing', 'Leadership'];
        data = [4, 3, 2, 2];
    }
    
    // Pie Chart - Posts by Type
    let pieCtx = document.getElementById('postsByTypeChart');
    if (pieCtx) {
        if (window.pieChart) window.pieChart.destroy();
        window.pieChart = new Chart(pieCtx, {
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
                    legend: {
                        position: 'bottom',
                        labels: { font: { size: 11, weight: 'bold' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                let value = context.raw || 0;
                                let total = context.dataset.data.reduce((a,b) => a + b, 0);
                                let percent = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} posts (${percent}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Line Chart - Timeline
    let timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx && history.length > 0) {
        if (window.lineChart) window.lineChart.destroy();
        
        // Group by date
        let postsByDate = {};
        history.forEach(post => {
            let date = post.date.split(' ')[0];
            postsByDate[date] = (postsByDate[date] || 0) + 1;
        });
        
        let dates = Object.keys(postsByDate).slice(-7);
        let counts = dates.map(d => postsByDate[d]);
        
        window.lineChart = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Posts Created',
                    data: counts,
                    borderColor: '#8E2DE2',
                    backgroundColor: 'rgba(142, 45, 226, 0.1)',
                    borderWidth: 3,
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
                    y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } }
                }
            }
        });
    } else if (timelineCtx) {
        showEmptyCharts();
    }
}

function showEmptyCharts() {
    let pieCtx = document.getElementById('postsByTypeChart');
    let timelineCtx = document.getElementById('timelineChart');
    
    if (pieCtx && !window.pieChart) {
        let ctx = pieCtx.getContext('2d');
        ctx.clearRect(0, 0, pieCtx.width, pieCtx.height);
        ctx.font = '14px Arial';
        ctx.fillStyle = '#999';
        ctx.fillText('Generate posts to see chart', pieCtx.width/2 - 100, pieCtx.height/2);
    }
    
    if (timelineCtx && !window.lineChart) {
        let ctx = timelineCtx.getContext('2d');
        ctx.clearRect(0, 0, timelineCtx.width, timelineCtx.height);
        ctx.font = '14px Arial';
        ctx.fillStyle = '#999';
        ctx.fillText('Generate posts to see timeline', timelineCtx.width/2 - 100, timelineCtx.height/2);
    }
}

async function viewPost(id) {
    try {
        let response = await fetch(`${API_BASE_URL}/get-post/${id}`);
        let data = await response.json();
        if (data.success) {
            document.getElementById('postContent').innerHTML = data.post.content.replace(/\n/g, '<br>');
            document.getElementById('postResult').style.display = 'block';
            document.getElementById('postResult').scrollIntoView({behavior: 'smooth'});
        }
    } catch (error) {
        alert('Error loading post');
    }
}

async function clearHistory() {
    if (confirm('Clear all history?')) {
        await fetch(`${API_BASE_URL}/delete-history`, {method: 'DELETE'});
        await loadHistory();
        alert('History cleared');
    }
}

function saveFavorite() {
    let topic = document.getElementById('topic').value;
    let type = document.getElementById('postType').value;
    
    if (!topic) {
        alert('Enter a topic first');
        return;
    }
    
    let favs = JSON.parse(localStorage.getItem('favorites') || '[]');
    favs.push({topic: topic, type: type, date: new Date().toLocaleDateString()});
    localStorage.setItem('favorites', JSON.stringify(favs));
    loadFavorites();
    alert('Saved to favorites');
}

function loadFavorites() {
    let favs = JSON.parse(localStorage.getItem('favorites') || '[]');
    let container = document.getElementById('favoritesList');
    
    if (!container) return;
    
    if (favs.length === 0) {
        container.innerHTML = '<p class="text-muted" style="text-align:center; padding:20px;">No favorites yet. Save your first template!</p>';
        return;
    }
    
    container.innerHTML = favs.map((fav, i) => `
        <div class="favorite-item" onclick="loadFavorite(${i})" style="padding:12px; border-bottom:1px solid #e0e0e0; cursor:pointer; display:flex; justify-content:space-between;">
            <div><strong style="color:#8E2DE2;">${fav.topic}</strong> <small>${fav.type}</small></div>
            <small style="color:#999;">${fav.date}</small>
        </div>
    `).join('');
}

function loadFavorite(index) {
    let favs = JSON.parse(localStorage.getItem('favorites') || '[]');
    let fav = favs[index];
    if (fav) {
        document.getElementById('topic').value = fav.topic;
        document.getElementById('postType').value = fav.type;
        alert('Favorite loaded! Click Generate Post');
        // Trigger character counter
        let event = new Event('input');
        document.getElementById('topic').dispatchEvent(event);
    }
}

function shareToLinkedIn() {
    let content = document.getElementById('postContent').innerText;
    if (content) {
        window.open(`https://www.linkedin.com/sharing/share-offsite/?text=${encodeURIComponent(content)}`, '_blank');
    } else {
        alert('Generate a post first');
    }
}

async function exportAsPDF() {
    let content = document.getElementById('postContent').innerText;
    if (!content) {
        alert('Generate a post first');
        return;
    }
    
    let response = await fetch(`${API_BASE_URL}/export-pdf`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({content: content})
    });
    
    if (response.ok) {
        let blob = await response.blob();
        let url = URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = 'linkedin_post.pdf';
        a.click();
        alert('PDF downloaded');
    }
}

function exportAsImage() {
    alert('Image export feature coming soon');
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    let btn = document.getElementById('darkModeToggle');
    if (document.body.classList.contains('dark-mode')) {
        btn.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('darkMode', 'true');
    } else {
        btn.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('darkMode', 'false');
    }
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.getElementById('darkModeToggle').innerHTML = '<i class="fas fa-sun"></i>';
}

// Make functions global
window.analyzeText = analyzeText;
window.clearHistory = clearHistory;
window.viewPost = viewPost;
window.saveFavorite = saveFavorite;
window.loadFavorite = loadFavorite;
window.shareToLinkedIn = shareToLinkedIn;
window.exportAsPDF = exportAsPDF;
window.exportAsImage = exportAsImage;