# Arquitetura de Endpoints - Design Pattern

## 📐 Estrutura em Camadas

A arquitetura segue um padrão de camadas bem definido:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Routes                            │
│              (api/routes/cliente.py)                         │
│                                                              │
│  POST, GET, GET{id}, PATCH, DELETE com validações HTTP     │
└────────────────────────┬────────────────────────────────────┘
                         │ Import
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Service Layer                               │
│            (services/cliente_service.py)                     │
│                                                              │
│  Business logic, authorization, CRUD operations,           │
│  transaction management                                     │
└────────────────────────┬────────────────────────────────────┘
                         │ Extend BaseService
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Base Service (CRUD Generic)                   │
│              (services/base.py)                              │
│                                                              │
│  Generic methods: get_by_id, get_all, create, update,     │
│  delete, get_count - type-safe with generics              │
└────────────────────────┬────────────────────────────────────┘
                         │ Use
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORM Models                                 │
│            (models/cliente.py)                              │
│                                                              │
│  SQLAlchemy models with relationships, cascade deletes     │
└────────────────────────┬────────────────────────────────────┘
                         │ Define
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Pydantic Schemas                               │
│            (schemas/cliente.py)                             │
│                                                              │
│  Request validation, response serialization, with          │
│  ConfigDict(from_attributes=True) for ORM compatibility    │
└───────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Requisição

```
1. HTTP Request (FastAPI Route Layer)
   ├─ Validação de URL parameters (nutricionista_id, cliente_id)
   ├─ Validação de Query parameters (skip, limit)
   ├─ Validação de Request Body (Pydantic schema)
   └─ Dependency injection: get_db()
   
2. Service Layer (Business Logic)
   ├─ Verificação de autorização (get_cliente_por_nutricionista)
   ├─ Lógica de negócio (rules específicas)
   ├─ Transações com banco de dados
   └─ Transformação de dados para schemas
   
3. Database Layer (SQLAlchemy)
   ├─ Query building
   ├─ ACID transactions
   ├─ Cascade operations
   └─ Connection pooling
   
4. Response (Serialization)
   ├─ Pydantic model.from_orm(db_object)
   ├─ JSON serialization
   ├─ HTTP status code
   └─ Optional headers
```

---

## 🏗️ Componentes da Camada de Serviço

### Base Service (services/base.py)

Template genérico para CRUD:

```python
from typing import Generic, TypeVar, List
from sqlalchemy.orm import Session

T = TypeVar('T')  # Model type
SchemaT = TypeVar('SchemaT')  # Schema type

class BaseService(Generic[T, SchemaT]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    # CRUD Methods
    def get_by_id(self, id: int) -> T | None:
        """Get single by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        """Get all with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj: SchemaT) -> T:
        """Create new record"""
        db_obj = self.model(**obj.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: int, obj: SchemaT) -> T | None:
        """Update existing record"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        data = obj.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """Delete record"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def get_count(self) -> int:
        """Count records"""
        return self.db.query(self.model).count()
```

### Serviço Específico (services/cliente_service.py)

Estende BaseService com lógica de negócio:

```python
class ClienteService(BaseService[Cliente, ClienteCreate]):
    def __init__(self, db: Session):
        super().__init__(db, Cliente)
    
    # 1. Query customizada: listar por owner
    def get_by_nutricionista(
        self,
        nutricionista_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[Cliente]:
        """List all clients for a specific nutritionist"""
        return (
            self.db.query(self.model)
            .filter(self.model.nutricionista_id == nutricionista_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    # 2. Count customizado: contar por owner
    def count_by_nutricionista(self, nutricionista_id: int) -> int:
        """Count clients for a specific nutritionist"""
        return (
            self.db.query(self.model)
            .filter(self.model.nutricionista_id == nutricionista_id)
            .count()
        )
    
    # 3. Autorização: verificar ownership
    def get_cliente_por_nutricionista(
        self,
        cliente_id: int,
        nutricionista_id: int
    ) -> Cliente | None:
        """Get client if it belongs to nutritionist (authorization check)"""
        return (
            self.db.query(self.model)
            .filter(
                self.model.id == cliente_id,
                self.model.nutricionista_id == nutricionista_id
            )
            .first()
        )
    
    # 4. Create com validação
    def create_cliente(
        self,
        nutricionista_id: int,
        data: ClienteCreate
    ) -> Cliente:
        """Create client with validation"""
        # Verify nutritionist exists
        nut = self.db.query(Nutricionista).filter(
            Nutricionista.id == nutricionista_id
        ).first()
        if not nut:
            raise ValueError(f"Nutricionista {nutricionista_id} não existe")
        
        # Create client
        cliente_data = data.model_dump()
        cliente_data['nutricionista_id'] = nutricionista_id
        cliente = Cliente(**cliente_data)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
    
    # 5. Update com validação
    def update_cliente(
        self,
        cliente_id: int,
        data: ClienteUpdate
    ) -> Cliente | None:
        """Update client with validation"""
        cliente = self.get_by_id(cliente_id)
        if not cliente:
            return None
        
        # Apply partial updates
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cliente, key, value)
        
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
    
    # 6. Delete com cascade
    def delete_cliente(self, cliente_id: int) -> bool:
        """Delete client (cascade deletes related records)"""
        cliente = self.get_by_id(cliente_id)
        if not cliente:
            return False
        
        # Cascade delete is configured in Model relationships
        # with cascade="all, delete" in ForeignKey
        self.db.delete(cliente)
        self.db.commit()
        return True
```

