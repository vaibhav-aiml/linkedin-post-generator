from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from datetime import datetime
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from groq import Groq

app = Flask(__name__)
CORS(app)

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'YOUR_GROQ_API_KEY_HERE')
client = Groq(api_key=GROQ_API_KEY)

HISTORY_FILE = 'post_history.json'
post_history = []

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'r') as f:
            post_history = json.load(f)
    except:
        pass

def save_post(topic, content, post_type):
    global post_history
    new_post = {
        'id': len(post_history) + 1,
        'topic': topic,
        'content': content,
        'type': post_type,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    post_history.insert(0, new_post)
    if len(post_history) > 50:
        post_history = post_history[:50]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(post_history, f, indent=2)
    return new_post

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    try:
        data = request.json
        topic = data.get('topic', '')
        post_type = data.get('type', 'professional')
        length = data.get('length', 'medium')
        
        # Map length to word count
        length_map = {'short': '150-200 words', 'medium': '350-450 words', 'long': '550-700 words'}
        target_length = length_map.get(length, '350-450 words')
        
        # Map post type to tone and style
        type_config = {
            'professional': {'tone': 'professional and insightful', 'style': 'share lessons learned and actionable advice'},
            'networking': {'tone': 'friendly and connection-oriented', 'style': 'invite conversation and relationship building'},
            'achievement': {'tone': 'celebratory and humble', 'style': 'share a milestone with gratitude and lessons'},
            'tech': {'tone': 'technical and forward-thinking', 'style': 'discuss trends, tools, and predictions'},
            'marketing': {'tone': 'strategic and value-driven', 'style': 'share proven strategies and results'},
            'leadership': {'tone': 'inspirational and practical', 'style': 'share leadership principles and real examples'},
            'career': {'tone': 'supportive and actionable', 'style': 'give career advice and encouragement'}
        }
        config = type_config.get(post_type, type_config['professional'])
        
        # Create prompt for Groq
        prompt = f"""Write an engaging LinkedIn post about "{topic}".

Requirements:
- Tone: {config['tone']}
- Style: {config['style']}
- Length: {target_length}
- Write in first person as a professional sharing real insights
- Include a thoughtful question at the end to encourage comments
- Use 3-5 relevant hashtags at the end
- Use short paragraphs and line breaks for easy reading
- Sound authentic and personal, not like AI wrote it
- Start with a strong hook that grabs attention
- Include specific, practical advice or insights

The post should be valuable for professionals in this field."""

        # Call Groq API - using Llama 3.3 70B (excellent quality)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a expert LinkedIn content creator who writes engaging, valuable posts that professionals love to read and share."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1200
        )
        
        content = chat_completion.choices[0].message.content
        
        # Generate hashtags separately
        hashtag_prompt = f"Generate 5 relevant hashtags for a LinkedIn post about {topic}. Return only the hashtags separated by spaces, like this: #Topic #Example #Tags"
        hashtag_response = client.chat.completions.create(
            messages=[{"role": "user", "content": hashtag_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=100
        )
        hashtags = hashtag_response.choices[0].message.content.strip().split()
        
        save_post(topic, content, post_type)
        
        return jsonify({
            'success': True,
            'post': {
                'content': content,
                'type': post_type,
                'suggested_hashtags': hashtags[:5]
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Keep all your other routes (generate-message, analyze-text, get-history, etc.)
# They remain exactly the same as before

@app.route('/api/generate-message', methods=['POST'])
def generate_message():
    try:
        data = request.json
        recipient = data.get('recipient_name', '')
        context = data.get('context', '')
        
        message_prompt = f"""Write a professional LinkedIn connection message to {recipient} about {context}.

Requirements:
- Be polite and respectful
- Show genuine interest in their work
- Keep it concise (100-150 words)
- End with a clear call to action
- Sound authentic, not like a template"""

        message_response = client.chat.completions.create(
            messages=[{"role": "user", "content": message_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=300
        )
        message = message_response.choices[0].message.content
        
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        # Fallback to template if API fails
        message = f"""Hello {recipient},

I came across your profile and was impressed by your work in {context}.

Would love to connect and learn from your experience.

Best regards,
[Your Name]"""
        return jsonify({'success': True, 'message': message})

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text or len(text.strip()) == 0:
            return jsonify({
                'success': True,
                'analysis': {
                    'score': 0,
                    'rating': 'No Text',
                    'summary': 'Please paste a LinkedIn post to analyze',
                    'word_count': 0,
                    'hashtag_count': 0,
                    'question_count': 0,
                    'has_emoji': False,
                    'suggestions': ['Paste your LinkedIn post above'],
                    'improvement_tips': ['Paste a post to get started'],
                    'corrected_version': '',
                    'length_status': 'No Data',
                    'length_message': 'Waiting for post',
                    'question_status': 'No Data',
                    'question_message': 'Add a question',
                    'hashtag_status': 'No Data',
                    'hashtag_message': 'Add hashtags',
                    'emoji_status': 'No Data',
                    'emoji_message': 'Add emojis'
                }
            })
        
        # Calculate basic metrics
        word_count = len(text.split())
        question_count = text.count('?')
        hashtag_count = text.count('#')
        has_question = question_count > 0
        has_emoji = any(c in text for c in ['😊', '🚀', '💡', '✅', '📊', '🎯', '💻', '🤝', '✨', '🔥', '💪', '🎉'])
        
        # Score calculation
        score = 60
        
        # Length scoring
        if 150 <= word_count <= 300:
            score += 15
            length_status = "Perfect"
            length_message = f"Great! {word_count} words is ideal"
        elif word_count < 100:
            score -= 10
            length_status = "Too Short"
            length_message = f"Only {word_count} words. Add more content"
        elif word_count > 400:
            score -= 10
            length_status = "Too Long"
            length_message = f"{word_count} words is too long"
        elif word_count < 150:
            score += 5
            length_status = "Good"
            length_message = f"{word_count} words. Add 50 more"
        else:
            score += 3
            length_status = "Acceptable"
            length_message = f"{word_count} words is acceptable"
        
        # Question scoring
        if question_count >= 2:
            score += 15
            question_status = "Excellent"
            question_message = f"{question_count} questions - great for engagement"
        elif question_count == 1:
            score += 10
            question_status = "Good"
            question_message = "1 question - good for discussion"
        else:
            score -= 15
            question_status = "Missing"
            question_message = "No questions. Add one to engage readers"
        
        # Hashtag scoring
        if 3 <= hashtag_count <= 5:
            score += 12
            hashtag_status = "Perfect"
            hashtag_message = f"{hashtag_count} hashtags - ideal"
        elif hashtag_count == 2:
            score += 6
            hashtag_status = "Good"
            hashtag_message = "2 hashtags. Add 1-2 more"
        elif hashtag_count == 1:
            score += 3
            hashtag_status = "Low"
            hashtag_message = "Only 1 hashtag. Add 2-4 more"
        elif hashtag_count > 5:
            score -= 5
            hashtag_status = "Too Many"
            hashtag_message = f"{hashtag_count} hashtags. Use 3-5"
        else:
            score -= 10
            hashtag_status = "Missing"
            hashtag_message = "No hashtags. Add 3-5 relevant ones"
        
        # Emoji scoring
        if has_emoji:
            score += 5
            emoji_status = "Good"
            emoji_message = "Emojis add visual appeal"
        else:
            emoji_status = "Missing"
            emoji_message = "No emojis. Add 1-2 relevant ones"
        
        score = max(0, min(100, score))
        
        # Rating
        if score >= 85:
            rating = "Excellent"
            summary = "High quality post ready to publish"
        elif score >= 70:
            rating = "Good"
            summary = "Solid post with minor improvements"
        elif score >= 50:
            rating = "Average"
            summary = "Has potential but needs improvements"
        else:
            rating = "Needs Work"
            summary = "Significant improvements needed"
        
        # Generate suggestions using Groq
        suggestions_prompt = f"""Analyze this LinkedIn post and provide 3 specific, actionable suggestions for improvement. Keep each suggestion brief (under 15 words).

Post: {text[:1000]}

Return only the suggestions as a numbered list, no other text."""

        try:
            suggestions_response = client.chat.completions.create(
                messages=[{"role": "user", "content": suggestions_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=200
            )
            suggestions_text = suggestions_response.choices[0].message.content
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip() and s.strip()[0].isdigit()]
        except:
            suggestions = ["Add more personal experience", "Include a question", "Use relevant hashtags"]
        
        # Generate improvement tips
        tips_prompt = f"""For this LinkedIn post, provide 3 quick tips on how to make it more engaging. Keep each tip under 15 words.

Post: {text[:500]}

Return only the tips as a numbered list."""

        try:
            tips_response = client.chat.completions.create(
                messages=[{"role": "user", "content": tips_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=200
            )
            tips_text = tips_response.choices[0].message.content
            improvement_tips = [t.strip() for t in tips_text.split('\n') if t.strip() and t.strip()[0].isdigit()]
        except:
            improvement_tips = ["Start with a hook", "End with a question", "Add a personal story"]
        
        # Generate corrected version
        corrected_prompt = f"""Improve this LinkedIn post to make it more engaging. Fix any issues with length, questions, hashtags, or emojis. Return only the improved post, no explanations.

Original post: {text}"""

        try:
            corrected_response = client.chat.completions.create(
                messages=[{"role": "user", "content": corrected_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=1000
            )
            corrected_version = corrected_response.choices[0].message.content
        except:
            corrected_version = text
        
        return jsonify({
            'success': True,
            'analysis': {
                'score': score,
                'rating': rating,
                'summary': summary,
                'word_count': word_count,
                'hashtag_count': hashtag_count,
                'question_count': question_count,
                'has_emoji': has_emoji,
                'suggestions': suggestions[:3],
                'improvement_tips': improvement_tips[:3],
                'corrected_version': corrected_version,
                'original_text': text,
                'length_status': length_status,
                'length_message': length_message,
                'question_status': question_status,
                'question_message': question_message,
                'hashtag_status': hashtag_status,
                'hashtag_message': hashtag_message,
                'emoji_status': emoji_status,
                'emoji_message': emoji_message
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-history', methods=['GET'])
def get_history():
    return jsonify({'success': True, 'history': post_history, 'count': len(post_history)})

@app.route('/api/get-post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    for post in post_history:
        if post['id'] == post_id:
            return jsonify({'success': True, 'post': post})
    return jsonify({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/delete-history', methods=['DELETE'])
def delete_history():
    global post_history
    post_history = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return jsonify({'success': True, 'message': 'History cleared'})

@app.route('/api/share-to-linkedin', methods=['POST'])
def share_to_linkedin():
    try:
        data = request.json
        content = data.get('content', '')
        import urllib.parse
        encoded = urllib.parse.quote(content)
        return jsonify({'success': True, 'share_url': f"https://www.linkedin.com/sharing/share-offsite/?text={encoded}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.json
        content = data.get('content', '')
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("LinkedIn Post", styles['Heading1']), Spacer(1, 12)]
        for line in content.split('\n'):
            if line.strip():
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 6))
        doc.build(story)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='linkedin_post.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("LinkedIn Post Generator Backend (Powered by Groq AI)")
    print("Running on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0') 