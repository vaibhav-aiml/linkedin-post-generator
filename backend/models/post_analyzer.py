import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

class PostAnalyzer:
    def __init__(self, nlp_service):
        self.nlp = nlp_service
        self.posts_data = []
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
    def load_posts(self, posts):
        """Load and analyze multiple LinkedIn posts"""
        self.posts_data = []
        for post in posts:
            analyzed = self.analyze_single_post(post)
            self.posts_data.append(analyzed)
        return self.posts_data
    
    def analyze_single_post(self, post):
        """Analyze a single LinkedIn post"""
        text = post.get('content', '')
        
        analysis = {
            'original_text': text,
            'keywords': self.nlp.extract_keywords(text),
            'tone': self.nlp.analyze_tone(text),
            'structure': self.nlp.detect_post_structure(text),
            'engagement_patterns': self.nlp.analyze_engagement_patterns(text),
            'length': len(text.split()),
            'metadata': {
                'likes': post.get('likes', 0),
                'comments': post.get('comments', 0),
                'date': post.get('date', '')
            }
        }
        
        # Calculate engagement score
        analysis['engagement_score'] = self._calculate_engagement_score(analysis)
        
        return analysis
    
    def _calculate_engagement_score(self, analysis):
        """Calculate an engagement score based on various factors"""
        score = 0
        
        # Tone impact
        if analysis['tone']['category'] in ['positive', 'very_positive']:
            score += 0.3
        elif analysis['tone']['category'] in ['negative', 'very_negative']:
            score -= 0.2
            
        # Structure impact
        if analysis['structure']['has_hook']:
            score += 0.2
        if analysis['structure']['has_conclusion']:
            score += 0.1
            
        # Engagement patterns
        patterns = analysis['engagement_patterns']
        if patterns['has_question']:
            score += 0.2
        if patterns['has_call_to_action']:
            score += 0.3
        if patterns['has_storytelling']:
            score += 0.15
        if patterns['has_data']:
            score += 0.1
            
        # Normalize score between 0 and 1
        return max(0, min(1, score))
    
    def get_top_performers(self, n=5):
        """Get top performing posts based on engagement"""
        sorted_posts = sorted(self.posts_data, 
                            key=lambda x: x['engagement_score'], 
                            reverse=True)
        return sorted_posts[:n]
    
    def get_common_patterns(self):
        """Identify common patterns among high-performing posts"""
        high_performers = [p for p in self.posts_data if p['engagement_score'] > 0.7]
        
        if not high_performers:
            return {}
        
        common_patterns = {
            'common_keywords': [],
            'common_tone': {},
            'common_structure': {},
            'common_patterns': {}
        }
        
        # Aggregate keywords
        all_keywords = []
        for post in high_performers:
            keywords = [kw[0] for kw in post['keywords'][:5]]
            all_keywords.extend(keywords)
        
        from collections import Counter
        common_patterns['common_keywords'] = Counter(all_keywords).most_common(10)
        
        # Aggregate tones
        tones = [post['tone']['category'] for post in high_performers]
        common_patterns['common_tone'] = Counter(tones).most_common()
        
        # Aggregate engagement patterns
        patterns_list = []
        for post in high_performers:
            patterns_list.append(post['engagement_patterns'])
        
        common_patterns['common_patterns'] = patterns_list
        
        return common_patterns