---

## 🛣️ Camada de Routes

### Estrutura de Router

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.dependencies import get_db
from services.cliente_service import ClienteService
from schemas.cliente import (
    ClienteCreate, ClienteUpdate, ClienteResponse, ClienteDetailResponse
)

router = APIRouter(
    prefix="/nutricionistas/{nutricionista_id}/clientes",
    tags=["clientes"],
)
```

### Endpoint 1: CREATE (POST)

```python
@router.post("", status_code=201, response_model=ClienteResponse)
async def criar_cliente(
    nutricionista_id: int,
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
) -> ClienteResponse:
    """Create new client for a nutritionist"""
    
    # Validation: nutricionista_id from URL must match request body
    if cliente_data.nutricionista_id != nutricionista_id:
        raise HTTPException(
            status_code=400,
            detail="Cliente deve estar vinculado ao nutricionista"
        )
    
    try:
        service = ClienteService(db=db)
        cliente = service.create_cliente(nutricionista_id, cliente_data)
        return ClienteResponse.from_orm(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar cliente")
```

**Response Status Codes:**
- ✅ 201 Created - Sucesso
- ❌ 400 Bad Request - nutricionista_id mismatch ou não existe
- ❌ 422 Unprocessable Entity - Validação de dados falhou
- ❌ 500 Internal Server Error - Erro do servidor

### Endpoint 2: READ LIST (GET)

```python
@router.get("", response_model=List[ClienteResponse])
async def listar_clientes(
    nutricionista_id: int,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items per page"),
    db: Session = Depends(get_db),
) -> List[ClienteResponse]:
    """List all clients for a nutritionist with pagination"""
    
    try:
        service = ClienteService(db=db)
        clientes = service.get_by_nutricionista(
            nutricionista_id=nutricionista_id,
            skip=skip,
            limit=limit
        )
        return [ClienteResponse.from_orm(c) for c in clientes]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao listar clientes")
```

**Query Parameters:**
- `skip` (int, ≥0, default=0) - Offset for pagination
- `limit` (int, 1-100, default=10) - Items per page

**Response Status Codes:**
- ✅ 200 OK - Array of clients (may be empty)
- ❌ 422 Unprocessable Entity - Invalid query parameters

### Endpoint 3: READ DETAIL (GET {id})

```python
@router.get("/{cliente_id}", response_model=ClienteDetailResponse)
async def obter_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
) -> ClienteDetailResponse:
    """Get detailed info for a specific client"""
    
    try:
        service = ClienteService(db=db)
        
        # Authorization check
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado para este nutricionista"
            )
        
        return ClienteDetailResponse.from_orm(cliente)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao obter cliente")
```

**Response Status Codes:**
- ✅ 200 OK - Client details with stats
- ❌ 404 Not Found - Client doesn't exist or belongs to another nutritionist
- ❌ 500 Internal Server Error - Server error

### Endpoint 4: UPDATE (PATCH)

```python
@router.patch("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    nutricionista_id: int,
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
) -> ClienteResponse:
    """Update client (partial update with PATCH)"""
    
    try:
        service = ClienteService(db=db)
        
        # Authorization check
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado para este nutricionista"
            )
        
        # Update client
        cliente_atualizado = service.update_cliente(cliente_id, cliente_data)
        if not cliente_atualizado:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        return ClienteResponse.from_orm(cliente_atualizado)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao atualizar cliente")
