from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Post history storage
HISTORY_FILE = 'post_history.json'
post_history = []

# Load existing history if file exists
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'r') as f:
            post_history = json.load(f)
    except:
        post_history = []

def save_post_to_history(topic, content, post_type, engagement_score=None):
    """Save generated post to history"""
    global post_history
    history_entry = {
        'id': len(post_history) + 1,
        'topic': topic,
        'content': content,
        'type': post_type,
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'engagement_score': engagement_score or 0,
        'likes': 0,
        'comments': 0
    }
    post_history.insert(0, history_entry)
    # Keep only last 50 posts
    if len(post_history) > 50:
        post_history = post_history[:50]
    
    # Save to file
    with open(HISTORY_FILE, 'w') as f:
        json.dump(post_history, f, indent=2)
    
    return history_entry

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running successfully!'
    })

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    try:
        data = request.json
        topic = data.get('topic', 'your industry')
        post_type = data.get('type', 'professional')
        
        # Professional post template
        if post_type == 'professional':
            content = f"""📊 Professional Insight: {topic}

Here's what I've learned about {topic}:

Key Takeaways:
• The landscape is evolving rapidly
• Data-driven decisions are crucial
• Innovation drives success

What's your experience with {topic}? Let's discuss in the comments! 👇

#{topic.replace(' ', '')} #ProfessionalGrowth #Leadership"""
        
        elif post_type == 'networking':
            content = f"""🤝 Let's connect and grow together!

I'm passionate about {topic} and looking to connect with like-minded professionals.

If you're interested in:
• {topic} trends and insights
• Collaboration opportunities
• Knowledge sharing

Let's connect and create value together!

#{topic.replace(' ', '')} #Networking #Collaboration"""
        
        elif post_type == 'achievement':
            content = f"""✨ Excited to share my journey with {topic}

After dedicated effort, I've gained valuable insights:
1. Continuous learning is key
2. Building relationships matters
3. Taking action creates results

What's one thing you've learned about {topic}?

Share your thoughts below! 👇

#{topic.replace(' ', '')} #GrowthMindset #Success"""

        elif post_type == 'tech':
            content = f"""💻 Tech Talk: {topic}

The technology landscape is evolving faster than ever!

Hot Trends:
🔹 AI integration everywhere
🔹 Cloud-native architectures
🔹 Cybersecurity first approach

What tech trends are you most excited about?

#{topic.replace(' ', '')} #TechTrends #Innovation"""

        elif post_type == 'marketing':
            content = f"""📢 Marketing Mastery: {topic}

In today's digital world, successful marketing requires:

✅ Deep audience understanding
✅ Authentic storytelling
✅ Data-driven decisions

What's working in your marketing strategy?

#{topic.replace(' ', '')} #DigitalMarketing #Growth"""

        elif post_type == 'leadership':
            content = f"""👥 Leadership Lessons: {topic}

Great leaders know that success comes from:

1️⃣ Empowering your team
2️⃣ Embracing failure as learning
3️⃣ Leading with empathy

What's the best leadership advice you've received?

#{topic.replace(' ', '')} #Leadership #Management"""

        elif post_type == 'career':
            content = f"""🚀 Career Growth: {topic}

Your career journey is unique. Here's what I've learned:

✨ Never stop learning
✨ Build meaningful relationships
✨ Take calculated risks

What's one career decision that changed your life?

#{topic.replace(' ', '')} #CareerAdvice #Success"""
                    # NEW: Sales & Business Development template
        elif post_type == 'sales':
            content = f"""💰 Sales & Business Development: {topic}

Here's what drives success in {topic}:

Key Strategies:
🎯 Focus on solving customer problems
🤝 Build genuine relationships
📈 Track and optimize metrics
💡 Always provide value first

Remember: People buy from people they trust!

What's your #1 sales tip?

#{topic.replace(' ', '')} #SalesTips #BusinessGrowth #Revenue"""

        # NEW: Personal Branding template
        elif post_type == 'branding':
            content = f"""✨ Personal Branding: {topic}

Your personal brand is your superpower!

3 Steps to Build Your Brand:
1️⃣ Define your unique value
2️⃣ Share your journey authentically
3️⃣ Engage with your community consistently

What makes your personal brand unique?

#{topic.replace(' ', '')} #PersonalBranding #Authenticity #CareerGrowth"""

        # NEW: Productivity & Workflow template
        elif post_type == 'productivity':
            content = f"""⚡ Productivity Hacks: {topic}

Stop working harder. Start working smarter!

My Top Productivity Tips:
✅ Prioritize deep work
✅ Eliminate distractions
✅ Batch similar tasks
✅ Take strategic breaks

What's your best productivity hack?

#{topic.replace(' ', '')} #Productivity #WorkSmart #TimeManagement"""

        # NEW: Diversity & Inclusion template
        elif post_type == 'diversity':
            content = f"""🌍 Diversity & Inclusion: {topic}

Inclusive workplaces are stronger workplaces!

Why D&I Matters:
• Different perspectives drive innovation
• Psychological safety boosts performance
• Belonging increases retention
• Diversity reflects our global community

How are you promoting inclusion at work?

#{topic.replace(' ', '')} #DiversityAndInclusion #Equity #WorkplaceCulture"""

        # NEW: Remote Work template
        elif post_type == 'remote':
            content = f"""🏠 Remote Work Wisdom: {topic}

Remote work is here to stay!

Success Factors:
📍 Clear communication channels
📍 Trust-based culture
📍 Work-life boundaries
📍 Virtual team building

What's your best remote work advice?

#{topic.replace(' ', '')} #RemoteWork #WFH #FutureOfWork"""

        # NEW: Learning & Development template
        elif post_type == 'learning':
            content = f"""📚 Lifelong Learning: {topic}

The best investment you can make is in yourself!

Learning Strategies:
🎓 Set weekly learning goals
📖 Read industry books
🎧 Listen to podcasts
🤝 Learn from mentors

What skill are you currently developing?

#{topic.replace(' ', '')} #LifelongLearning #SkillUp #ProfessionalDevelopment"""

        else:
            content = f"""💡 Quick Thoughts on {topic}

Here's my perspective:
• Stay curious and keep learning
• Collaborate and share knowledge
• Focus on creating value

What are your thoughts?

#{topic.replace(' ', '')} #ProfessionalGrowth"""
        
        # Save to history
        save_post_to_history(topic, content, post_type)
        
        return jsonify({
            'success': True,
            'post': {
                'content': content,
                'type': post_type,
                'suggested_hashtags': [
                    f'#{topic.replace(" ", "")}', 
                    '#LinkedIn', 
                    '#Professional',
                    '#Growth'
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-message', methods=['POST'])
def generate_message():
    try:
        data = request.json
        recipient = data.get('recipient_name', 'there')
        context = data.get('context', 'professional opportunities')
        purpose = data.get('purpose', 'networking')
        
        if purpose == 'networking':
            message = f"""Hi {recipient},

I came across your profile and was impressed by your work in {context}.

Would love to connect and learn from your experience.

Best regards,
[Your Name]"""
        
        elif purpose == 'collaboration':
            message = f"""Hello {recipient},

I'm working on {context} and believe there could be a great collaboration opportunity.

Would you be open to a brief chat next week?

Looking forward to connecting!"""
        
        else:
            message = f"""Dear {recipient},

I'm reaching out regarding {context}. Your expertise in this area would be invaluable.

Would appreciate any insights you could share.

Thank you!"""
        
        return jsonify({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        text = data.get('text', '')
        
        # Basic analysis
        word_count = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        has_question = '?' in text
        has_hashtags = '#' in text
        
        # Generate suggestions
        suggestions = []
        if word_count < 100:
            suggestions.append("Add more details to increase value")
        if word_count > 500:
            suggestions.append("Consider shortening for better engagement")
        if not has_question:
            suggestions.append("Add a question to encourage comments")
        if not has_hashtags:
            suggestions.append("Add relevant hashtags for discoverability")
        
        return jsonify({
            'success': True,
            'analysis': {
                'word_count': word_count,
                'sentence_count': sentences,
                'has_question': has_question,
                'has_hashtags': has_hashtags,
                'suggestions': suggestions,
                'is_optimal': 150 <= word_count <= 300
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New endpoints for history and sharing
@app.route('/api/get-history', methods=['GET'])
def get_history():
    """Get all post history"""
    global post_history
    return jsonify({
        'success': True,
        'history': post_history,
        'count': len(post_history)
    })

@app.route('/api/get-post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get specific post by ID"""
    global post_history
    post = next((p for p in post_history if p['id'] == post_id), None)
    if post:
        return jsonify({'success': True, 'post': post})
    return jsonify({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/delete-history', methods=['DELETE'])
def delete_history():
    """Delete all history"""
    global post_history
    post_history = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return jsonify({'success': True, 'message': 'History cleared'})

@app.route('/api/share-to-linkedin', methods=['POST'])
def share_to_linkedin():
    """Generate shareable LinkedIn URL"""
    try:
        data = request.json
        content = data.get('content', '')
        
        # Encode content for URL
        import urllib.parse
        encoded_content = urllib.parse.quote(content)
        
        # LinkedIn share URL
        share_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_content}"
        
        return jsonify({
            'success': True,
            'share_url': share_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("=" * 50)
    print("🚀 LinkedIn Post Generator Backend")
    print(f"📍 Running on: http://localhost:{port}")
    print(f"📝 Health check: http://localhost:{port}/api/health")
    print("=" * 50)
    app.run(debug=True, port=port)