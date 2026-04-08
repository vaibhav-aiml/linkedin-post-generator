import random
from typing import Dict, List, Optional

class PostGenerator:
    def __init__(self, nlp_service, ai_service=None):
        self.nlp = nlp_service
        self.ai_service = ai_service
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load post templates for different scenarios"""
        return {
            'professional_achievement': {
                'structure': [
                    "Excited to share that {achievement}",
                    "This journey taught me {lesson}",
                    "Grateful to {people} for their support",
                    "Looking forward to {future_goal}"
                ],
                'tone': 'positive'
            },
            'industry_insight': {
                'structure': [
                    "Here's what I learned about {topic} recently",
                    "The key insight is {insight}",
                    "This matters because {reason}",
                    "What are your thoughts on this?"
                ],
                'tone': 'professional'
            },
            'networking_message': {
                'structure': [
                    "Hi {name}, I've been following your work on {topic}",
                    "Your recent post about {post_topic} really resonated",
                    "Would love to connect and learn more about {interest}",
                    "Looking forward to connecting!"
                ],
                'tone': 'friendly'
            },
            'problem_solving': {
                'structure': [
                    "Here's a challenge I've been thinking about: {problem}",
                    "After analysis, here's my approach: {solution}",
                    "The results so far: {results}",
                    "Would appreciate your insights on {specific_aspect}"
                ],
                'tone': 'thoughtful'
            }
        }
    
    def generate_post(self, 
                     topic: str, 
                     post_type: str = 'professional',
                     tone: str = 'professional',
                     key_points: List[str] = None,
                     include_cta: bool = True,
                     length: str = 'medium') -> Dict:
        """Generate a LinkedIn post based on parameters"""
        
        if self.ai_service:
            # Use AI service for generation
            return self._generate_with_ai(topic, post_type, tone, key_points, include_cta, length)
        else:
            # Use template-based generation
            return self._generate_with_templates(topic, post_type, tone, key_points, include_cta, length)
    
    def _generate_with_ai(self, topic, post_type, tone, key_points, include_cta, length):
        """Generate post using AI service (GPT or similar)"""
        prompt = self._create_ai_prompt(topic, post_type, tone, key_points, include_cta, length)
        generated_text = self.ai_service.generate_text(prompt)
        
        return {
            'content': generated_text,
            'type': post_type,
            'tone': tone,
            'analysis': self.nlp.analyze_tone(generated_text),
            'suggested_hashtags': self._generate_hashtags(topic, generated_text)
        }
    
    def _create_ai_prompt(self, topic, post_type, tone, key_points, include_cta, length):
        """Create prompt for AI model"""
        length_map = {'short': '150-200', 'medium': '250-300', 'long': '400-500'}
        
        prompt = f"""Write a LinkedIn {post_type} post about {topic}. 
        Tone should be {tone}. 
        Length: {length_map[length]} characters.
        """
        
        if key_points:
            prompt += f"\nInclude these key points: {', '.join(key_points)}"
        
        if include_cta:
            prompt += "\nEnd with a call to action asking for engagement."
        
        prompt += "\nMake it engaging, professional, and suitable for LinkedIn audience."
        
        return prompt
    
    def _generate_with_templates(self, topic, post_type, tone, key_points, include_cta, length):
        """Generate post using template-based approach"""
        template_key = self._match_template(post_type, tone)
        template = self.templates.get(template_key, self.templates['industry_insight'])
        
        # Fill template placeholders
        post_content = []
        for sentence_template in template['structure']:
            filled = self._fill_template(sentence_template, topic, key_points)
            post_content.append(filled)
        
        # Adjust length
        if length == 'short':
            post_content = post_content[:3]
        elif length == 'long':
            post_content = post_content + self._add_expansion(topic)
        
        full_post = '\n\n'.join(post_content)
        
        # Add call to action if needed
        if include_cta and not self._has_cta(full_post):
            full_post += f"\n\nWhat are your thoughts on {topic}? Share in the comments below! 👇"
        
        # Add line breaks for readability
        full_post = self._add_line_breaks(full_post)
        
        return {
            'content': full_post,
            'type': post_type,
            'tone': tone,
            'analysis': self.nlp.analyze_tone(full_post),
            'suggested_hashtags': self._generate_hashtags(topic, full_post)
        }
    
    def _match_template(self, post_type, tone):
        """Match user parameters to appropriate template"""
        mapping = {
            ('professional', 'positive'): 'professional_achievement',
            ('networking', 'friendly'): 'networking_message',
            ('insight', 'professional'): 'industry_insight',
            ('problem', 'thoughtful'): 'problem_solving'
        }
        return mapping.get((post_type, tone), 'industry_insight')
    
    def _fill_template(self, template, topic, key_points):
        """Fill template placeholders with actual content"""
        replacements = {
            '{topic}': topic,
            '{achievement}': f"my achievement in {topic}",
            '{lesson}': "the importance of continuous learning",
            '{people}': "my amazing team",
            '{future_goal}': "more innovations",
            '{insight}': f"key insight about {topic}",
            '{reason}': "it's transforming our industry",
            '{problem}': f"the {topic} challenge",
            '{solution}': "a systematic approach",
            '{results}': "promising early results",
            '{specific_aspect}': f"the {topic} methodology"
        }
        
        # Add key points if available
        if key_points and '{key_points}' in template:
            replacements['{key_points}'] = ', '.join(key_points)
        
        filled = template
        for placeholder, value in replacements.items():
            filled = filled.replace(placeholder, value)
        
        return filled
    
    def _add_expansion(self, topic):
        """Add additional content for longer posts"""
        expansions = [
            f"This approach to {topic} has several benefits...",
            f"Here's a real example of how {topic} made a difference...",
            f"The data shows that {topic} is becoming increasingly important...",
            f"I'd love to hear how others are approaching {topic}."
        ]
        return random.sample(expansions, 2)
    
    def _has_cta(self, text):
        """Check if post already has a call to action"""
        cta_phrases = ['comment', 'share', 'thoughts', 'opinion', 'let me know', 'agree?']
        return any(phrase in text.lower() for phrase in cta_phrases)
    
    def _add_line_breaks(self, text):
        """Add line breaks for better readability on LinkedIn"""
        sentences = text.split('. ')
        formatted = '.\n\n'.join(sentences[:3])  # Break after first few sentences
        if len(sentences) > 3:
            formatted += '.\n\n' + '. '.join(sentences[3:])
        return formatted
    
    def _generate_hashtags(self, topic, text):
        """Generate relevant hashtags for the post"""
        # Extract key terms from topic and text
        key_terms = self.nlp.extract_keywords(text + ' ' + topic, top_n=5)
        
        # Convert to hashtags
        hashtags = [f"#{term[0].replace(' ', '')}" for term in key_terms[:3]]
        
        # Add industry standard hashtags
        industry_tags = ['#LinkedIn', '#ProfessionalGrowth', '#Career']
        
        # Combine and limit to 5 hashtags
        all_hashtags = hashtags + industry_tags
        return list(dict.fromkeys(all_hashtags))[:5]
    
    def generate_message(self, recipient_name: str, context: str, purpose: str) -> str:
        """Generate a professional LinkedIn message"""
        templates = {
            'networking': f"Hi {recipient_name}, I came across your profile and was impressed by your work in {context}. Would love to connect and learn from your experience.",
            'job_inquiry': f"Dear {recipient_name}, I'm reaching out regarding {context}. Your expertise would be valuable, and I'd appreciate any insights you could share.",
            'collaboration': f"Hello {recipient_name}, I'm working on {context} and believe there could be a great collaboration opportunity. Would you be open to a brief chat?",
            'follow_up': f"Hi {recipient_name}, following up on {context}. Would love to continue our conversation about potential synergies."
        }
        
        message = templates.get(purpose, templates['networking'])
        
        # Add personalization
        message += f"\n\nLooking forward to connecting and sharing ideas about {context}."
        
        return message