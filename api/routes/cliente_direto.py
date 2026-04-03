"""Rotas diretas de Cliente (sem prefix de nutricionista) - usadas pelo frontend."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user
from models.nutricionista import Nutricionista
from schemas.cliente import ClienteResponse, ClienteUpdate, ClienteDetailResponse
from services.cliente_service import ClienteService

# Router para endpoints diretos /clientes/{id}
router_cliente_direto = APIRouter(prefix="/clientes", tags=["clientes"])


@router_cliente_direto.get(
    "/{cliente_id}",
    response_model=ClienteDetailResponse,
    summary="Obter detalhe do cliente",
    description="Obtém informações completas de um cliente pelo ID.",
)
async def get_cliente_direto(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> ClienteDetailResponse:
    """
    Obtém detalhes de um cliente pelo ID direto.
    
    Verifica se o cliente pertence ao nutricionista autenticado.
    Requer autenticação via Bearer token.
    """
    try:
        service = ClienteService(db=db)
        
        # Obter cliente
        cliente = service.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado",
            )
        
        # Verificar que pertence ao usuário autenticado
        if cliente.nutricionista_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este cliente",
            )
        
        # Preparar resposta com estatísticas
        detail_dict = {
            "total_medicoes": len(cliente.medicoes) if cliente.medicoes else 0,
            "total_observacoes": len(cliente.observacoes) if cliente.observacoes else 0,
            "total_documentos": len(cliente.documentos) if cliente.documentos else 0,
        }
        
        # Adicionar última medição se existir
        if cliente.medicoes:
            ultima_medicao = max(cliente.medicoes, key=lambda m: m.data_medicao or m.created_at)
            detail_dict["ultimo_peso"] = ultima_medicao.peso
            detail_dict["data_ultima_medicao"] = ultima_medicao.data_medicao or ultima_medicao.created_at
        
        response_dict = {**ClienteResponse.from_orm(cliente).model_dump(), **detail_dict}
        return ClienteDetailResponse(**response_dict)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter cliente: {str(e)}",
        )


@router_cliente_direto.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Atualizar cliente",
    description="Atualiza informações de um cliente.",
)
async def update_cliente_direto(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> ClienteResponse:
    """
    Atualiza um cliente pelo ID direto.
    
    Verifica se o cliente pertence ao nutricionista autenticado.
    Requer autenticação via Bearer token.
    """
    try:
        service = ClienteService(db=db)
        
        # Obter cliente
        cliente = service.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado",
            )
        
        # Verificar que pertence ao usuário autenticado
        if cliente.nutricionista_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para atualizar este cliente",
            )
        
        cliente_atualizado = service.update_cliente(cliente_id, cliente_data)
        if not cliente_atualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Falha ao atualizar cliente {cliente_id}",
            )
        
        return ClienteResponse.from_orm(cliente_atualizado)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar cliente: {str(e)}",
        )


@router_cliente_direto.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cliente",
    description="Deleta um cliente.",
)
async def delete_cliente_direto(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> None:
    """
    Deleta um cliente pelo ID direto.
    
    Verifica se o cliente pertence ao nutricionista autenticado.
    Requer autenticação via Bearer token.
    """
    # Verificar que o cliente pertence ao usuário autenticado
    try:
        service = ClienteService(db=db)
        
        cliente = service.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado",
            )
        
        if cliente.nutricionista_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar este cliente",
            )
        
        sucesso = service.delete_cliente(cliente_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Falha ao deletar cliente {cliente_id}",
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar cliente: {str(e)}",
        )
