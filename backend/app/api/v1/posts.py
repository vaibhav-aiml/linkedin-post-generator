from datetime import datetime
import hashlib
import urllib.parse
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.security import get_current_user_optional, get_current_user
from backend.app.models.user import User
from backend.app.models.post import Post
from backend.app.schemas.post import (
    PostCreateRequest,
    PostGenerationResponse,
    PostResponse,
    MessageCreateRequest,
    MessageResponse,
    ShareResponse
)
from backend.app.services.llm_service import LLMFactory

router = APIRouter(tags=["Posts & Generation"])


@router.post("/generate-post", response_model=PostGenerationResponse)
def generate_post(
    req: PostCreateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    try:
        llm_provider = LLMFactory.get_provider()
        content = llm_provider.generate_post(
            topic=req.topic,
            post_type=req.type,
            length=req.length,
            tone=req.tone
        )
        hashtags = llm_provider.generate_hashtags(req.topic)

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        raw_hash = f"{req.topic.strip()}:{content.strip()}:{now_str}"
        content_hash = hashlib.sha256(raw_hash.encode('utf-8')).hexdigest()

        new_post = Post(
            user_id=current_user.id if current_user else None,
            topic=req.topic,
            content=content,
            type=req.type,
            date=now_str,
            content_hash=content_hash
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return PostGenerationResponse(
            success=True,
            post=PostResponse(
                id=new_post.id,
                topic=new_post.topic,
                content=new_post.content,
                type=new_post.type,
                date=new_post.date,
                suggested_hashtags=hashtags
            )
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate post: {str(e)}"
        )


@router.post("/generate-message", response_model=MessageResponse)
def generate_message(req: MessageCreateRequest):
    try:
        llm_provider = LLMFactory.get_provider()
        message = llm_provider.generate_message(
            recipient=req.recipient_name,
            context=req.context,
            purpose=req.purpose or "networking"
        )
        return MessageResponse(success=True, message=message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate message: {str(e)}"
        )


@router.get("/get-history")
def get_history(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Post)
    if current_user:
        query = query.filter((Post.user_id == current_user.id) | (Post.user_id == None))
    
    posts = query.order_by(Post.id.desc()).limit(50).all()
    history = [
        {
            "id": p.id,
            "topic": p.topic,
            "content": p.content,
            "type": p.type,
            "date": p.date
        }
        for p in posts
    ]
    return {"success": True, "history": history, "count": len(history)}


@router.get("/get-post/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "success": True,
        "post": {
            "id": post.id,
            "topic": post.topic,
            "content": post.content,
            "type": post.type,
            "date": post.date
        }
    }


@router.delete("/delete-history")
def delete_history(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Post)
    if current_user:
        query.filter(Post.user_id == current_user.id).delete(synchronize_session=False)
    else:
        query.filter(Post.user_id == None).delete(synchronize_session=False)
    
    db.commit()
    return {"success": True, "message": "History cleared"}


@router.post("/share-to-linkedin", response_model=ShareResponse)
def share_to_linkedin(data: dict):
    content = data.get("content", "")
    encoded = urllib.parse.quote(content)
    share_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded}"
    return ShareResponse(success=True, share_url=share_url)
