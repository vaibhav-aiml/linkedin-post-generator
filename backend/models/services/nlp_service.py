import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from collections import Counter
import string

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

class NLPService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        # Remove punctuation and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Convert to lowercase
        text = text.lower()
        return text.strip()
    
    def extract_keywords(self, text, top_n=10):
        """Extract important keywords from text"""
        cleaned = self.clean_text(text)
        words = word_tokenize(cleaned)
        # Filter stopwords and short words
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
        keyword_freq = Counter(keywords)
        return keyword_freq.most_common(top_n)
    
    def analyze_tone(self, text):
        """Analyze the tone of the post"""
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        
        tone = {
            'sentiment_score': sentiment['compound'],
            'positive': sentiment['pos'],
            'negative': sentiment['neg'],
            'neutral': sentiment['neu']
        }
        
        # Determine tone category
        if tone['sentiment_score'] >= 0.5:
            tone['category'] = 'very_positive'
        elif tone['sentiment_score'] > 0:
            tone['category'] = 'positive'
        elif tone['sentiment_score'] == 0:
            tone['category'] = 'neutral'
        elif tone['sentiment_score'] > -0.5:
            tone['category'] = 'negative'
        else:
            tone['category'] = 'very_negative'
            
        return tone
    
    def detect_post_structure(self, text):
        """Analyze the structure of the post"""
        sentences = sent_tokenize(text)
        structure = {
            'sentence_count': len(sentences),
            'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
            'has_hook': any(len(s.split()) < 10 for s in sentences[:2]),  # Short first sentence as hook
            'has_conclusion': len(sentences) > 2,
            'sections': self._identify_sections(sentences)
        }
        return structure
    
    def _identify_sections(self, sentences):
        """Identify different sections of the post"""
        sections = []
        if len(sentences) >= 3:
            sections.append('opening')
            sections.append('body')
            sections.append('conclusion')
        return sections
    
    def analyze_engagement_patterns(self, text):
        """Identify patterns that drive engagement"""
        patterns = {
            'has_question': '?' in text,
            'has_call_to_action': any(phrase in text.lower() for phrase in [
                'comment', 'share', 'like', 'agree', 'thoughts', 'opinion'
            ]),
            'has_storytelling': len(text.split()) > 100,
            'has_data': any(char.isdigit() for char in text),
            'has_lists': text.count('\n•') > 0 or text.count('\n-') > 0
        }
        return patterns