import io
import pytest
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_sample_pdf_bytes(text: str) -> bytes:
    """Helper to create a valid text-based PDF in memory."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Certificate of Achievement", styles['Heading1']),
        Spacer(1, 12),
        Paragraph(text, styles['Normal'])
    ]
    doc.build(story)
    return buf.getvalue()


def test_upload_document_success(client):
    """Test extracting achievement context from a text-based certificate PDF."""
    cert_text = "This certifies that Jane Doe has successfully completed AWS Certified Solutions Architect Associate on August 2026."
    pdf_bytes = create_sample_pdf_bytes(cert_text)

    files = {
        "file": ("aws_certificate.pdf", pdf_bytes, "application/pdf")
    }

    response = client.post("/api/v1/upload-document", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["document_type"] == "certificate"
    assert "AWS Certified Solutions Architect" in data["extracted_context"]
    assert "Jane Doe" in data["extracted_context"]


def test_upload_document_unsupported_file_type(client):
    """Test that non-PDF / non-image file types (e.g., .txt, .exe) are rejected with 415."""
    files = {
        "file": ("script.exe", b"binarycontent", "application/octet-stream")
    }
    response = client.post("/api/v1/upload-document", files=files)
    assert response.status_code == 415
    assert "unsupported file type" in response.json()["detail"].lower()


def test_upload_document_file_too_large(client):
    """Test that files exceeding 5MB are rejected with 413."""
    oversized_data = b"%PDF-1.4 " + (b"0" * (5 * 1024 * 1024 + 1024))
    files = {
        "file": ("large_doc.pdf", oversized_data, "application/pdf")
    }
    response = client.post("/api/v1/upload-document", files=files)
    assert response.status_code == 413
    assert "exceeds 5mb" in response.json()["detail"].lower()


def test_upload_image_returns_ocr_guidance(client):
    """Test that image uploads without OCR support return 422 with clear guidance."""
    fake_png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    files = {
        "file": ("certificate.png", fake_png, "image/png")
    }
    response = client.post("/api/v1/upload-document", files=files)
    assert response.status_code == 422
    assert "require ocr" in response.json()["detail"].lower() or "text-based pdf" in response.json()["detail"].lower()


def test_upload_empty_file_rejected(client):
    """Test that uploading an empty file returns 400."""
    files = {
        "file": ("empty.pdf", b"", "application/pdf")
    }
    response = client.post("/api/v1/upload-document", files=files)
    assert response.status_code == 400
