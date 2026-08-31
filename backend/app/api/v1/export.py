from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from backend.app.core.database import get_db
from backend.app.core.limiter import limiter
from backend.app.core.security import get_current_user_optional
from backend.app.models.user import User
from backend.app.models.post import Post
from backend.app.services.pdf_service import PDFService

router = APIRouter(tags=["Export"])


class ExportPDFRequest(BaseModel):
    content: Optional[str] = Field(None, description="Raw content to export as PDF (max 5000 chars)")
    post_id: Optional[int] = Field(None, description="Optional ID of saved post to export")



@router.post("/export-pdf")
@limiter.limit("10/minute")
def export_pdf(
    request: Request,
    data: ExportPDFRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    pdf_content = ""

    if data.post_id is not None:
        post = db.query(Post).filter(Post.id == data.post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        # Ownership check
        if post.user_id is not None:
            if not current_user or current_user.id != post.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You do not own this post"
                )
        pdf_content = post.content
    elif data.content:
        if len(data.content) > 5000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content exceeds maximum allowed length of 5000 characters"
            )
        pdf_content = data.content
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either post_id or content must be provided"
        )

    if not pdf_content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF content cannot be empty"
        )

    pdf_buffer = PDFService.create_post_pdf(pdf_content)
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=linkedin_post.pdf"}
    )

