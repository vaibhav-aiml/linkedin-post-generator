const API_BASE_URL = window.location.port === '5000' ? 'http://localhost:5000/api' : 'http://localhost:8000/api';

document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend loaded');
    loadHistory();
    loadFavorites();
    
    document.getElementById('postForm').addEventListener('submit', generatePost);
    document.getElementById('messageForm').addEventListener('submit', generateMessage);
    document.getElementById('darkModeToggle').addEventListener('click', toggleDarkMode);
    
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
    
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    try {
        let response = await fetch(`${API_BASE_URL}/analyze-text`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        });
        
        let data = await response.json();
        
        if (data.success) {
            displayAnalysis(data.analysis);
        } else {
            alert('Analysis failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing text. Make sure backend is running.');
    }
    
    document.getElementById('loadingOverlay').style.display = 'none';
}

function displayAnalysis(a) {
    const analysisDiv = document.getElementById('analysisResult');
    
    if (!analysisDiv) return;
    
    console.log('Analysis data received:', a);
    
    let scoreColor = '#dc3545';
    let scoreBg = '#f8d7da';
    if (a.score >= 85) {
        scoreColor = '#155724';
        scoreBg = '#d4edda';
    } else if (a.score >= 70) {
        scoreColor = '#856404';
        scoreBg = '#fff3cd';
    } else if (a.score >= 50) {
        scoreColor = '#e65100';
        scoreBg = '#fff3e0';
    }
    
    const getStatusClass = (status) => {
        if (!status || status === 'No Data') return 'status-missing';
        if (status === 'Perfect' || status === 'Excellent') return 'status-good';
        if (status === 'Good') return 'status-good';
        if (status === 'Too Short' || status === 'Too Long' || status === 'Missing' || status === 'Low') return 'status-missing';
        if (status === 'Too Many') return 'status-warning';
        return 'status-warning';
    };
    
    const getStatusIcon = (status) => {
        if (!status || status === 'No Data') return '❓';
        if (status === 'Perfect' || status === 'Excellent') return '✅';
        if (status === 'Good') return '👍';
        if (status === 'Too Many') return '⚠️';
        if (status === 'Too Short' || status === 'Too Long' || status === 'Missing' || status === 'Low') return '❌';
        return '⚠️';
    };
    
    analysisDiv.innerHTML = `
        <style>
            .analysis-score-section {
                text-align: center;
                padding: 20px;
                background: ${scoreBg};
                border-radius: 12px;
                margin-bottom: 20px;
            }
            .analysis-score-number {
                font-size: 52px;
                font-weight: bold;
                color: ${scoreColor};
            }
            .analysis-rating {
                font-size: 24px;
                font-weight: bold;
                color: #1a1a2e;
                margin-top: 8px;
            }
            .analysis-summary {
                color: #495057;
                margin-top: 8px;
                font-size: 14px;
            }
            .analysis-stats-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
                margin-bottom: 20px;
            }
            .analysis-stat-card {
                background: #f8f9fa;
                padding: 12px;
                border-radius: 8px;
                text-align: center;
            }
            .analysis-stat-value {
                font-size: 22px;
                font-weight: bold;
                color: #8E2DE2;
            }
            .analysis-stat-label {
                font-size: 11px;
                color: #6c757d;
                margin-top: 5px;
            }
            .analysis-status-section {
                background: white;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 20px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .analysis-status-title {
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 12px;
                color: #1a1a2e;
                border-left: 3px solid #8E2DE2;
                padding-left: 10px;
            }
            .status-good {
                background: #d4edda;
                color: #155724;
                padding: 10px 12px;
                border-radius: 8px;
                margin-bottom: 8px;
                font-size: 13px;
            }
            .status-warning {
                background: #fff3cd;
                color: #856404;
                padding: 10px 12px;
                border-radius: 8px;
                margin-bottom: 8px;
                font-size: 13px;
            }
            .status-missing {
                background: #f8d7da;
                color: #721c24;
                padding: 10px 12px;
                border-radius: 8px;
                margin-bottom: 8px;
                font-size: 13px;
            }
            .analysis-suggestions-box {
                background: #e8f5e9;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 4px solid #4caf50;
            }
            .analysis-improvement-box {
                background: #fff3e0;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 4px solid #ff9800;
            }
            .analysis-corrected-box {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 4px solid #2196f3;
            }
            .analysis-section-title {
                font-weight: 700;
                margin-bottom: 10px;
                color: #1a1a2e;
                font-size: 14px;
            }
            .corrected-text {
                background: #f0f7ff;
                padding: 12px;
                border-radius: 8px;
                font-family: monospace;
                font-size: 13px;
                line-height: 1.5;
                white-space: pre-wrap;
                margin-top: 10px;
                max-height: 200px;
                overflow-y: auto;
            }
            .copy-corrected-btn {
                background: #2196f3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
                font-size: 12px;
                display: inline-flex;
                align-items: center;
                gap: 5px;
            }
            .copy-corrected-btn:hover {
                background: #1976d2;
            }
            body.dark-mode .analysis-status-section {
                background: #1e1e2e;
            }
            body.dark-mode .analysis-stat-card {
                background: #2d2d3d;
            }
            body.dark-mode .analysis-stat-value {
                color: #a78bfa;
            }
            body.dark-mode .analysis-stat-label {
                color: #a0a0a0;
            }
            body.dark-mode .analysis-status-title {
                color: #e0e0e0;
            }
            body.dark-mode .analysis-summary {
                color: #c0c0c0;
            }
            body.dark-mode .analysis-rating {
                color: #e0e0e0;
            }
            body.dark-mode .corrected-text {
                background: #2d2d3d;
                color: #e0e0e0;
            }
        </style>
        
        <div class="analysis-score-section">
            <div class="analysis-score-number">${a.score || 0}%</div>
            <div class="analysis-rating">${a.rating || 'No Rating'}</div>
            <div class="analysis-summary">${a.summary || ''}</div>
        </div>
        
        <div class="analysis-stats-grid">
            <div class="analysis-stat-card">
                <div class="analysis-stat-value">${a.word_count || 0}</div>
                <div class="analysis-stat-label">Words</div>
            </div>
            <div class="analysis-stat-card">
                <div class="analysis-stat-value">${a.hashtag_count || 0}</div>
                <div class="analysis-stat-label">Hashtags</div>
            </div>
            <div class="analysis-stat-card">
                <div class="analysis-stat-value">${a.question_count || 0}</div>
                <div class="analysis-stat-label">Questions</div>
            </div>
            <div class="analysis-stat-card">
                <div class="analysis-stat-value">${a.has_emoji ? 'Yes' : 'No'}</div>
                <div class="analysis-stat-label">Emojis</div>
            </div>
        </div>
        
        <div class="analysis-status-section">
            <div class="analysis-status-title">Detailed Breakdown</div>
            
            <div class="${getStatusClass(a.length_status)}">
                ${getStatusIcon(a.length_status)} <strong>Length:</strong> ${a.length_status || 'Unknown'} - ${a.length_message || 'Check your word count'}
            </div>
            
            <div class="${getStatusClass(a.question_status)}">
                ${getStatusIcon(a.question_status)} <strong>Questions:</strong> ${a.question_status || 'Unknown'} - ${a.question_message || 'Add a question to engage readers'}
            </div>
            
            <div class="${getStatusClass(a.hashtag_status)}">
                ${getStatusIcon(a.hashtag_status)} <strong>Hashtags:</strong> ${a.hashtag_status || 'Unknown'} - ${a.hashtag_message || 'Add 3-5 relevant hashtags'}
            </div>
            
            <div class="${getStatusClass(a.emoji_status)}">
                ${getStatusIcon(a.emoji_status)} <strong>Emojis:</strong> ${a.emoji_status || 'Unknown'} - ${a.emoji_message || 'Add emojis for visual appeal'}
            </div>
        </div>
    `;
    
    if (a.suggestions && a.suggestions.length > 0) {
        analysisDiv.innerHTML += `
            <div class="analysis-suggestions-box">
                <div class="analysis-section-title">What to Improve</div>
                <ul style="margin: 0; padding-left: 20px;">
                    ${a.suggestions.map(s => `<li style="margin-bottom: 8px;">${s}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (a.improvement_tips && a.improvement_tips.length > 0) {
        analysisDiv.innerHTML += `
            <div class="analysis-improvement-box">
                <div class="analysis-section-title">How to Improve</div>
                <ul style="margin: 0; padding-left: 20px;">
                    ${a.improvement_tips.map(t => `<li style="margin-bottom: 8px;">${t}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (a.corrected_version && a.corrected_version !== a.original_text && a.corrected_version !== 'No post to correct. Please paste your LinkedIn post above.') {
        analysisDiv.innerHTML += `
            <div class="analysis-corrected-box">
                <div class="analysis-section-title">Improved Version (Copy-Paste Ready)</div>
                <div class="corrected-text" id="correctedText">${escapeHtml(a.corrected_version)}</div>
                <button class="copy-corrected-btn" onclick="copyCorrectedVersion()">
                    Copy Improved Version
                </button>
            </div>
        `;
    }
    
    analysisDiv.classList.add('show');
}

function copyCorrectedVersion() {
    const correctedText = document.getElementById('correctedText');
    if (correctedText) {
        navigator.clipboard.writeText(correctedText.innerText).then(() => {
            alert('Improved version copied to clipboard!');
        }).catch(() => {
            alert('Failed to copy. Please select and copy manually.');
        });
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function loadHistory() {
    try {
        let response = await fetch(`${API_BASE_URL}/get-history`);
        let data = await response.json();
        
        let historyDiv = document.getElementById('historyList');
        
        if (data.history && data.history.length > 0) {
            historyDiv.innerHTML = data.history.map(post => `
                <div class="history-item" onclick="viewPost(${post.id})" style="padding:12px; border-bottom:1px solid #e0e0e0; cursor:pointer;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <strong style="color:#8E2DE2;">${escapeHtml(post.topic)}</strong>
                        <small style="color:#999;">${post.date}</small>
                    </div>
                    <div style="font-size:12px; color:#666;">${escapeHtml(post.content.substring(0, 100))}...</div>
                </div>
            `).join('');
            
            document.getElementById('totalPosts').innerText = data.history.length;
            
            let topics = {};
            let types = {};
            data.history.forEach(post => {
                topics[post.topic] = (topics[post.topic] || 0) + 1;
                types[post.type] = (types[post.type] || 0) + 1;
            });
            
            let mostTopic = Object.keys(topics).reduce((a,b) => topics[a] > topics[b] ? a : b, 'None');
            document.getElementById('mostUsedTopic').innerText = mostTopic;
            
            let typeNames = {'professional':'Professional','networking':'Networking','tech':'Technology','marketing':'Marketing','leadership':'Leadership','career':'Career'};
            let mostType = Object.keys(types).reduce((a,b) => types[a] > types[b] ? a : b, 'professional');
            document.getElementById('popularType').innerText = typeNames[mostType] || mostType;
            
            let totalLen = data.history.reduce((sum, p) => sum + p.content.length, 0);
            let avgLen = Math.round(totalLen / data.history.length);
            document.getElementById('avgLength').innerText = avgLen;
            
            createCharts(types, data.history);
        } else {
            historyDiv.innerHTML = '<p class="text-muted" style="text-align:center; padding:20px;">No posts yet. Generate your first post!</p>';
            document.getElementById('totalPosts').innerText = '0';
            document.getElementById('mostUsedTopic').innerText = '-';
            document.getElementById('popularType').innerText = '-';
            document.getElementById('avgLength').innerText = '0';
            showEmptyCharts();
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function createCharts(types, history) {
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
    const colors = ['#8E2DE2', '#4A00E0', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b'];
    const typeNames = {'professional':'Professional','networking':'Networking','tech':'Technology','marketing':'Marketing','leadership':'Leadership','career':'Career'};
    
    let labels = Object.keys(types).map(t => typeNames[t] || t);
    let data = Object.values(types);
    
    if (labels.length === 0) {
        labels = ['Professional', 'Technology', 'Marketing', 'Leadership'];
        data = [4, 3, 2, 2];
    }
    
    let pieCtx = document.getElementById('postsByTypeChart');
    if (pieCtx) {
        if (window.pieChart) window.pieChart.destroy();
        window.pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: { labels: labels, datasets: [{ data: data, backgroundColor: colors.slice(0, labels.length), borderWidth: 2, borderColor: '#fff' }] },
            options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom' } } }
        });
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
            <div><strong style="color:#8E2DE2;">${escapeHtml(fav.topic)}</strong> <small>${fav.type}</small></div>
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

if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.getElementById('darkModeToggle').innerHTML = '<i class="fas fa-sun"></i>';
}

window.analyzeText = analyzeText;
window.clearHistory = clearHistory;
window.viewPost = viewPost;
window.saveFavorite = saveFavorite;
window.loadFavorite = loadFavorite;
window.shareToLinkedIn = shareToLinkedIn;
window.exportAsPDF = exportAsPDF;
window.exportAsImage = exportAsImage;
window.copyCorrectedVersion = copyCorrectedVersion;