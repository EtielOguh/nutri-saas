"""Rotas públicas (sem autenticação) do sistema."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.cliente import ClientePublicResponse
from schemas.token_acesso import ClientePublicAccessResponse
from services.cliente_service import ClienteService

router = APIRouter(
    prefix="/public",
    tags=["public"],
    responses={
        404: {"description": "Recurso não encontrado"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno do servidor"},
    },
)


@router.get(
    "/cliente/{token}",
    response_model=ClientePublicAccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Acessar cliente por token público",
    description="Acesso público aos dados básicos de um cliente usando token único (sem autenticação).",
)
async def obter_cliente_por_token(
    token: str,
    db: Session = Depends(get_db),
) -> ClientePublicAccessResponse:
    """
    Obtém os dados básicos de um cliente usando seu token de acesso público.
    
    Este endpoint não requer autenticação. O acesso é controlado apenas pelo token.
    Retorna apenas dados públicos do cliente (nome, idade, altura, objetivo).
    
    **Path Parameters:**
    - **token**: Token único de acesso público (UUID ou string)
    
    **Resposta (200):**
    - id: ID do cliente
    - nome: Nome do cliente
    - idade: Idade em anos
    - altura: Altura em centímetros
    - objetivo: Objetivo de saúde
    - token_criado_em: Data de criação do token
    
    **Erros:**
    - 404: Token inválido ou cliente não encontrado
    - 422: Erro de validação
    - 500: Erro interno do servidor
    
    **Exemplo:**
    ```
    GET /public/cliente/550e8400-e29b-41d4-a716-446655440000
    
    Response:
    {
        "id": 1,
        "nome": "João Silva",
        "idade": 30,
        "altura": 180,
        "objetivo": "Ganhar massa muscular",
        "token_criado_em": "2026-04-02T10:30:00"
    }
    ```
    """
    try:
        # Validar que o token não está vazio
        if not token or len(token.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Token deve ser fornecido",
            )
        
        # Buscar cliente pelo token
        service = ClienteService(db=db)
        cliente = service.get_cliente_por_token(token.strip())
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token inválido ou cliente não encontrado",
            )
        
        # Obter informações do token para retornar data de criação
        from models.token_acesso import TokenAcessoCliente
        
        token_obj = (
            db.query(TokenAcessoCliente)
            .filter(TokenAcessoCliente.token_unico == token.strip())
            .first()
        )
        
        token_criado_em = None
        if token_obj and hasattr(token_obj, 'created_at'):
            token_criado_em = token_obj.created_at.isoformat() if token_obj.created_at else None
        
        # Montar resposta
        return ClientePublicAccessResponse(
            id=cliente.id,
            nome=cliente.nome,
            idade=cliente.idade,
            altura=cliente.altura,
            objetivo=cliente.objetivo,
            token_criado_em=token_criado_em,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar cliente: {str(e)}",
        )


@router.get(
    "/cliente/{token}/validar",
    summary="Validar token de cliente",
    description="Verifica se um token de acesso é válido.",
)
async def validar_token(
    token: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Valida um token de acesso público de um cliente.
    
    Este endpoint verifica se o token existe e está ativo.
    
    **Path Parameters:**
    - **token**: Token único de acesso público
    
    **Resposta (200):**
    ```json
    {
        "valido": true,
        "cliente_id": 1,
        "cliente_nome": "João Silva",
        "mensagem": "Token válido"
    }
    ```
    
    Se token inválido:
    ```json
    {
        "valido": false,
        "cliente_id": null,
        "cliente_nome": null,
        "mensagem": "Token inválido ou expirado"
    }
    ```
    """
    try:
        if not token or len(token.strip()) == 0:
            return {
                "valido": False,
                "cliente_id": None,
                "cliente_nome": None,
                "mensagem": "Token deve ser fornecido",
            }
        
        # Buscar cliente pelo token
        service = ClienteService(db=db)
        cliente = service.get_cliente_por_token(token.strip())
        
        if not cliente:
            return {
                "valido": False,
                "cliente_id": None,
                "cliente_nome": None,
                "mensagem": "Token inválido ou expirado",
            }
        
        return {
            "valido": True,
            "cliente_id": cliente.id,
            "cliente_nome": cliente.nome,
            "mensagem": "Token válido",
        }
    
    except Exception as e:
        return {
            "valido": False,
            "cliente_id": None,
            "cliente_nome": None,
            "mensagem": f"Erro ao validar token: {str(e)}",
        }
