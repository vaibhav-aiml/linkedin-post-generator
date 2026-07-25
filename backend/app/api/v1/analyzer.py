from fastapi import APIRouter
from backend.app.schemas.analyzer import AnalyzeRequest, AnalyzeResponse
from backend.app.services.analyzer_service import AnalyzerService

router = APIRouter(tags=["Analyzer"])


@router.post("/analyze-text", response_model=AnalyzeResponse)
def analyze_text(req: AnalyzeRequest):
    metrics = AnalyzerService.analyze_text(req.text)
    return AnalyzeResponse(success=True, analysis=metrics)
