from typing import List, Optional
from pydantic import BaseModel, Field


class PostCreateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, description="Topic of the LinkedIn post")
    type: str = Field("professional", description="Type/Category of the post")
    length: str = Field("medium", description="Length: short, medium, or long")
    tone: Optional[str] = Field("professional", description="Tone of the post")
    key_points: Optional[List[str]] = Field(default=[], description="Bullet points to include")
    include_cta: Optional[bool] = Field(True, description="Whether to include call-to-action")


class PostResponse(BaseModel):
    id: Optional[int] = None
    topic: str
    content: str
    type: str
    date: Optional[str] = None
    suggested_hashtags: List[str] = []


class PostGenerationResponse(BaseModel):
    success: bool = True
    post: PostResponse


class MessageCreateRequest(BaseModel):
    recipient_name: str = Field(..., min_length=1, max_length=100)
    context: str = Field(..., min_length=2, max_length=500)
    purpose: Optional[str] = Field("networking")


class MessageResponse(BaseModel):
    success: bool = True
    message: str


class ShareResponse(BaseModel):
    success: bool = True
    share_url: str
