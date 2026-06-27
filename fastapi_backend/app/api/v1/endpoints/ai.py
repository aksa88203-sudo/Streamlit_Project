from fastapi import APIRouter, Depends

from app.api.deps import get_ai_suite_service
from app.schemas.ai import AIInsightRequest, AIInsightResponse
from app.services.ai_suite import AISuiteService

router = APIRouter(prefix="/ai", tags=["AI Suite"])


@router.post("/insights", response_model=AIInsightResponse)
def generate_ai_insight(payload: AIInsightRequest, service: AISuiteService = Depends(get_ai_suite_service)):
    return service.generate_insight(focus=payload.focus, question=payload.question)
