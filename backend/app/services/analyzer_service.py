from typing import Dict, Any
from backend.app.schemas.analyzer import AnalysisMetrics
from backend.app.services.llm_service import LLMFactory


class AnalyzerService:
    @staticmethod
    def analyze_text(text: str) -> AnalysisMetrics:
        if not text or len(text.strip()) == 0:
            return AnalysisMetrics(
                score=0,
                rating="No Text",
                summary="Please paste a LinkedIn post to analyze",
                word_count=0,
                hashtag_count=0,
                question_count=0,
                has_emoji=False,
                suggestions=["Paste your LinkedIn post above"],
                improvement_tips=["Paste a post to get started"],
                corrected_version="",
                original_text="",
                length_status="No Data",
                length_message="Waiting for post",
                question_status="No Data",
                question_message="Add a question",
                hashtag_status="No Data",
                hashtag_message="Add hashtags",
                emoji_status="No Data",
                emoji_message="Add emojis"
            )

        words = text.split()
        word_count = len(words)
        question_count = text.count('?')
        hashtag_count = text.count('#')
        has_emoji = any(c in text for c in ['😊', '🚀', '💡', '✅', '📊', '🎯', '💻', '🤝', '✨', '🔥', '💪', '🎉'])

        score = 60

        # Word count scoring
        if 150 <= word_count <= 300:
            score += 15
            length_status = "Perfect"
            length_message = f"Great! {word_count} words is ideal for engagement"
        elif word_count < 100:
            score -= 10
            length_status = "Too Short"
            length_message = f"Only {word_count} words. Add more context"
        elif word_count > 400:
            score -= 10
            length_status = "Too Long"
            length_message = f"{word_count} words is slightly long for quick scrolling"
        elif word_count < 150:
            score += 5
            length_status = "Good"
            length_message = f"{word_count} words is good"
        else:
            score += 3
            length_status = "Acceptable"
            length_message = f"{word_count} words is acceptable"

        # Question scoring
        if question_count >= 2:
            score += 15
            question_status = "Excellent"
            question_message = f"{question_count} questions - great for comments"
        elif question_count == 1:
            score += 10
            question_status = "Good"
            question_message = "1 question - good for starting discussion"
        else:
            score -= 15
            question_status = "Missing"
            question_message = "No questions. Add one to boost engagement"

        # Hashtag scoring
        if 3 <= hashtag_count <= 5:
            score += 12
            hashtag_status = "Perfect"
            hashtag_message = f"{hashtag_count} hashtags - optimal range"
        elif hashtag_count == 2:
            score += 6
            hashtag_status = "Good"
            hashtag_message = "2 hashtags. Add 1-2 more"
        elif hashtag_count == 1:
            score += 3
            hashtag_status = "Low"
            hashtag_message = "Only 1 hashtag. Consider adding 2 more"
        elif hashtag_count > 5:
            score -= 5
            hashtag_status = "Too Many"
            hashtag_message = f"{hashtag_count} hashtags. Keep it to 3-5"
        else:
            score -= 10
            hashtag_status = "Missing"
            hashtag_message = "No hashtags. Add 3-5 relevant ones"

        # Emoji scoring
        if has_emoji:
            score += 5
            emoji_status = "Good"
            emoji_message = "Emojis add visual break and appeal"
        else:
            emoji_status = "Missing"
            emoji_message = "No emojis. Add 1-2 key emojis for emphasis"

        score = max(0, min(100, score))

        if score >= 85:
            rating = "Excellent"
            summary = "High quality post ready to publish"
        elif score >= 70:
            rating = "Good"
            summary = "Solid post with minor improvements possible"
        elif score >= 50:
            rating = "Average"
            summary = "Has potential but needs refinements"
        else:
            rating = "Needs Work"
            summary = "Significant improvements needed"

        # Base suggestions
        suggestions = []
        if word_count < 150:
            suggestions.append("Expand your post with concrete examples or key takeaways")
        if question_count == 0:
            suggestions.append("Include a compelling call-to-action question at the end")
        if hashtag_count < 3:
            suggestions.append("Add 3-5 industry-specific hashtags for discoverability")
        if not suggestions:
            suggestions = [
                "Hook readers early in the first line",
                "Ensure short paragraph spacing for mobile readability",
                "Share actionable metrics to increase shareability"
            ]

        tips = [
            "Break long blocks into 1-2 sentence paragraphs",
            "Use bullet points for lists to improve scannability",
            "Tag relevant experts or organizations to expand reach"
        ]

        # Dynamic AI Rewriting
        issues = {
            "word_count": word_count,
            "length_status": length_status,
            "question_count": question_count,
            "hashtag_count": hashtag_count,
            "has_emoji": has_emoji,
            "suggestions": suggestions
        }

        corrected_version = text
        try:
            llm = LLMFactory.get_provider()
            improved = llm.improve_post(original_text=text, issues=issues)
            if improved and improved.strip():
                corrected_version = improved.strip()
        except Exception:
            pass

        if corrected_version == text:
            fallback_parts = [text]
            if question_count == 0:
                fallback_parts.append("What are your thoughts on this? Share below! 👇")
            if hashtag_count < 3:
                fallback_parts.append("#ProfessionalGrowth #CareerAdvice #Leadership")
            corrected_version = "\n\n".join(fallback_parts)

        return AnalysisMetrics(
            score=score,
            rating=rating,
            summary=summary,
            word_count=word_count,
            hashtag_count=hashtag_count,
            question_count=question_count,
            has_emoji=has_emoji,
            suggestions=suggestions[:3],
            improvement_tips=tips[:3],
            corrected_version=corrected_version,
            original_text=text,
            length_status=length_status,
            length_message=length_message,
            question_status=question_status,
            question_message=question_message,
            hashtag_status=hashtag_status,
            hashtag_message=hashtag_message,
            emoji_status=emoji_status,
            emoji_message=emoji_message
        )
