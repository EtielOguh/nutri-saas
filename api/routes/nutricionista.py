"""Rotas de Nutricionista."""
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

from core.database import get_db
from models.nutricionista import Nutricionista
from schemas.nutricionista import (
    ConfiguracaoNutricionistaResponse,
    ConfiguracaoNutricionistaUpdate,
    LogoUploadResponse,
    NutricionistaResponse,
    DashboardNutricionistaResponse,
)
from schemas.base import ErrorResponse
from services.nutricionista_service import NutricionistaService


router = APIRouter(
    prefix="/nutricionistas",
    tags=["nutricionistas"],
    responses={
        404: {"model": ErrorResponse, "description": "Recurso não encontrado"},
        422: {"model": ErrorResponse, "description": "Erro de validação"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
    },
)


@router.get(
    "/{nutricionista_id}",
    response_model=NutricionistaResponse,
    summary="Obter nutricionista",
    description="Obtém informações de um nutricionista específico.",
)
async def get_nutricionista(
    nutricionista_id: int,
    db: Session = Depends(get_db),
) -> NutricionistaResponse:
    """
    Obtém informações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    
    Retorna informações do nutricionista com suas configurações.
    """
    service = NutricionistaService(db=db)
    nutricionista = service.get_by_id(nutricionista_id)

    if not nutricionista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutricionista com ID {nutricionista_id} não encontrado",
        )

    return NutricionistaResponse.model_validate(nutricionista)


@router.get(
    "/{nutricionista_id}/configuracao",
    response_model=ConfiguracaoNutricionistaResponse,
    summary="Obter configurações",
    description="Obtém as configurações de um nutricionista.",
)
async def get_configuracao(
    nutricionista_id: int,
    db: Session = Depends(get_db),
) -> ConfiguracaoNutricionistaResponse:
    """
    Obtém configurações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    
    Retorna configurações como logo, cor primária, valor de consulta.
    """
    service = NutricionistaService(db=db)
    config = service.get_configuracao(nutricionista_id)

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configurações não encontradas para nutricionista {nutricionista_id}",
        )

    return ConfiguracaoNutricionistaResponse.model_validate(config)


@router.put(
    "/{nutricionista_id}/configuracao",
    response_model=ConfiguracaoNutricionistaResponse,
    summary="Atualizar configurações",
    description="Atualiza as configurações de um nutricionista.",
)
async def update_configuracao(
    nutricionista_id: int,
    config_data: ConfiguracaoNutricionistaUpdate,
    db: Session = Depends(get_db),
) -> ConfiguracaoNutricionistaResponse:
    """
    Atualiza configurações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    - **config_data**: Dados a atualizar (logo_url, cor_primaria, valor_consulta, link_agendamento)
    
    Qualquer campo não fornecido não será alterado.
    """
    service = NutricionistaService(db=db)

    try:
        config = service.update_configuracao(nutricionista_id, config_data)
        return ConfiguracaoNutricionistaResponse.model_validate(config)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/{nutricionista_id}/upload-logo",
    response_model=LogoUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload de logo",
    description="Faz upload de uma logo para o nutricionista.",
)
async def upload_logo(
    nutricionista_id: int,
    file: UploadFile = File(..., description="Arquivo de imagem (JPG, PNG, WebP, GIF)"),
    db: Session = Depends(get_db),
) -> LogoUploadResponse:
    """
    Faz upload de uma logo para um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    - **file**: Arquivo de imagem (máximo 5MB)
    
    Aceita os seguintes formatos: JPG, PNG, WebP, GIF
    
    A logo anterior será substituída automaticamente.
    """
    service = NutricionistaService(db=db)

    try:
        logo_url, logo_path, file_size = service.upload_logo(nutricionista_id, file)

        return LogoUploadResponse(
            nutricionista_id=nutricionista_id,
            logo_url=logo_url,
            logo_path=logo_path,
            file_size=file_size,
            message=f"Logo enviada com sucesso ({file_size / 1024:.2f}KB)",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar arquivo: {str(e)}",
        )


@router.delete(
    "/{nutricionista_id}/logo",
    summary="Remover logo",
    description="Remove a logo de um nutricionista.",
)
async def delete_logo(
    nutricionista_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove a logo de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    
    Retorna uma mensagem confirmando a remoção.
    """
    service = NutricionistaService(db=db)

    deleted = service.delete_logo(nutricionista_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma logo encontrada para nutricionista {nutricionista_id}",
        )

    return {
        "message": f"Logo removida com sucesso",
        "nutricionista_id": nutricionista_id,
    }


@router.get(
    "/{nutricionista_id}/dashboard",
    response_model=DashboardNutricionistaResponse,
    summary="Dashboard do nutricionista",
    description="Obtém dados agregados e métricas do dashboard para um nutricionista.",
)
async def get_dashboard(
    nutricionista_id: int,
    db: Session = Depends(get_db),
) -> DashboardNutricionistaResponse:
    """
    Obtém dados completos do dashboard para um nutricionista.
    
    Retorna:
    - **Total de clientes**: Quantidade total de clientes do nutricionista
    - **Total de medições**: Quantidade total de medições registradas
    - **Média de peso**: Média ponderada das últimas medições de cada cliente
    - **Clientes ativos**: Clientes com medições no último mês
    - **Últimos clientes**: 5 clientes com atividade mais recente
    
    Args:
        nutricionista_id: ID do nutricionista
    
    Returns:
        Objeto com métricas, clientes recentes e configurações
    """
    service = NutricionistaService(db=db)

    try:
        dashboard_data = service.get_dashboard_data(nutricionista_id)
        return DashboardNutricionistaResponse.model_validate(dashboard_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# Endpoint público para servir arquivos estáticos (logos)
@router.get(
    "/uploads/logos/{filename}",
    summary="Obter logo",
    description="Obtém uma logo armazenada.",
)
async def get_logo(filename: str):
    """
    Retorna uma logo armazenada.
    
    - **filename**: Nome do arquivo da logo
    
    Retorna a imagem com o tipo MIME apropriado.
    """
    file_path = Path("uploads") / "logos" / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logo não encontrada",
        )

    return FileResponse(
        file_path,
        media_type="image/jpeg",  # Será ajustado pela extensão do arquivo
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )
