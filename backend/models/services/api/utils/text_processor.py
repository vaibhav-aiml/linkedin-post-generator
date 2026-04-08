import re
from textblob import TextBlob
from typing import List, Tuple

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', '', text)
        return text.strip()
    
    @staticmethod
    def extract_emojis(text: str) -> List[str]:
        """Extract emojis from text"""
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.findall(text)
    
    @staticmethod
    def calculate_readability(text: str) -> dict:
        """Calculate readability scores"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        if not sentences or not words:
            return {'score': 0, 'level': 'Unable to calculate'}
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Flesch Reading Ease (simplified)
        if avg_words_per_sentence < 10:
            readability = "Very Easy"
            score = 90
        elif avg_words_per_sentence < 15:
            readability = "Easy"
            score = 70
        elif avg_words_per_sentence < 20:
            readability = "Moderate"
            score = 50
        elif avg_words_per_sentence < 25:
            readability = "Difficult"
            score = 30
        else:
            readability = "Very Difficult"
            score = 10
        
        return {
            'score': score,
            'level': readability,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1)
        }
    
    @staticmethod
    def suggest_improvements(text: str) -> List[str]:
        """Suggest improvements for the text"""
        suggestions = []
        
        # Check length
        word_count = len(text.split())
        if word_count < 100:
            suggestions.append("Consider adding more details or examples to increase value")
        elif word_count > 500:
            suggestions.append("Post might be too long. Consider breaking into multiple posts")
        
        # Check for personal touch
        if "I" not in text and "we" not in text:
            suggestions.append("Add personal experiences or opinions to make it more authentic")
        
        # Check for engagement
        if "?" not in text:
            suggestions.append("Add a question to encourage comments and discussion")
        
        # Check for call to action
        cta_words = ['comment', 'share', 'thoughts', 'agree', 'think']
        if not any(word in text.lower() for word in cta_words):
            suggestions.append("Include a clear call-to-action (e.g., 'What are your thoughts?')")
        
        # Check for line breaks
        if '\n' not in text and len(text) > 200:
            suggestions.append("Add line breaks to improve readability")
        
        # Check for hashtags
        if '#' not in text:
            suggestions.append("Add relevant hashtags to increase discoverability")
        
        return suggestions
    
    @staticmethod
    def format_for_linkedin(text: str) -> str:
        """Format text specifically for LinkedIn"""
        # Add line breaks every 2-3 sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        formatted = []
        
        for i, sentence in enumerate(sentences):
            formatted.append(sentence)
            if (i + 1) % 2 == 0 and i < len(sentences) - 1:
                formatted.append('\n\n')
            else:
                formatted.append(' ')
        
        result = ''.join(formatted).strip()
        
        # Ensure maximum length
        if len(result) > 3000:
            result = result[:2997] + "..."
        
        return result