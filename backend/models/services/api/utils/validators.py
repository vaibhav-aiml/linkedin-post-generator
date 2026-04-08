import re
from typing import Dict, List, Tuple

class Validators:
    @staticmethod
    def validate_post_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate post generation input"""
        errors = []
        
        # Check required fields
        if not data.get('topic'):
            errors.append("Topic is required")
        
        # Validate topic length
        topic = data.get('topic', '')
        if len(topic) < 3:
            errors.append("Topic must be at least 3 characters")
        if len(topic) > 100:
            errors.append("Topic must be less than 100 characters")
        
        # Validate post type
        valid_types = ['professional', 'networking', 'achievement', 'thought_leadership', 'insight', 'problem']
        if data.get('type') and data['type'] not in valid_types:
            errors.append(f"Invalid post type. Must be one of: {', '.join(valid_types)}")
        
        # Validate tone
        valid_tones = ['professional', 'friendly', 'thoughtful', 'positive', 'negative', 'neutral']
        if data.get('tone') and data['tone'] not in valid_tones:
            errors.append(f"Invalid tone. Must be one of: {', '.join(valid_tones)}")
        
        # Validate key points
        key_points = data.get('key_points', [])
        if len(key_points) > 5:
            errors.append("Maximum 5 key points allowed")
        
        for point in key_points:
            if len(point) > 100:
                errors.append("Each key point must be less than 100 characters")
        
        # Validate length
        valid_lengths = ['short', 'medium', 'long']
        if data.get('length') and data['length'] not in valid_lengths:
            errors.append(f"Invalid length. Must be one of: {', '.join(valid_lengths)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_message_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate message generation input"""
        errors = []
        
        if not data.get('recipient_name'):
            errors.append("Recipient name is required")
        elif len(data['recipient_name']) > 50:
            errors.append("Recipient name must be less than 50 characters")
        
        if not data.get('context'):
            errors.append("Context is required")
        elif len(data['context']) > 200:
            errors.append("Context must be less than 200 characters")
        
        valid_purposes = ['networking', 'job_inquiry', 'collaboration', 'follow_up']
        if data.get('purpose') and data['purpose'] not in valid_purposes:
            errors.append(f"Invalid purpose. Must be one of: {', '.join(valid_purposes)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS and other issues"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        
        # Remove potentially dangerous characters
        text = re.sub(r'[<>{}]', '', text)
        
        # Limit length
        if len(text) > 5000:
            text = text[:5000]
        
        return text.strip()