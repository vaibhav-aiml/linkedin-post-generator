const API_BASE_URL = window.location.origin.includes('5000')
    ? 'http://localhost:5000/api'
    : (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? 'http://localhost:8000/api/v1'
        : `${window.location.origin}/api/v1`;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend loaded, connecting to API:', API_BASE_URL);
    checkAuthStatus();
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

async function checkAuthStatus() {
    try {
        let response = await fetch(`${API_BASE_URL}/auth/me`, {
            method: 'GET',
            credentials: 'include'
        });
        if (response.ok) {
            let user = await response.json();
            document.getElementById('userBadge').style.display = 'inline-block';
            document.getElementById('userEmailText').innerText = user.email;
            document.getElementById('authBtn').style.display = 'none';
            document.getElementById('logoutBtn').style.display = 'inline-block';
        } else {
            document.getElementById('userBadge').style.display = 'none';
            document.getElementById('authBtn').style.display = 'inline-block';
            document.getElementById('logoutBtn').style.display = 'none';
        }
    } catch (e) {
        console.log('Auth check error (running in guest mode):', e);
    }
}

function openAuthModal() {
    document.getElementById('authModal').style.display = 'flex';
}

function closeAuthModal() {
    document.getElementById('authModal').style.display = 'none';
}

function switchAuthTab(tab) {
    if (tab === 'login') {
        document.getElementById('tabLoginBtn').classList.add('active');
        document.getElementById('tabRegisterBtn').classList.remove('active');
        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('registerForm').style.display = 'none';
    } else {
        document.getElementById('tabRegisterBtn').classList.add('active');
        document.getElementById('tabLoginBtn').classList.remove('active');
        document.getElementById('registerForm').style.display = 'block';
        document.getElementById('loginForm').style.display = 'none';
    }
}

async function handleLogin(e) {
    e.preventDefault();
    let email = document.getElementById('loginEmail').value;
    let password = document.getElementById('loginPassword').value;

    try {
        let response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({email, password})
        });
        let data = await response.json();
        if (response.ok) {
            alert('Login successful!');
            closeAuthModal();
            await checkAuthStatus();
            await loadHistory();
        } else {
            alert(data.detail || 'Login failed');
        }
    } catch (err) {
        alert('Login error: ' + err.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    let email = document.getElementById('registerEmail').value;
    let password = document.getElementById('registerPassword').value;

    try {
        let response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({email, password})
        });
        let data = await response.json();
        if (response.ok) {
            alert('Registration successful! Please login.');
            switchAuthTab('login');
            document.getElementById('loginEmail').value = email;
        } else {
            alert(data.detail || 'Registration failed');
        }
    } catch (err) {
        alert('Registration error: ' + err.message);
    }
}

