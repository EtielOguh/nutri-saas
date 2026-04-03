"""Rotas de Nutricionista."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

from core.database import get_db
from core.dependencies import get_current_user
from models.nutricionista import Nutricionista, ConfiguracaoNutricionista
from models.nutricionista import Nutricionista as NutricionistaModel
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
    current_user: Nutricionista = Depends(get_current_user),
) -> NutricionistaResponse:
    """
    Obtém informações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    
    Retorna informações do nutricionista com suas configurações.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando acessar seus próprios dados
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar dados de outro nutricionista",
        )
    
    service = NutricionistaService(db=db)
    nutricionista = service.get_by_id(nutricionista_id)

    if not nutricionista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutricionista com ID {nutricionista_id} não encontrado",
        )

    return NutricionistaResponse.model_validate(nutricionista)


@router.put(
    "/{nutricionista_id}",
    response_model=NutricionistaResponse,
    summary="Atualizar nutricionista",
    description="Atualiza informações de um nutricionista (nome, CRN).",
)
async def update_nutricionista(
    nutricionista_id: int,
    nutricionista_data: dict,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> NutricionistaResponse:
    """
    Atualiza informações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    - **Body**: JSON com nome ou crn (campos opcionais)
    
    Exemplo:
    ```json
    {
      "nome": "Dr. João Silva",
      "crn": "123456/SP"
    }
    ```
    
    Requer autenticação via Bearer token.
    """
    # Verifica permissão
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar dados de outro nutricionista",
        )
    
    service = NutricionistaService(db=db)
    nutricionista = service.get_by_id(nutricionista_id)

    if not nutricionista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutricionista com ID {nutricionista_id} não encontrado",
        )

    # Atualizar campos fornecidos
    if "nome" in nutricionista_data and nutricionista_data["nome"]:
        nutricionista.nome = nutricionista_data["nome"]
    
    if "crn" in nutricionista_data:
        nutricionista.crn = nutricionista_data["crn"]
    
    db.commit()
    db.refresh(nutricionista)

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
    current_user: Nutricionista = Depends(get_current_user),
) -> ConfiguracaoNutricionistaResponse:
    """
    Obtém configurações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    
    Retorna configurações como logo, cor primária, valor de consulta.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando acessar seus próprios dados
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar configurações de outro nutricionista",
        )
    
    service = NutricionistaService(db=db)
    config = service.get_configuracao(nutricionista_id)

    # Se não existir configuração, retorna uma com valores padrão (sem persistir)
    if not config:
        # Verifica que nutricionista existe
        nutricionista = service.get_by_id(nutricionista_id)
        if not nutricionista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nutricionista {nutricionista_id} não encontrado",
            )
        
        # Retorna configuração padrão sem salvar no banco
        config_data = {
            "id": nutricionista_id,
            "nutricionista_id": nutricionista_id,
            "logo_url": None,
            "valor_consulta": None,
            "link_agendamento": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        return ConfiguracaoNutricionistaResponse(**config_data)

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
    current_user: Nutricionista = Depends(get_current_user),
) -> ConfiguracaoNutricionistaResponse:
    """
    Atualiza configurações de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    - **config_data**: Dados a atualizar (logo_url, cor_primaria, valor_consulta, link_agendamento)
    
    Qualquer campo não fornecido não será alterado.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando atualizar suas próprias configurações
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar configurações de outro nutricionista",
        )
    
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
    current_user: Nutricionista = Depends(get_current_user),
) -> LogoUploadResponse:
    """
    Faz upload de uma logo para um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    - **file**: Arquivo de imagem (máximo 5MB)
    
    Aceita os seguintes formatos: JPG, PNG, WebP, GIF
    
    A logo anterior será substituída automaticamente.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando fazer upload para sua própria logo
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para fazer upload de logo de outro nutricionista",
        )
    
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
    current_user: Nutricionista = Depends(get_current_user),
):
    """
    Remove a logo de um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista
    
    Retorna uma mensagem confirmando a remoção.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando deletar logo de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar logo de outro nutricionista",
        )
    
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
    current_user: Nutricionista = Depends(get_current_user),
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
    
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando acessar dashboard de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar dashboard de outro nutricionista",
        )
    
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
