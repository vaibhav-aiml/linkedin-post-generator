from fastapi import APIRouter, Response
from backend.app.services.pdf_service import PDFService

router = APIRouter(tags=["Export"])


@router.post("/export-pdf")
def export_pdf(data: dict):
    content = data.get("content", "")
    pdf_buffer = PDFService.create_post_pdf(content)
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=linkedin_post.pdf"}
    )
