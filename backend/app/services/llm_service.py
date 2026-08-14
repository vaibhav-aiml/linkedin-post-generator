from abc import ABC, abstractmethod
from typing import List
from backend.app.core.config import settings


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_post(self, topic: str, post_type: str, length: str, tone: str) -> str:
        pass

    @abstractmethod
    def generate_hashtags(self, topic: str) -> List[str]:
        pass

    @abstractmethod
    def generate_message(self, recipient: str, context: str, purpose: str) -> str:
        pass


class GroqProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        from groq import Groq
        self.client = Groq(api_key=api_key)

    def generate_post(self, topic: str, post_type: str, length: str, tone: str) -> str:
        length_map = {'short': '150-200 words', 'medium': '350-450 words', 'long': '550-700 words'}
        target_length = length_map.get(length, '350-450 words')

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

        prompt = f"""Write an engaging LinkedIn post about "{topic}".

Requirements:
- Tone: {config['tone']}
- Style: {config['style']}
- Length: {target_length}
- Write in first person as a professional sharing real insights
- Include a thoughtful question at the end to encourage comments
- Use short paragraphs and line breaks for easy reading
- Sound authentic and personal
- Start with a strong hook that grabs attention
"""
        max_tokens = min(settings.MAX_LLM_TOKENS_PER_POST, 1200)

        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert LinkedIn content creator who writes engaging, high-performing posts."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=max_tokens
        )
        return chat_completion.choices[0].message.content

    def generate_hashtags(self, topic: str) -> List[str]:
        hashtag_prompt = f"Generate 5 relevant hashtags for a LinkedIn post about {topic}. Return only the hashtags separated by spaces, like this: #Topic #Example #Tags"
        hashtag_response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": hashtag_prompt}],
            model="openai/gpt-oss-20b",
            temperature=0.5,
            max_tokens=100
        )
        tags = hashtag_response.choices[0].message.content.strip().split()
        return [t for t in tags if t.startswith('#')][:5]

    def generate_message(self, recipient: str, context: str, purpose: str) -> str:
        prompt = f"Write a professional LinkedIn message to {recipient} regarding {context} for {purpose} purposes. Keep it polite, personalized, under 150 words."
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-20b",
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    def generate_post(self, topic: str, post_type: str, length: str, tone: str) -> str:
        prompt = f"Write an engaging LinkedIn post about '{topic}'. Post Type: {post_type}, Length: {length}, Tone: {tone}."
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert LinkedIn content strategist."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=settings.MAX_LLM_TOKENS_PER_POST
        )
        return response.choices[0].message.content

    def generate_hashtags(self, topic: str) -> List[str]:
        prompt = f"Generate 5 trending hashtags for LinkedIn about {topic}. Return only the hashtags separated by spaces."
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
            max_tokens=100
        )
        tags = response.choices[0].message.content.strip().split()
        return [t for t in tags if t.startswith('#')][:5]

    def generate_message(self, recipient: str, context: str, purpose: str) -> str:
        prompt = f"Write a concise, professional LinkedIn connection message to {recipient} about {context} ({purpose}). Keep under 150 words."
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
            max_tokens=300
        )
        return response.choices[0].message.content


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_post(self, topic: str, post_type: str, length: str, tone: str) -> str:
        prompt = f"Write an engaging LinkedIn post about '{topic}'. Style: {post_type}, Length: {length}, Tone: {tone}."
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=settings.MAX_LLM_TOKENS_PER_POST,
            system="You are a professional LinkedIn content writer.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def generate_hashtags(self, topic: str) -> List[str]:
        prompt = f"Generate 5 relevant hashtags for a LinkedIn post about {topic}. Return only hashtags separated by spaces."
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        tags = response.content[0].text.strip().split()
        return [t for t in tags if t.startswith('#')][:5]

    def generate_message(self, recipient: str, context: str, purpose: str) -> str:
        prompt = f"Write a polite, engaging LinkedIn message to {recipient} about {context} for {purpose}."
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class MockLLMProvider(BaseLLMProvider):
    def generate_post(self, topic: str, post_type: str, length: str, tone: str) -> str:
        return f"""🚀 Key Lessons I've Learned About {topic.title()}

Over the past few years working in this field, I've realized that continuous learning and adaptability are everything.

Here are 3 major takeaways:
1. Done is better than perfect.
2. Focus on clear, value-driven execution.
3. Help others along the journey.

What are your thoughts on {topic}? Have you noticed a similar trend in your industry?

#ProfessionalGrowth #{topic.replace(' ', '')} #Leadership #CareerGrowth"""

    def generate_hashtags(self, topic: str) -> List[str]:
        clean = topic.replace(" ", "")
        return [f"#{clean}", "#Professional", "#Networking", "#Career", "#Growth"]

    def generate_message(self, recipient: str, context: str, purpose: str) -> str:
        return f"Hello {recipient},\n\nI came across your profile and loved your work in {context}. Would love to connect and share insights!\n\nBest regards,\n[Your Name]"


class LLMFactory:
    @staticmethod
    def get_provider() -> BaseLLMProvider:
        provider_type = settings.LLM_PROVIDER.lower()

        if provider_type == "groq" and settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("your_"):
            try:
                return GroqProvider(api_key=settings.GROQ_API_KEY)
            except Exception:
                pass

        if provider_type == "openai" and settings.OPENAI_API_KEY:
            try:
                return OpenAIProvider(api_key=settings.OPENAI_API_KEY)
            except Exception:
                pass

        if provider_type == "anthropic" and settings.ANTHROPIC_API_KEY:
            try:
                return AnthropicProvider(api_key=settings.ANTHROPIC_API_KEY)
            except Exception:
                pass

        return MockLLMProvider()
