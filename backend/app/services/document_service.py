import io
import re
from typing import Dict, Any, Tuple
from fastapi import HTTPException, status, UploadFile
import pypdf

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/pjpeg"
}
MAX_EXTRACTED_CHARS = 2000  # ~500-800 tokens


HTTP_413_CONTENT_TOO_LARGE = getattr(status, "HTTP_413_CONTENT_TOO_LARGE", getattr(status, "HTTP_413_REQUEST_ENTITY_TOO_LARGE", 413))
HTTP_422_UNPROCESSABLE_CONTENT = getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", getattr(status, "HTTP_422_UNPROCESSABLE_ENTITY", 422))
HTTP_415_UNSUPPORTED_MEDIA_TYPE = getattr(status, "HTTP_415_UNSUPPORTED_MEDIA_TYPE", 415)


class DocumentService:
    @staticmethod
    def validate_file(file: UploadFile, content_bytes: bytes) -> str:
        # Check file size
        if len(content_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=HTTP_413_CONTENT_TOO_LARGE,
                detail=f"File size exceeds 5MB limit. Current size: {len(content_bytes) / (1024 * 1024):.2f}MB"
            )

        filename = file.filename or ""
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        content_type = (file.content_type or "").lower()

        if ext not in ALLOWED_EXTENSIONS and content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type '{ext or content_type}'. Please upload a .pdf certificate or document."
            )

        return ext

    @classmethod
    def extract_context(cls, file: UploadFile, content_bytes: bytes) -> Dict[str, Any]:
        ext = cls.validate_file(file, content_bytes)

        if ext in {".png", ".jpg", ".jpeg"}:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Scanned image files and images require OCR. Please upload a text-based PDF certificate."
            )

        # PDF extraction
        try:
            reader = pypdf.PdfReader(io.BytesIO(content_bytes))
            pages_text = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    pages_text.append(text.strip())
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Failed to parse PDF document: {str(e)}"
            )

        raw_text = "\n\n".join(pages_text).strip()
        if not raw_text:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_CONTENT,
                detail="No extractable text found in this PDF. It appears to be a scanned image. Please upload a text-based PDF certificate."
            )


        extracted_context, doc_type, warnings = cls._summarize_context(raw_text)

        return {
            "success": True,
            "extracted_context": extracted_context,
            "document_type": doc_type,
            "warnings": warnings
        }

    @staticmethod
    def _summarize_context(raw_text: str) -> Tuple[str, str, list]:
        warnings = []
        # Normalize whitespace and excessive newlines
        cleaned = re.sub(r'[ \t]+', ' ', raw_text)
        cleaned_lines = [line.strip() for line in cleaned.splitlines() if line.strip()]

        # Identify document type
        lower_full = raw_text.lower()
        if any(term in lower_full for term in ["certificate", "certify", "certified", "completed", "awarded to", "license", "credential"]):
            doc_type = "certificate"
        elif any(term in lower_full for term in ["report", "quarterly", "executive summary", "whitepaper", "analysis"]):
            doc_type = "report"
        else:
            doc_type = "document"

        # Cap length to ~500-800 tokens (~2000 chars)
        joined_text = "\n".join(cleaned_lines)
        if len(joined_text) > MAX_EXTRACTED_CHARS:
            extracted_context = joined_text[:MAX_EXTRACTED_CHARS].rsplit(' ', 1)[0] + "..."
            warnings.append("Extracted content was truncated to fit context budget.")
        else:
            extracted_context = joined_text

        return extracted_context, doc_type, warnings
