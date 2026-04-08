import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict
import time

class LinkedInScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_profile_posts(self, profile_url: str, limit: int = 10) -> List[Dict]:
        """
        Scrape posts from a LinkedIn profile
        Note: This is a simplified version. LinkedIn requires authentication for full access.
        """
        # For demo purposes, return sample data
        # In production, you'd need to use LinkedIn API or proper authentication
        return self._get_sample_posts()
    
    def _get_sample_posts(self) -> List[Dict]:
        """Return sample LinkedIn posts for testing"""
        sample_posts = [
            {
                "content": """Excited to announce that our team just hit a major milestone! 🎉 

After months of hard work, we've successfully launched our new AI-powered analytics platform. This tool is going to revolutionize how businesses understand their customer data.

Key features:
• Real-time insights
• Predictive analytics
• Customizable dashboards

The future of data analytics is here! Would love to hear your thoughts on how AI is transforming your industry.

#DataAnalytics #AI #Innovation""",
                "likes": 245,
                "comments": 34,
                "date": "2024-01-15"
            },
            {
                "content": """The biggest lesson I learned in 2024? 

Success doesn't come from working harder—it comes from working smarter.

Here's what changed my perspective:
1. Prioritize deep work over busy work
2. Automate repetitive tasks
3. Invest in continuous learning
4. Build meaningful relationships

What's one thing you're doing differently this year? 

#Productivity #CareerGrowth #Leadership""",
                "likes": 189,
                "comments": 47,
                "date": "2024-01-10"
            },
            {
                "content": """Just finished reading "Atomic Habits" by James Clear, and I'm blown away by one concept:

Small changes compound into remarkable results.

In my career, I've seen this play out countless times:
• Writing daily → Became a thought leader
• Networking weekly → Built a powerful community
• Learning monthly → Stayed ahead of industry trends

What small habit has transformed your professional life?

#PersonalDevelopment #Habits #Success""",
                "likes": 312,
                "comments": 89,
                "date": "2024-01-05"
            },
            {
                "content": """Remote work isn't going anywhere. Here's why companies should embrace it:

✅ Access to global talent
✅ Higher employee satisfaction
✅ Reduced overhead costs
✅ Increased productivity (yes, really!)

The companies fighting this trend will be left behind.

What's your remote work experience been like?

#RemoteWork #FutureOfWork #HR""",
                "likes": 567,
                "comments": 123,
                "date": "2024-01-01"
            },
            {
                "content": """Stop trying to please everyone. 

In business and in life, you can't be everything to everyone.

Focus on your ideal audience:
• Who needs you most?
• Where can you add unique value?
• What problems can you solve?

When you niche down, you stand out.

Agree or disagree?

#Marketing #Strategy #BusinessGrowth""",
                "likes": 421,
                "comments": 67,
                "date": "2023-12-28"
            }
        ]
        return sample_posts[:limit] if limit else sample_posts
    
    def analyze_hashtags(self, posts: List[Dict]) -> Dict:
        """Analyze hashtag usage in posts"""
        hashtag_counts = {}
        
        for post in posts:
            content = post.get('content', '')
            hashtags = re.findall(r'#\w+', content)
            
            for tag in hashtags:
                hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        # Sort by frequency
        sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'popular_hashtags': sorted_hashtags[:10],
            'total_unique_hashtags': len(hashtag_counts),
            'avg_hashtags_per_post': sum(hashtag_counts.values()) / len(posts) if posts else 0
        }
    
    def get_engagement_metrics(self, posts: List[Dict]) -> Dict:
        """Calculate engagement metrics from posts"""
        if not posts:
            return {}
        
        total_likes = sum(post.get('likes', 0) for post in posts)
        total_comments = sum(post.get('comments', 0) for post in posts)
        
        return {
            'total_likes': total_likes,
            'total_comments': total_comments,
            'avg_likes_per_post': total_likes / len(posts),
            'avg_comments_per_post': total_comments / len(posts),
            'engagement_rate': (total_likes + total_comments) / len(posts),
            'best_performing_post': max(posts, key=lambda x: x.get('likes', 0) + x.get('comments', 0))
        }