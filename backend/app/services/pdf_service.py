from io import BytesIO
import xml.sax.saxutils
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class PDFService:
    @staticmethod
    def create_post_pdf(content: str) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        story = [
            Paragraph("LinkedIn Post Export", styles['Heading1']),
            Spacer(1, 12)
        ]

        for line in content.split('\n'):
            if line.strip():
                safe_line = xml.sax.saxutils.escape(line)
                story.append(Paragraph(safe_line, styles['Normal']))
                story.append(Spacer(1, 6))

        doc.build(story)
        buffer.seek(0)
        return buffer

