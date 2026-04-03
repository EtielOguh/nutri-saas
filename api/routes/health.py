"""Rota de verificação de saúde da API."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health Check")
async def health_check():
    """Verifica se a API está ativa."""
    return {"status": "ok", "message": "API is running"}
