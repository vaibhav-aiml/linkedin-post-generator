from flask import Blueprint, request, jsonify
from backend.models.post_analyzer import PostAnalyzer
from backend.models.post_generator import PostGenerator
from backend.services.nlp_service import NLPService

api_bp = Blueprint('api', __name__)

# Initialize services
nlp_service = NLPService()
post_analyzer = PostAnalyzer(nlp_service)
post_generator = PostGenerator(nlp_service)

@api_bp.route('/analyze', methods=['POST'])
def analyze_posts():
    """Analyze LinkedIn posts"""
    try:
        data = request.json
        posts = data.get('posts', [])
        
        if not posts:
            return jsonify({'error': 'No posts provided'}), 400
        
        analysis_results = post_analyzer.load_posts(posts)
        top_performers = post_analyzer.get_top_performers()
        common_patterns = post_analyzer.get_common_patterns()
        
        return jsonify({
            'success': True,
            'analysis': analysis_results,
            'top_performers': top_performers,
            'common_patterns': common_patterns
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/generate-post', methods=['POST'])
def generate_post():
    """Generate a LinkedIn post"""
    try:
        data = request.json
        topic = data.get('topic')
        post_type = data.get('type', 'professional')
        tone = data.get('tone', 'professional')
        key_points = data.get('key_points', [])
        include_cta = data.get('include_cta', True)
        length = data.get('length', 'medium')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        generated = post_generator.generate_post(
            topic=topic,
            post_type=post_type,
            tone=tone,
            key_points=key_points,
            include_cta=include_cta,
            length=length
        )
        
        return jsonify({
            'success': True,
            'post': generated
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/generate-message', methods=['POST'])
def generate_message():
    """Generate a professional message"""
    try:
        data = request.json
        recipient = data.get('recipient_name')
        context = data.get('context')
        purpose = data.get('purpose', 'networking')
        
        if not recipient or not context:
            return jsonify({'error': 'Recipient name and context are required'}), 400
        
        message = post_generator.generate_message(recipient, context, purpose)
        
        return jsonify({
            'success': True,
            'message': message
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze a single piece of text"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        analysis = {
            'keywords': nlp_service.extract_keywords(text),
            'tone': nlp_service.analyze_tone(text),
            'structure': nlp_service.detect_post_structure(text),
            'engagement_patterns': nlp_service.analyze_engagement_patterns(text)
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500