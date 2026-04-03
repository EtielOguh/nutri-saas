# Schemas - Validação de Dados com Pydantic

Este documento descreve os schemas Pydantic do Nutri SaaS, utilizados para validar dados de entrada e serializar respostas da API.

## Estrutura de Schemas

Cada entidade segue um padrão consistente com 3-5 variações de schema:

### 1. **Base Schema**
Define todos os campos da entidade com suas validações. Usada como base para outras schemas.

```python
class ClienteBase(BaseSchema):
    nutricionista_id: int = Field(..., gt=0)
    nome: str = Field(..., min_length=3, max_length=255)
    idade: Optional[int] = Field(None, ge=1, le=150)
    altura: Optional[float] = Field(None, gt=0, le=300)
    objetivo: Optional[str] = Field(None, max_length=255)
```

### 2. **Create Schema**
Usada para criar novas entidades (POST). Herda da Base schema com campos obrigatórios.

```python
class ClienteCreate(ClienteBase):
    """Todos os campos herdados de ClienteBase"""
    pass
```

### 3. **Update Schema**
Usada para atualizar entidades (PATCH/PUT). Todos os campos são opcionais.

```python
class ClienteUpdate(BaseSchema):
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    idade: Optional[int] = Field(None, ge=1, le=150)
    altura: Optional[float] = Field(None, gt=0, le=300)
    objetivo: Optional[str] = Field(None, max_length=255)
```

### 4. **Response Schema**
Usada na resposta (GET). Inclui timestamps e pode conter relacionamentos.

```python
class ClienteResponse(TimestampSchema, ClienteBase):
    nutricionista: Optional[NutricionistaSimpleResponse]
```

### 5. **Simple Response Schema**
Versão simplificada para uso em relacionamentos (evita referências circulares).

```python
class ClienteSimpleResponse(BaseSchema):
    id: int
    nome: str
    idade: Optional[int]
    altura: Optional[float]
```

## Entidades e Schemas

### 1. Nutricionista

**Campos principais:**
- `nome`: String 3-255 caracteres
- `email`: Email válido (EmailStr)
- `senha`: String mínimo 8 caracteres (apenas em Create)

**Schemas disponíveis:**
- `NutricionistaCreate` - Criar nutricionista
- `NutricionistaUpdate` - Atualizar nutricionista
- `NutricionistaResponse` - Resposta com dados completos
- `NutricionistaDetailResponse` - Resposta com total de clientes
- `NutricionistaSimpleResponse` - Resposta simplificada

**Exemplo:**
```python
from schemas import NutricionistaCreate, NutricionistaResponse

# Criar
nutricionista_data = NutricionistaCreate(
    nome="Dr. João Silva",
    email="joao@example.com",
    senha="senhaSegura123"
)

# Resposta (com timestamps)
response_data = {
    "id": 1,
    "nome": "Dr. João Silva",
    "email": "joao@example.com",
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}
nutricionista = NutricionistaResponse(**response_data)
```

### 2. ConfiguraçãoNutricionista

