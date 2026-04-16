from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from datetime import datetime
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

app = Flask(__name__)
CORS(app)

HISTORY_FILE = 'post_history.json'
post_history = []

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'r') as f:
            post_history = json.load(f)
        print(f"Loaded {len(post_history)} posts")
    except:
        print("No existing history")

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
        
        if post_type == 'professional':
            content = f"""What I Have Learned About {topic} After 5 Years in the Industry

The journey to mastering {topic} has been nothing short of transformative. Looking back, I wish someone had shared these insights with me when I was starting out.

The Biggest Lesson: Consistency Over Intensity

When I first started working with {topic}, I thought success meant working 80 hour weeks and sacrificing everything else. I was wrong. The people who truly excel in {topic} are not the ones who work the hardest for a week and burn out. They are the ones who show up every single day, even when motivation is low.

Building Genuine Relationships Matters More Than Technical Skills

Early in my career, I focused entirely on learning technical aspects of {topic}. I ignored networking and relationship building. That was a mistake. The opportunities that changed my career came from people I had built genuine connections with, not from random job applications or cold emails.

Never Stop Learning

{topic} evolves constantly. What was cutting edge two years ago is now standard practice. The professionals who thrive are the ones who dedicate time each week to learning something new. I make it a habit to read one book, take one course, or attend one workshop every month.

Take Imperfect Action

Analysis paralysis is real. I spent months planning before taking action. Now I follow a simple rule: take imperfect action. You can always adjust course, but you cannot steer a parked car.

Your Turn

What is the most important lesson you have learned in your {topic} journey? I would genuinely love to hear your perspective in the comments below.

Save this post for when you need a reminder to keep going.

#{topic.replace(' ', '')} #ProfessionalGrowth #CareerAdvice #LessonsLearned #Motivation"""

        elif post_type == 'tech':
            content = f"""The State of {topic} in 2024: What Every Professional Needs to Know

After spending considerable time researching and working with {topic}, I want to share my honest observations about where this field is heading.

The landscape is changing faster than ever before. What was considered advanced just 18 months ago is now becoming table stakes. Here is what you need to know.

First, AI integration is no longer optional. Every company is finding ways to incorporate intelligence into their {topic} workflows. If you are not exploring this, you are falling behind.

Second, cloud native architectures have won. The debate is over. Organizations that have not migrated are now playing catch up. The efficiency gains are too significant to ignore.

Third, security must be built in from day one. The era of adding security as an afterthought is over. Zero trust models are becoming standard practice across the industry.

Fourth, sustainability is becoming a competitive advantage. Efficient code means lower cloud costs and smaller carbon footprints. Green coding is not just ethical, it is economical.

What does this mean for you?

If you are early in your career, focus on fundamentals. The specific tools will change, but solid understanding of core principles will serve you for decades.

If you are a manager, invest in upskilling your team. The skills gap is widening and those who invest in learning will pull ahead.

If you are a leader, create a culture of continuous learning. The organizations that learn fastest will win.

The Bottom Line

{topic} is transforming from a technical specialty to a business necessity. The question is not whether you should adopt these practices, but how quickly you can.

Let me know in the comments, what trend in {topic} excites you most right now?

Tag a colleague who needs to see this.

#{topic.replace(' ', '')} #TechTrends #Innovation #CloudComputing #FutureOfWork"""

        elif post_type == 'marketing':
            content = f"""Marketing in {topic}: What Actually Works in 2024

I have run hundreds of marketing campaigns and spent significant budget testing different strategies. Here is what I have learned about what actually works in {topic} and what is a complete waste of time.

Strategy One: Know Your Audience Deeply

Most marketing fails because it tries to speak to everyone. When you speak to everyone, you connect with no one. The most successful campaigns I have run were targeted at very specific segments. Get granular about who you are trying to reach.

Strategy Two: Provide Value Before Asking for Anything

The best marketing is helpful marketing. I have seen conversion rates triple when we shifted from selling to helping. Share insights, answer questions, solve problems. When you give first, people will naturally want to work with you.

Strategy Three: Measure What Actually Matters

Vanity metrics like likes and shares feel good but they do not pay the bills. Focus on metrics that tie directly to business outcomes. Cost per acquisition, customer lifetime value, and return on ad spend are what executives actually care about.

Strategy Four: Test Everything

I cannot tell you how many times my assumptions have been wrong. The only way to know what works is to test. Run small experiments, measure results, scale what works, and kill what does not.

Common Mistakes I See

Not having a clear value proposition. Trying to be everywhere at once. Ignoring data. Forgetting to follow up.

Your Action Items for This Week

Audit your current marketing strategy. Identify one thing you are doing that is not working. Stop doing it. Identify one thing you could test. Run a small experiment.

What marketing strategy has worked best for you this year? I am genuinely curious to learn from your experience.

#{topic.replace(' ', '')} #MarketingStrategy #DigitalMarketing #BusinessGrowth #MarketingTips"""

        elif post_type == 'leadership':
            content = f"""Leadership Lessons from {topic}: What 10 Years of Leading Teams Has Taught Me

I have made plenty of mistakes as a leader. I want to share the most important lessons I have learned so you can avoid making the same errors I did.

Lesson One: Listen More Than You Speak

Early in my leadership journey, I thought I needed to have all the answers. I would jump in with solutions before fully understanding problems. This was a terrible approach. The best ideas almost always come from the people doing the work every day. Create space for your team to share their thoughts.

Lesson Two: Psychological Safety Is Everything

Teams that feel safe to speak up, admit mistakes, and share ideas outperform teams that do not by a significant margin. I have seen this play out repeatedly. As a leader, your most important job is creating an environment where people feel psychologically safe.

Lesson Three: Micromanagement Destroys Morale

I used to micromanage because I cared deeply about quality. What I did not realize was that I was destroying my team's motivation and creativity. Hire great people, set clear expectations, and then get out of their way. Trust is the foundation of high performing teams.

Lesson Four: Admit When You Are Wrong

Pretending to have all the answers erodes trust. Being honest about your mistakes builds respect and shows your team that it is okay to be human. Some of the most powerful moments in my career came from simply saying, I was wrong about that.

Lesson Five: Develop Other Leaders

Your true legacy is not the projects you completed or the revenue you generated. It is the leaders you helped develop. Spend meaningful time mentoring your team. Their growth is your ultimate measure of success.

A Challenge for You

Pick one of these principles and apply it intentionally this week. Then ask your team for feedback. You might be surprised by what you learn.

What is the best leadership advice you have ever received? I would love to learn from your experience.

#{topic.replace(' ', '')} #Leadership #Management #TeamBuilding #CareerGrowth #ExecutiveLeadership"""

        elif post_type == 'career':
            content = f"""Career Advice for Anyone Building a Future in {topic}

I have made many mistakes in my career journey. Here is what I wish someone had told me earlier.

Stop Comparing Yourself to Others

Social media makes it look like everyone is succeeding except you. This is not reality. People share their wins, not their struggles. Focus on your own progress. Compare yourself only to who you were yesterday.

Say Yes to Opportunities That Scare You

Growth happens outside your comfort zone. The projects I was most nervous about taught me the most. When an opportunity scares you, that is usually a sign you should take it.

Build Relationships Before You Need Them

Reach out to people you admire. Offer help without expecting anything in return. Your network will be there for you when you need it, but only if you have invested in those relationships beforehand.

Take Care of Yourself

Burnout is real and it will catch up with you. I learned this the hard way. Your career is a marathon, not a sprint. Rest is productive. Exercise is not optional. Sleep is not for the weak.

Ask for Help

No one succeeds alone. The most successful people I know are not afraid to admit what they do not know. Asking for help is a sign of strength, not weakness.

Your 30 Day Career Plan

Week one, identify one skill you want to develop. Week two, find a mentor or course. Week three, practice that skill daily. Week four, share what you learned with your network.

What is one piece of career advice you would give to someone just starting out? Share your wisdom in the comments.

#{topic.replace(' ', '')} #CareerAdvice #ProfessionalDevelopment #GrowthMindset #JobSearch #Success"""

        else:
            content = f"""Everything I Wish I Knew About {topic} Before I Started

Looking back at my journey, here are the most important lessons I have learned about {topic}. I hope these insights save you time and frustration.

Lesson One: Done Is Better Than Perfect

I wasted so much time trying to make things perfect before sharing them. This was fear disguised as perfectionism. Now I follow a simple rule, ship early and iterate based on feedback.

Lesson Two: Ask for Help

I used to struggle alone, thinking I needed to figure everything out myself. This was foolish. No one succeeds alone. The most successful people I know are not afraid to admit what they do not know.

Lesson Three: Consistency Beats Intensity

Working hard for a week then burning out does not create lasting results. Small daily actions compound into remarkable outcomes over time. Show up every day, even when you do not feel like it.

Lesson Four: Your Attitude Determines Your Altitude

Challenges will come. Setbacks will happen. How you respond to them matters more than the challenges themselves. I have seen talented people fail because of poor attitude and less talented people succeed because of great attitude.

Lesson Five: Help Others Generously

The best way to advance your own career is to help others advance theirs. Share what you learn. Make introductions. Give credit freely. What goes around truly does come around.

A Practical Exercise

Write down one thing you learned this week about {topic}. Share it with your network. You will be surprised how many people appreciate your insights.

What is the most important lesson you have learned in your professional journey? I would love to hear your perspective.

#{topic.replace(' ', '')} #LifeLessons #GrowthMindset #Wisdom #PersonalDevelopment #Success"""

        save_post(topic, content, post_type)
        
        return jsonify({
            'success': True,
            'post': {
                'content': content,
                'type': post_type,
                'suggested_hashtags': [f'#{topic.replace(" ", "")}', '#LinkedIn', '#ProfessionalGrowth', '#CareerAdvice']
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Keep all other routes the same as before
@app.route('/api/generate-message', methods=['POST'])
def generate_message():
    try:
        data = request.json
        recipient = data.get('recipient_name', '')
        context = data.get('context', '')
        
        message = f"""Hello {recipient},

I came across your profile and was impressed by your work in {context}. I am also passionate about this field and would love to connect.

I believe we could learn a lot from each other. Would you be open to a quick chat sometime next week?

Looking forward to connecting.

Best regards
[Your Name]"""
        
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        text = data.get('text', '')
        word_count = len(text.split())
        has_question = '?' in text
        has_hashtags = '#' in text
        hashtag_count = text.count('#')
        
        score = 60
        suggestions = []
        
        if 150 <= word_count <= 300:
            score += 15
        elif word_count < 100:
            score -= 10
            suggestions.append("Add more details to make your post more valuable")
        
        if has_question:
            score += 15
        else:
            score -= 15
            suggestions.append("Add a question to encourage comments and discussion")
        
        if has_hashtags:
            if 3 <= hashtag_count <= 5:
                score += 10
            else:
                suggestions.append("Use 3 to 5 hashtags for best results")
        else:
            score -= 8
            suggestions.append("Add 3 to 5 relevant hashtags for better discoverability")
        
        score = max(0, min(100, score))
        
        if score >= 85:
            rating = "Excellent"
            summary = "This is a high quality post ready to publish"
        elif score >= 70:
            rating = "Good"
            summary = "This is a solid post with minor improvements possible"
        elif score >= 50:
            rating = "Average"
            summary = "This post has potential but needs several improvements"
        else:
            rating = "Needs Work"
            summary = "This post needs significant improvements to perform well"
        
        return jsonify({
            'success': True,
            'analysis': {
                'score': score,
                'rating': rating,
                'summary': summary,
                'word_count': word_count,
                'has_question': has_question,
                'has_hashtags': has_hashtags,
                'hashtag_count': hashtag_count,
                'suggestions': suggestions
            }
        })
    except Exception as e:
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
    print("LinkedIn Post Generator Backend")
    print("Running on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)