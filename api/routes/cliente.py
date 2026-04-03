"""Rotas FastAPI para gerenciamento de Clientes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import uuid

from core.database import get_db
from core.dependencies import get_current_user
from models.cliente import Cliente
from models.nutricionista import Nutricionista
from models.token_acesso import TokenAcessoCliente
from schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate, ClienteDetailResponse
from schemas.token_acesso import TokenAcessoClienteGenerateResponse
from schemas.base import PaginatedResponse, ErrorResponse
from services.cliente_service import ClienteService

router = APIRouter(
    prefix="/nutricionistas/{nutricionista_id}/clientes",
    tags=["clientes"],
    responses={
        404: {"model": ErrorResponse, "description": "Recurso não encontrado"},
        422: {"model": ErrorResponse, "description": "Erro de validação"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
    },
)


@router.post(
    "",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    description="Cria um novo cliente vinculado a um nutricionista.",
)
async def criar_cliente(
    nutricionista_id: int,
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> ClienteResponse:
    """
    Cria um novo cliente para um nutricionista.
    
    - **nutricionista_id**: ID do nutricionista proprietário
    - **cliente_data**: Dados do cliente (nome, idade, altura, objetivo)
    
    Retorna o cliente criado com ID e timestamps.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando criar cliente para outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para criar clientes para outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        
        # Validar que o cliente está vinculado ao nutricionista correto
        if cliente_data.nutricionista_id != nutricionista_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cliente deve estar vinculado ao nutricionista da URL",
            )
        
        cliente = service.create_cliente(nutricionista_id, cliente_data)
        return ClienteResponse.from_orm(cliente)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar cliente: {str(e)}",
        )


@router.get(
    "",
    response_model=List[ClienteResponse],
    summary="Listar clientes do nutricionista",
    description="Lista todos os clientes vinculados a um nutricionista com paginação.",
)
async def listar_clientes(
    nutricionista_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> List[ClienteResponse]:
    """
    Lista todos os clientes de um nutricionista.
    
    Query parameters:
    - **skip**: Número de registros a pular (padrão: 0)
    - **limit**: Número máximo de registros a retornar (padrão: 10, máximo: 100)
    
    Retorna lista de clientes com paginação.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando listar clientes de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para listar clientes de outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        clientes = service.get_by_nutricionista(nutricionista_id, skip=skip, limit=limit)
        return [ClienteResponse.from_orm(c) for c in clientes]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar clientes: {str(e)}",
        )


@router.get(
    "/{cliente_id}",
    response_model=ClienteDetailResponse,
    summary="Obter detalhes do cliente",
    description="Retorna informações detalhadas de um cliente específico.",
)
async def obter_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> ClienteDetailResponse:
    """
    Obtém detalhes completos de um cliente.
    
    - **nutricionista_id**: ID do nutricionista proprietário
    - **cliente_id**: ID do cliente
    
    Retorna cliente com estatísticas (total de medições, observações, etc).
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando acessar clientes de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar clientes de outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        
        # Verificar que o cliente pertence ao nutricionista
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado para este nutricionista",
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


@router.patch(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Atualizar cliente",
    description="Atualiza informações de um cliente existente.",
)
async def atualizar_cliente(
    nutricionista_id: int,
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> ClienteResponse:
    """
    Atualiza um cliente existente.
    
    - **nutricionista_id**: ID do nutricionista proprietário
    - **cliente_id**: ID do cliente a atualizar
    - **cliente_data**: Dados a atualizar (todos opcionais)
    
    Apenas campos fornecidos serão atualizados.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando alterar clientes de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para alterar clientes de outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        
        # Verificar que o cliente pertence ao nutricionista
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado para este nutricionista",
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


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cliente",
    description="Deleta um cliente e todos os seus dados associados.",
)
async def deletar_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> None:
    """
    Deleta um cliente.
    
    - **nutricionista_id**: ID do nutricionista proprietário
    - **cliente_id**: ID do cliente a deletar
    
    Retorna 204 No Content se sucesso.
    Retorna 404 se cliente não encontrado.
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando deletar clientes de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar clientes de outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        
        # Verificar que o cliente pertence ao nutricionista
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado para este nutricionista",
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


@router.post(
    "/{cliente_id}/gerar-token-acesso",
    response_model=TokenAcessoClienteGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Gerar token de acesso público",
    description="Gera um novo token único para acesso público do cliente (sem autenticação).",
)
async def gerar_token_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> TokenAcessoClienteGenerateResponse:
    """
    Gera um novo token de acesso público para um cliente.
    
    O token gerado permite que o cliente acesse seus dados via endpoint público
    sem necessidade de autenticação tradicional.
    
    - **nutricionista_id**: ID do nutricionista proprietário
    - **cliente_id**: ID do cliente
    
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando gerar token para clientes de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para gerar tokens para clientes de outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        
        # Verificar que o cliente pertence ao nutricionista
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado para este nutricionista",
            )
        
        # Gerar novo token (UUID v4)
        novo_token = str(uuid.uuid4())
        
        # Verificar se já existe token para este cliente
        token_existente = db.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.cliente_id == cliente_id
        ).first()
        
        if token_existente:
            # Atualizar token existente
            token_existente.token_unico = novo_token
            db.add(token_existente)
        else:
            # Criar novo registro de token
            novo_token_obj = TokenAcessoCliente(
                cliente_id=cliente_id,
                token_unico=novo_token,
            )
            db.add(novo_token_obj)
        
        db.commit()
        
        return TokenAcessoClienteGenerateResponse(
            token_unico=novo_token,
            cliente_id=cliente_id,
            mensagem="Token gerado com sucesso"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar token: {str(e)}",
        )


@router.get(
    "/{cliente_id}/token-acesso",
    response_model=TokenAcessoClienteGenerateResponse,
    summary="Obter token de acesso público",
    description="Retorna o token de acesso público de um cliente (se existir).",
)
async def obter_token_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Nutricionista = Depends(get_current_user),
) -> TokenAcessoClienteGenerateResponse:
    """
    Obtém o token de acesso público de um cliente.
    
    Requer autenticação via Bearer token.
    """
    # Verifica se o usuário está tentando acessar token de clientes de outro nutricionista
    if current_user.id != nutricionista_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar tokens de clientes de outro nutricionista",
        )
    
    try:
        service = ClienteService(db=db)
        
        # Verificar que o cliente pertence ao nutricionista
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não encontrado para este nutricionista",
            )
        
        # Buscar token do cliente
        token_obj = db.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.cliente_id == cliente_id
        ).first()
        
        if not token_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} não possui um token de acesso gerado",
            )
        
        return TokenAcessoClienteGenerateResponse(
            token_unico=token_obj.token_unico,
            cliente_id=cliente_id,
            mensagem="Token recuperado com sucesso"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter token: {str(e)}",
        )