async function logoutUser() {
    try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        alert('Logged out');
        await checkAuthStatus();
        await loadHistory();
    } catch (e) {
        console.error(e);
    }
}

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
            credentials: 'include',
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
            credentials: 'include',
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
            credentials: 'include',
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

    analysisDiv.innerHTML = `
        <div class="quality-stamp-hero">
            <div class="quality-seal-badge">
                <div class="seal-score-number">${a.score || 0}%</div>
                <div class="seal-score-label">QUALITY SCORE</div>
            </div>
            <div class="seal-details">
                <div class="seal-rating-title">${escapeHtml(a.rating || 'Audit Completed')}</div>
                <div class="seal-summary-text">${escapeHtml(a.summary || '')}</div>
            </div>
        </div>

        <div class="breakdown-grid">
            <div class="breakdown-card">
                <div class="breakdown-val">${a.word_count || 0}</div>
                <div class="breakdown-lbl">Words Count</div>
            </div>
            <div class="breakdown-card">
                <div class="breakdown-val">${a.hashtag_count || 0}</div>
                <div class="breakdown-lbl">Hashtags</div>
            </div>
            <div class="breakdown-card">
                <div class="breakdown-val">${a.question_count || 0}</div>
                <div class="breakdown-lbl">Questions</div>
            </div>
            <div class="breakdown-card">
                <div class="breakdown-val">${a.has_emoji ? 'Yes' : 'No'}</div>
                <div class="breakdown-lbl">Emoji Elements</div>
            </div>
        </div>

        ${a.suggestions && a.suggestions.length > 0 ? `
            <div class="audit-box">
                <div class="audit-box-title"><i class="fas fa-lightbulb"></i> Actionable Suggestions</div>
                <ul>${a.suggestions.map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>
            </div>
        ` : ''}

        ${a.improvement_tips && a.improvement_tips.length > 0 ? `
            <div class="audit-box improvement">
                <div class="audit-box-title"><i class="fas fa-chart-line"></i> Engagement Tips</div>
                <ul>${a.improvement_tips.map(t => `<li>${escapeHtml(t)}</li>`).join('')}</ul>
            </div>
        ` : ''}

        ${a.corrected_version && a.corrected_version !== a.original_text ? `
            <div class="audit-box corrected">
                <div class="audit-box-title"><i class="fas fa-magic"></i> AI Improved Version</div>
                <div class="corrected-text-block" id="correctedText">${escapeHtml(a.corrected_version)}</div>
                <button class="paper-btn copy" style="margin-top:12px;" onclick="copyCorrectedVersion()">
                    <i class="fas fa-copy"></i> Copy Improved Version
                </button>
            </div>
        ` : ''}
    `;

    analysisDiv.style.display = 'block';
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
        let response = await fetch(`${API_BASE_URL}/get-history`, {
            credentials: 'include'
        });
        let data = await response.json();
        
        let historyDiv = document.getElementById('historyList');
        
        if (historyDiv && data.history && data.history.length > 0) {
            historyDiv.innerHTML = data.history.map(post => `
                <div class="history-item" onclick="viewPost(${post.id})">
                    <div class="history-item-header">
                        <strong class="item-topic">${escapeHtml(post.topic)}</strong>
                        <small class="item-date">${post.date}</small>
                    </div>
                    <div class="item-preview">${escapeHtml(post.content.substring(0, 100))}...</div>
                </div>
            `).join('');
            
            if (document.getElementById('totalPosts')) document.getElementById('totalPosts').innerText = data.history.length;
            
            let topics = {};
            let types = {};
            data.history.forEach(post => {
                topics[post.topic] = (topics[post.topic] || 0) + 1;
                types[post.type] = (types[post.type] || 0) + 1;
            });
            
            let mostTopic = Object.keys(topics).reduce((a,b) => topics[a] > topics[b] ? a : b, 'None');
            if (document.getElementById('mostUsedTopic')) document.getElementById('mostUsedTopic').innerText = mostTopic;
            
            let typeNames = {'professional':'Professional','networking':'Networking','tech':'Technology','marketing':'Marketing','leadership':'Leadership','career':'Career'};
            let mostType = Object.keys(types).reduce((a,b) => types[a] > types[b] ? a : b, 'professional');
            if (document.getElementById('popularType')) document.getElementById('popularType').innerText = typeNames[mostType] || mostType;
            
            let totalLen = data.history.reduce((sum, p) => sum + p.content.length, 0);
            let avgLen = Math.round(totalLen / data.history.length);
            if (document.getElementById('avgLength')) document.getElementById('avgLength').innerText = avgLen;
            
            createCharts(types, data.history);
        } else if (historyDiv) {
            historyDiv.innerHTML = '<p class="text-muted" style="text-align:center; padding:20px;">No posts yet. Generate your first post!</p>';
            if (document.getElementById('totalPosts')) document.getElementById('totalPosts').innerText = '0';
            if (document.getElementById('mostUsedTopic')) document.getElementById('mostUsedTopic').innerText = '-';
            if (document.getElementById('popularType')) document.getElementById('popularType').innerText = '-';
            if (document.getElementById('avgLength')) document.getElementById('avgLength').innerText = '0';
            showEmptyCharts();
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function createCharts(types, history) {
    renderCharts(types, history);
}

function renderCharts(types, history) {
    const isDark = document.body.classList.contains('dark-mode');
    const colors = ['#2B5278', '#C49A45', '#3A6B9B', '#D97706', '#059669', '#6366F1', '#8B5CF6'];
    const typeNames = {'professional':'Professional','networking':'Networking','tech':'Technology','marketing':'Marketing','leadership':'Leadership','career':'Career'};
    
    const textColor = isDark ? '#A0A8B5' : '#4A525D';
    const legendColor = isDark ? '#EAECEF' : '#1A1E24';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

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
            type: 'doughnut',
            data: { 
                labels: labels, 
                datasets: [{ 
                    data: data, 
                    backgroundColor: colors.slice(0, labels.length), 
                    borderWidth: 2, 
                    borderColor: 'transparent' 
                }] 
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false, 
                plugins: { 
                    legend: { 
                        position: 'bottom',
                        labels: { 
                            color: legendColor,
                            font: { family: 'Plus Jakarta Sans', size: 11 } 
                        } 
                    } 
                } 
            }
        });
    }

    let timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx) {
        if (window.timelineChartObj) window.timelineChartObj.destroy();
        let timelineLabels = (history || []).slice(-7).map(p => p.date ? p.date.split(' ')[0] : 'Recent');
        if (timelineLabels.length === 0) timelineLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        let timelineData = (history || []).slice(-7).map((_, i) => i + 1);
        if (timelineData.length === 0) timelineData = [1, 2, 1, 3, 2, 4, 3];

        window.timelineChartObj = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: timelineLabels,
                datasets: [{
                    label: 'Drafts Created',
                    data: timelineData,
                    borderColor: isDark ? '#D4AF37' : '#2B5278',
                    backgroundColor: isDark ? 'rgba(212, 175, 55, 0.12)' : 'rgba(43, 82, 120, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { 
                        ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } },
                        grid: { display: false } 
                    },
                    y: { 
                        beginAtZero: true, 
                        ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } },
                        grid: { color: gridColor } 
                    }
                }
            }
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
        let response = await fetch(`${API_BASE_URL}/get-post/${id}`, {
            credentials: 'include'
        });
        let data = await response.json();
        if (response.ok && data.success) {
            document.getElementById('postContent').innerHTML = data.post.content.replace(/\n/g, '<br>');
            document.getElementById('postResult').style.display = 'block';
            let hashtags = document.getElementById('postHashtags');
            if (hashtags) hashtags.innerHTML = '';
            document.getElementById('postResult').scrollIntoView({behavior: 'smooth'});
        } else {
            alert(data.detail || 'Could not load post (Access denied or not logged in)');
        }
    } catch (error) {
        alert('Error loading post details');
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear your post history?')) return;
    try {
        let response = await fetch(`${API_BASE_URL}/delete-history`, {
            method: 'DELETE',
            credentials: 'include'
        });
        let data = await response.json();
        if (response.ok) {
            alert('History cleared');
            await loadHistory();
        } else {
            alert(data.detail || 'Could not clear history (Login required)');
        }
    } catch (e) {
        alert('Error clearing history');
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
        <div class="favorite-item" onclick="loadFavorite(${i})">
            <div>
                <strong class="item-topic">${escapeHtml(fav.topic)}</strong> 
                <span class="item-type-badge">${escapeHtml(fav.type)}</span>
            </div>
            <small class="item-date">${fav.date}</small>
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

    // Refresh history and charts with dynamic theme colors
    loadHistory();
    loadFavorites();
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