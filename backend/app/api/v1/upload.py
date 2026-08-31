from typing import List, Optional
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from pydantic import BaseModel

from backend.app.core.limiter import limiter
from backend.app.services.document_service import DocumentService

router = APIRouter(tags=["Document Upload"])


class DocumentUploadResponse(BaseModel):
    success: bool = True
    extracted_context: str
    document_type: str
    warnings: List[str] = []


@router.post("/upload-document", response_model=DocumentUploadResponse)
@limiter.limit("10/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):
    try:
        content_bytes = await file.read()
        if not content_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )

        result = DocumentService.extract_context(file, content_bytes)
        return DocumentUploadResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process uploaded document: {str(e)}"
        )
    finally:
        await file.close()