**Campos principais:**
- `logo_url`: URL opcional
- `cor_primaria`: Cor em hex format (^#[0-9A-Fa-f]{6}$)
- `valor_consulta`: Float positivo

**Schemas disponíveis:**
- `ConfiguracaoNutricionistaCreate`
- `ConfiguracaoNutricionistaUpdate`
- `ConfiguracaoNutricionistaResponse`

### 3. Cliente

**Campos principais:**
- `nutricionista_id`: ID obrigatório
- `nome`: String 3-255 caracteres
- `idade`: Inteiro 1-150 (opcional)
- `altura`: Float 0-300 cm (opcional)
- `objetivo`: String até 255 caracteres (opcional)

**Schemas disponíveis:**
- `ClienteCreate` - Criar cliente
- `ClienteUpdate` - Atualizar cliente
- `ClienteResponse` - Resposta com nutricionista
- `ClienteDetailResponse` - Resposta com estatísticas
- `ClienteSimpleResponse` - Resposta simplificada

**Validações:**
```
- Idade: 1 <= idade <= 150
- Altura: 0 < altura <= 300 cm
- Nome: 3 <= len <= 255
```

### 4. Medição

**Campos principais:**
- `cliente_id`: ID obrigatório
- `peso`: Float 0 < peso <= 1000 kg
- `data_medicao`: DateTime (opcional, padrão = agora)

**Schemas disponíveis:**
- `MedicaoCreate` - Criar medição
- `MedicaoUpdate` - Atualizar medição
- `MedicaoResponse` - Resposta com cliente
- `MedicaoSimpleResponse` - Resposta simplificada
- `MedicaoHistoricoResponse` - Histórico com lista de medições

**Exemplo:**
```python
from schemas import MedicaoCreate, MedicaoHistoricoResponse

# Criar
medicao = MedicaoCreate(
    cliente_id=1,
    peso=75.5
)

# Histórico
historico = MedicaoHistoricoResponse(
    total=10,
    medicoes=[...],  # List[MedicaoResponse]
    variacao_total=-2.5
)
```

### 5. Observação

**Campos principais:**
- `cliente_id`: ID obrigatório
- `texto`: String 1-5000 caracteres

**Schemas disponíveis:**
- `ObservacaoCreate`
- `ObservacaoUpdate`
- `ObservacaoResponse`
- `ObservacaoSimpleResponse`

### 6. Token de Acesso

**Campos principais:**
- `cliente_id`: ID obrigatório
- `token_unico`: String 20-255 caracteres

**Schemas disponíveis:**
- `TokenAcessoClienteCreate` - Criar token (gerado automaticamente)
- `TokenAcessoClienteUpdate` - Atualizar (vazio)
- `TokenAcessoClienteResponse` - Resposta com cliente
- `TokenAcessoClienteGenerateResponse` - Resposta ao gerar
- `TokenValidacaoResponse` - Validação de token

**Exemplo:**
```python
from schemas import TokenValidacaoResponse

validacao = TokenValidacaoResponse(
    valido=True,
    cliente_id=1,
    cliente_nome="João Cliente"
)
```

### 7. Documento PDF

**Campos principais:**
- `cliente_id`: ID obrigatório
- `url_pdf`: String até 512 caracteres

**Schemas disponíveis:**
- `DocumentoPDFCreate`
- `DocumentoPDFUpdate`
- `DocumentoPDFResponse`
- `DocumentoPDFSimpleResponse`
- `DocumentoPDFBulkResponse` - Resposta de upload em lote

**Exemplo:**
```python
from schemas import DocumentoPDFBulkResponse

bulk = DocumentoPDFBulkResponse(
    total=2,
    sucesso=2,
    erro=0
)
```

## Schemas Base

### BaseSchema
Classe base com configurações padrão Pydantic v2:
- `from_attributes=True` - Compatível com SQLAlchemy
- `populate_by_name=True` - Aliases e field names
- Comportamento de dados extras: ignorar

### TimestampSchema
Estende BaseSchema com campos de timestamp:
- `id`: Inteiro
- `created_at`: DateTime
- `updated_at`: DateTime

### Schemas de Resposta Comum

**PaginatedResponse**
```python
class PaginatedResponse(BaseSchema, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]
```

**ErrorResponse**
```python
class ErrorResponse(BaseSchema):
    error: str
    detail: Optional[str]
    status_code: int
```

## Validações Implementadas

### EmailStr
```python
email: EmailStr  # Valida formato de email
```

### Field Constraints
```python
# Numéricos
Field(..., ge=1, le=150)      # Min/max inclusive
Field(..., gt=0)               # Strict greater than
Field(..., le=1000)            # Less than or equal

# Strings
Field(..., min_length=3, max_length=255)
Field(..., pattern="^#[0-9A-Fa-f]{6}$")  # Regex

# Obrigatório vs Opcional
Field(...)              # Obrigatório
Field(None)            # Opcional
Optional[str]          # Tipo opcional
```

## Integração com FastAPI

### Exemplo de Rota com Schemas

```python
from fastapi import APIRouter, Depends
from schemas import ClienteCreate, ClienteResponse, ClienteUpdate
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/clientes", response_model=ClienteResponse)
def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """Criar novo cliente"""
    # Validação automática com ClienteCreate
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    return ClienteResponse.from_orm(db_cliente)

@router.patch("/clientes/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar cliente"""
    # Apenas campos fornecidos
    db_cliente = db.query(models.Cliente).filter_by(id=cliente_id).first()
    update_data = cliente.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    db.commit()
    return ClienteResponse.from_orm(db_cliente)

@router.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obter cliente"""
    cliente = db.query(models.Cliente).filter_by(id=cliente_id).first()
    return ClienteResponse.from_orm(cliente)
```

### Conversão de Modelos SQLAlchemy

```python
# De ORM para Schema
from_orm() ou from_attributes=True

# Exemplo
response = ClienteResponse.from_orm(db_cliente)

# Ou com exclude
response = ClienteResponse.from_orm(db_cliente, exclude={"nutricionista"})
```

## Serialização JSON

Todos os schemas suportam JSON serialization:

```python
# Para JSON
json_str = cliente.model_dump_json()

# Para dict Python
dict_data = cliente.model_dump()

# Com exclusões
dict_data = cliente.model_dump(exclude={"id"})
```

## Testes

Executar testes das schemas:

```bash
pytest test_schemas.py -v

# Resultado esperado:
# ✅ 27 passed in 0.13s
```

## Conventions e Boas Práticas

1. **Nomes de campos**: Use snake_case
2. **Obrigatório vs Opcional**: Sempre especificar com Field(...) ou None
3. **Validações**: Use Field constraints, não lógica em validators quando possível
4. **Nomenclatura de schemas**:
   - Create: Dados de entrada para POST
   - Update: Dados de entrada para PATCH (todos opcionais)
   - Response: Dados de saída com timestamps
   - Simple: Versão reduzida para relacionamentos
5. **Relacionamentos**: Use Optional[SimpleResponse] para evitar ciclos
6. **Type hints**: Sempre incluir type hints completos

## Próximos Passos

1. ✅ Schemas validadas e testadas (27/27 tests passing)
2. 🔄 Implementar service layer (repository pattern)
3. 🔄 Criar FastAPI routes com schemas
4. 🔄 Adicionar autenticação e autorização
5. 🔄 Integrar com documentação automática (Swagger)

---

**Versão:** 1.0  
**Data:** Janeiro 2024  
**Status:** Pronto para produção
