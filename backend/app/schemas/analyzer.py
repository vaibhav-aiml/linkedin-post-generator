from typing import List, Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Post text to analyze")


class AnalysisMetrics(BaseModel):
    score: int
    rating: str
    summary: str
    word_count: int
    hashtag_count: int
    question_count: int
    has_emoji: bool
    suggestions: List[str]
    improvement_tips: List[str]
    corrected_version: str
    original_text: Optional[str] = ""
    length_status: str
    length_message: str
    question_status: str
    question_message: str
    hashtag_status: str
    hashtag_message: str
    emoji_status: str
    emoji_message: str


class AnalyzeResponse(BaseModel):
    success: bool = True
    analysis: AnalysisMetrics