```

**Request Body:**
- All fields are optional (partial update)
- Uses `exclude_unset=True` for partial updates

**Response Status Codes:**
- ✅ 200 OK - Updated client
- ❌ 404 Not Found - Client doesn't exist or authorization failed
- ❌ 422 Unprocessable Entity - Validation failed
- ❌ 500 Internal Server Error - Server error

### Endpoint 5: DELETE

```python
@router.delete("/{cliente_id}", status_code=204)
async def deletar_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete client (cascade deletes related records)"""
    
    try:
        service = ClienteService(db=db)
        
        # Authorization check
        cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado para este nutricionista"
            )
        
        # Delete client
        sucesso = service.delete_cliente(cliente_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao deletar cliente")
```

**Response Status Codes:**
- ✅ 204 No Content - Success (no response body)
- ❌ 404 Not Found - Client doesn't exist or authorization failed
- ❌ 500 Internal Server Error - Server error

---

## 🔐 Padrão de Autorização

### Implementação no Service

```python
def get_cliente_por_nutricionista(
    self,
    cliente_id: int,
    nutricionista_id: int
) -> Cliente | None:
    """Verifica se cliente pertence ao nutricionista"""
    return (
        self.db.query(self.model)
        .filter(
            self.model.id == cliente_id,
            self.model.nutricionista_id == nutricionista_id
        )
        .first()
    )
```

### Uso em Routes

```python
# Verificação antes de qualquer operação
cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
if not cliente:
    raise HTTPException(404, "Cliente não encontrado para este nutricionista")
```

### Benefícios

- ✅ Simples e legível
- ✅ Previne acesso cross-owner
- ✅ Retorna 404 (não 403) para não vazar informações
- ✅ Reutilizável em todos os endpoints
- ✅ Pronto para upgrade a JWT token validation

---

## 📦 Integração com Main App

### Registrar Router

```python
# main.py
from api.routes import cliente

app.include_router(cliente.router)
```

### Resultado

Todos os endpoints ficam disponíveis:
- `POST /nutricionistas/{nutricionista_id}/clientes`
- `GET /nutricionistas/{nutricionista_id}/clientes`
- `GET /nutricionistas/{nutricionista_id}/clientes/{cliente_id}`
- `PATCH /nutricionistas/{nutricionista_id}/clientes/{cliente_id}`
- `DELETE /nutricionistas/{nutricionista_id}/clientes/{cliente_id}`

---

## 📋 Padrão para Replicar em Outras Entidades

### 1. Criar Serviço (services/[entity]_service.py)

```python
from services.base import BaseService
from models.[entity] import [Entity]
from schemas.[entity] import [EntityCreate], [EntityUpdate]

class [Entity]Service(BaseService[[Entity], [EntityCreate]]):
    def __init__(self, db: Session):
        super().__init__(db, [Entity])
    
    # Adicione métodos customizados:
    # - get_by_owner()
    # - get_[entity]_por_owner()
    # - Validações específicas
```

### 2. Criar Routes (api/routes/[entity].py)

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from services.[entity]_service import [Entity]Service
from schemas.[entity] import [EntityCreate], [EntityUpdate], [EntityResponse]

router = APIRouter(
    prefix="/[entities]",
    tags=["[entities]"],
)

@router.post("", status_code=201, response_model=[EntityResponse])
async def criar_[entity](...):
    ...

@router.get("", response_model=List[[EntityResponse]])
async def listar_[entities](...):
    ...

# etc...
```

### 3. Integrar em main.py

```python
from api.routes import [entity]

app.include_router([entity].router)
```

---

## 🎯 Checklist de Implementação

Para adicionar um novo endpoint REST completo:

- [ ] **Service Layer**
  - [ ] Criar `services/[entity]_service.py`
  - [ ] Estender `BaseService[[Entity], [EntityCreate]]`
  - [ ] Implementar `get_by_owner()` para listagem
  - [ ] Implementar `get_[entity]_por_owner()` para autorização
  - [ ] Adicionar validações específicas

- [ ] **Routes Layer**
  - [ ] Criar `api/routes/[entity].py`
  - [ ] Implementar `@router.post()` com validação
  - [ ] Implementar `@router.get()` com paginação
  - [ ] Implementar `@router.get("/{id}")` com autorização
  - [ ] Implementar `@router.patch()` com partial updates
  - [ ] Implementar `@router.delete()` com cascade

- [ ] **Integration**
  - [ ] Importar router em `main.py`
  - [ ] Registrar com `app.include_router()`
  - [ ] Testar todos os endpoints

- [ ] **Documentation**
  - [ ] Adicionar exemplos cURL
  - [ ] Documentar validações
  - [ ] Documentar status codes
  - [ ] Documentar autorização

---

## 📚 Referências

- [fastapi.tiangolo.com - Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [sqlalchemy.org - Sessions](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [pydantic.dev - Field Validation](https://docs.pydantic.dev/latest/concepts/validators/)

---

Última atualização: 2024-01-15
