import openai
import os
from typing import List, Dict, Optional
import json

class AIService:
    def __init__(self, api_key=None, use_local_model=False):
        self.use_local_model = use_local_model
        if not use_local_model and api_key:
            openai.api_key = api_key
        elif not use_local_model and not api_key:
            print("Warning: No OpenAI API key provided. Falling back to template-based generation.")
            self.use_local_model = True
            
    def generate_text(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate text using AI model"""
        if not self.use_local_model:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional LinkedIn content creator expert in writing engaging, professional posts."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._generate_local_fallback(prompt)
        else:
            return self._generate_local_fallback(prompt)
    
    def _generate_local_fallback(self, prompt: str) -> str:
        """Fallback generation without AI"""
        # Simple rule-based generation for demo purposes
        if "LinkedIn" in prompt and "post" in prompt:
            topic = self._extract_topic(prompt)
            return f"""I've been diving deep into {topic} recently, and here's what I've discovered.

The landscape is changing rapidly, and those who adapt will thrive. Key takeaways:
• Data-driven decisions are non-negotiable
• Customer experience is the new competitive advantage
• Continuous learning separates the best from the rest

What's your experience with {topic}? Share your thoughts below! 👇

#ProfessionalGrowth #{topic.replace(' ', '')} #Innovation"""
        
        return "Here's a professional post about your topic. Remember to add your personal insights to make it authentic!"
    
    def _extract_topic(self, prompt: str) -> str:
        """Extract topic from prompt"""
        import re
        match = re.search(r'about (.*?)(?:\.|\n|post)', prompt)
        if match:
            return match.group(1).strip()
        return "your industry"
    
    def analyze_post_quality(self, post_text: str) -> Dict:
        """Analyze the quality of a generated post"""
        analysis = {
            "score": 0,
            "suggestions": [],
            "strengths": []
        }
        
        # Basic quality checks
        word_count = len(post_text.split())
        if 150 <= word_count <= 300:
            analysis["score"] += 20
            analysis["strengths"].append("Optimal length for LinkedIn")
        elif word_count < 100:
            analysis["suggestions"].append("Consider adding more details to increase engagement")
        elif word_count > 500:
            analysis["suggestions"].append("Post might be too long for optimal engagement")
        
        # Check for engagement elements
        if "?" in post_text:
            analysis["score"] += 20
            analysis["strengths"].append("Includes questions to drive engagement")
        
        if any(cta in post_text.lower() for cta in ['comment', 'share', 'thoughts', 'agree']):
            analysis["score"] += 20
            analysis["strengths"].append("Has clear call-to-action")
        
        if "#" in post_text:
            analysis["score"] += 10
            analysis["strengths"].append("Uses relevant hashtags")
        
        if len(post_text.split('\n')) >= 3:
            analysis["score"] += 15
            analysis["strengths"].append("Good use of line breaks for readability")
        
        # Check for personal touch
        if any(word in post_text.lower() for word in ['i', 'my', 'we', 'our']):
            analysis["score"] += 15
            analysis["strengths"].append("Personal and authentic tone")
        
        return analysis