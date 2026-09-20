from fastapi import APIRouter
from ..models.responses import HealthResponse
from ..core.config import get_settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health():
    s = get_settings()
    return HealthResponse(status="ok", provider=s.LLM_PROVIDER)