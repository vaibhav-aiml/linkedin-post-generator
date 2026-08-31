from fastapi import APIRouter, Request
from backend.app.core.limiter import limiter
from backend.app.schemas.analyzer import AnalyzeRequest, AnalyzeResponse
from backend.app.services.analyzer_service import AnalyzerService

router = APIRouter(tags=["Analyzer"])


@router.post("/analyze-text", response_model=AnalyzeResponse)
@limiter.limit("10/minute")
def analyze_text(request: Request, req: AnalyzeRequest):
    metrics = AnalyzerService.analyze_text(req.text)
    return AnalyzeResponse(success=True, analysis=metrics)

