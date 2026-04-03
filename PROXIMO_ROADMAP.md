# Próximos Passos - Roteiro de Implementação

## 📋 Mapa de Entidades Pendentes

```
Sistema de Nutricionistas Saas
│
├─ ✅ CONCLUÍDO: Cliente (CRUD completo)
│
├─ ⏳ PENDENTE: Nutricionista (gerenciamento de contas)
│  ├─ CRUD: criar, listar, obter, atualizar, deletar
│  ├─ Permissões: Verificar que admin/doctor só vê seus dados
│  └─ Relacionamentos: 1→N com Cliente
│
├─ ⏳ PENDENTE: Medicao (registro de medidas)
│  ├─ CRUD: criar, listar, obter, atualizar, deletar
│  ├─ Relacionamentos: N→1 com Cliente
│  ├─ Specs: peso, altura, circunferência, IMC
│  └─ Filtros: por cliente, por data range
│
├─ ⏳ PENDENTE: Observacao (anotações)
│  ├─ CRUD: criar, listar, obter, deletar (update?)
│  ├─ Relacionamentos: N→1 com Cliente
│  ├─ Specs: texto livre, data, tipo
│  └─ Filtros: por cliente, por data
│
├─ ⏳ PENDENTE: TokenAcesso (compartilhamento de acesso)
│  ├─ CRUD: criar, listar, obter, deletar
│  ├─ Relacionamentos: N→1 com Cliente
│  ├─ Specs: permissões, data expiração
│  └─ Validação: revogar automático pós-expiração
│
└─ ⏳ PENDENTE: Documento (arquivos)
   ├─ CRUD: criar (upload), listar, obter, deletar
   ├─ Relacionamentos: N→1 com Cliente
   ├─ Specs: tipo, url/path, data upload
   └─ Validação: tamanho máximo, formatos permitidos
```

---

## 🚀 Priority Stack

### Fase 1: Core Nutritionist Management
1. **Nutricionista Service** - Gerenciar contas de nutricionistas
2. **Nutricionista Routes** - CRUD endpoints
3. **Auth Middleware** - Proteger rotas com JWT

### Fase 2: Primary Data Recording
4. **Medicao Service/Routes** - Registrar medições de clientes
5. **Observacao Service/Routes** - Anotações de progresso

### Fase 3: Access Control & Files
6. **TokenAcesso Service/Routes** - Compartilhamento de acesso
7. **Documento Service/Routes** - Upload de documentos

---

## 🎯 Fase 1.1: Nutricionista Service

### Criar: `services/nutricionista_service.py`

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.nutricionista import Nutricionista
from schemas.nutricionista import NutricionistaCreate, NutricionistaUpdate, NutricionistaResponse
from services.base import BaseService


class NutricionistaService(BaseService[Nutricionista, NutricionistaCreate]):
    """Service for managing nutritionists"""
    
    def __init__(self, db: Session):
        super().__init__(db, Nutricionista)
    
    def get_by_email(self, email: str) -> Optional[Nutricionista]:
        """Get nutritionist by email (for auth/duplicate check)"""
        return (
            self.db.query(self.model)
            .filter(self.model.email == email.lower())
            .first()
        )
    
    def create_nutricionista(self, data: NutricionistaCreate) -> Nutricionista:
        """Create new nutritionist with validations"""
        # Check if email already exists
        if self.get_by_email(data.email):
            raise ValueError(f"Email {data.email} já está registrado")
        
        # Create nutritionist
        nut_data = data.model_dump()
        nut_data['email'] = nut_data['email'].lower()
        
        nutricionista = Nutricionista(**nut_data)
        self.db.add(nutricionista)
        self.db.commit()
        self.db.refresh(nutricionista)
        
        return nutricionista
    
    def update_nutricionista(
        self,
        nutricionista_id: int,
        data: NutricionistaUpdate
    ) -> Optional[Nutricionista]:
        """Update nutritionist with validations"""
        nutricionista = self.get_by_id(nutricionista_id)
        if not nutricionista:
            return None
        
        # Check email uniqueness if changed
        if data.email and data.email != nutricionista.email:
            if self.get_by_email(data.email):
                raise ValueError(f"Email {data.email} já está registrado")
        
        # Apply updates
        update_data = data.model_dump(exclude_unset=True)
        if 'email' in update_data:
            update_data['email'] = update_data['email'].lower()
        
        for key, value in update_data.items():
            setattr(nutricionista, key, value)
        
        self.db.commit()
        self.db.refresh(nutricionista)
        return nutricionista
    
    def get_nutrients_count(self, nutricionista_id: int) -> int:
        """Count total clients for a nutritionist"""
        nutricionista = self.get_by_id(nutricionista_id)
        if not nutricionista:
            return 0
        return len(nutricionista.clientes)
```

### Criar: `api/routes/nutricionista.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from services.nutricionista_service import NutricionistaService
from schemas.nutricionista import (
    NutricionistaCreate,
    NutricionistaUpdate,
    NutricionistaResponse,
)

router = APIRouter(
    prefix="/nutricionistas",
    tags=["nutricionistas"],
)


@router.post("", status_code=201, response_model=NutricionistaResponse)
async def criar_nutricionista(
    nutri_data: NutricionistaCreate,
    db: Session = Depends(get_db),
) -> NutricionistaResponse:
    """Create new nutritionist account"""
    try:
        service = NutricionistaService(db=db)
        nutricionista = service.create_nutricionista(nutri_data)
        return NutricionistaResponse.from_orm(nutricionista)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar nutricionista")


@router.get("", response_model=List[NutricionistaResponse])
async def listar_nutricionistas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[NutricionistaResponse]:
    """List all nutritionists (admin only)"""
    try:
        service = NutricionistaService(db=db)
        nutricionistas = service.get_all(skip=skip, limit=limit)
        return [NutricionistaResponse.from_orm(n) for n in nutricionistas]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao listar nutricionistas")


@router.get("/{nutricionista_id}", response_model=NutricionistaResponse)
async def obter_nutricionista(
    nutricionista_id: int,
    db: Session = Depends(get_db),
) -> NutricionistaResponse:
    """Get nutritionist details"""
    try:
        service = NutricionistaService(db=db)
        nutricionista = service.get_by_id(nutricionista_id)
        if not nutricionista:
            raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
        return NutricionistaResponse.from_orm(nutricionista)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao obter nutricionista")


@router.patch("/{nutricionista_id}", response_model=NutricionistaResponse)
async def atualizar_nutricionista(
    nutricionista_id: int,
    nutri_data: NutricionistaUpdate,
    db: Session = Depends(get_db),
) -> NutricionistaResponse:
    """Update nutritionist (partial)"""
    try:
        service = NutricionistaService(db=db)
        nutricionista = service.update_nutricionista(nutricionista_id, nutri_data)
        if not nutricionista:
            raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
        return NutricionistaResponse.from_orm(nutricionista)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao atualizar nutricionista")


@router.delete("/{nutricionista_id}", status_code=204)
async def deletar_nutricionista(
    nutricionista_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete nutritionist (cascade: removes all clients and data)"""
    try:
        service = NutricionistaService(db=db)
        sucesso = service.delete(nutricionista_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao deletar nutricionista")
```

---

## 🚀 Fase 1.2: Integrar em main.py

```python
# Adicionar em main.py

from api.routes import health, cliente, nutricionista

# Registrar routers
app.include_router(health.router)
app.include_router(nutricionista.router)  # ✅ NOVO
app.include_router(cliente.router)
```

---

## 📊 Fase 2.1: Medicao Service

### Criar: `services/medicao_service.py`

```python
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models.medicao import Medicao
from models.cliente import Cliente
from schemas.medicao import MedicaoCreate, MedicaoUpdate, MedicaoResponse
from services.base import BaseService


class MedicaoService(BaseService[Medicao, MedicaoCreate]):
    """Service for managing client measurements"""
    
    def __init__(self, db: Session):
        super().__init__(db, Medicao)
    
    def get_by_cliente(
        self,
        cliente_id: int,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Medicao]:
        """Get all measurements for a client"""
        return (
            self.db.query(self.model)
            .filter(self.model.cliente_id == cliente_id)
            .order_by(self.model.data_medicao.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_medicao_por_cliente(
        self,
        medicao_id: int,
        cliente_id: int
    ) -> Optional[Medicao]:
        """Get measurement if it belongs to client (authorization)"""
        return (
            self.db.query(self.model)
            .filter(
                self.model.id == medicao_id,
                self.model.cliente_id == cliente_id
            )
            .first()
        )
    
    def get_ultima_medicao(self, cliente_id: int) -> Optional[Medicao]:
        """Get the most recent measurement for a client"""
        return (
            self.db.query(self.model)
            .filter(self.model.cliente_id == cliente_id)
            .order_by(self.model.data_medicao.desc())
            .first()
        )
    
    def get_medicoes_range(
        self,
        cliente_id: int,
        data_inicio: datetime,
        data_fim: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Medicao]:
        """Get measurements within a date range"""
        return (
            self.db.query(self.model)
            .filter(
                self.model.cliente_id == cliente_id,
                self.model.data_medicao >= data_inicio,
                self.model.data_medicao <= data_fim,
            )
            .order_by(self.model.data_medicao.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_medicao(
        self,
        cliente_id: int,
        data: MedicaoCreate,
    ) -> Medicao:
        """Create new measurement with validation"""
        # Verify client exists
        cliente = self.db.query(Cliente).filter(
            Cliente.id == cliente_id
        ).first()
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} não existe")
        
        # Create measurement
        medicao_data = data.model_dump()
        medicao_data['cliente_id'] = cliente_id
        medicao = Medicao(**medicao_data)
        
        self.db.add(medicao)
        self.db.commit()
        self.db.refresh(medicao)
        return medicao
```

### Criar: `api/routes/medicao.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from core.dependencies import get_db
from services.medicao_service import MedicaoService
from schemas.medicao import MedicaoCreate, MedicaoUpdate, MedicaoResponse

router = APIRouter(
    prefix="/clientes/{cliente_id}/medicoes",
    tags=["medicoes"],
)


@router.post("", status_code=201, response_model=MedicaoResponse)
async def criar_medicao(
    cliente_id: int,
    medicao_data: MedicaoCreate,
    db: Session = Depends(get_db),
) -> MedicaoResponse:
    """Record new measurement for client"""
    try:
        service = MedicaoService(db=db)
        medicao = service.create_medicao(cliente_id, medicao_data)
        return MedicaoResponse.from_orm(medicao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao criar medição")


@router.get("", response_model=List[MedicaoResponse])
async def listar_medicoes(
    cliente_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[MedicaoResponse]:
    """List all measurements for a client"""
    try:
        service = MedicaoService(db=db)
        medicoes = service.get_by_cliente(cliente_id, skip=skip, limit=limit)
        return [MedicaoResponse.from_orm(m) for m in medicoes]
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao listar medições")


@router.get("/{medicao_id}", response_model=MedicaoResponse)
async def obter_medicao(
    cliente_id: int,
    medicao_id: int,
    db: Session = Depends(get_db),
) -> MedicaoResponse:
    """Get specific measurement details"""
    try:
        service = MedicaoService(db=db)
        medicao = service.get_medicao_por_cliente(medicao_id, cliente_id)
        if not medicao:
            raise HTTPException(status_code=404, detail="Medição não encontrada")
        return MedicaoResponse.from_orm(medicao)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao obter medição")


@router.patch("/{medicao_id}", response_model=MedicaoResponse)
async def atualizar_medicao(
    cliente_id: int,
    medicao_id: int,
    medicao_data: MedicaoUpdate,
    db: Session = Depends(get_db),
) -> MedicaoResponse:
    """Update measurement data"""
    try:
        service = MedicaoService(db=db)
        medicao = service.get_medicao_por_cliente(medicao_id, cliente_id)
        if not medicao:
            raise HTTPException(status_code=404, detail="Medição não encontrada")
        
        medicao_atualizada = service.update(medicao_id, medicao_data)
        return MedicaoResponse.from_orm(medicao_atualizada)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao atualizar medição")


@router.delete("/{medicao_id}", status_code=204)
async def deletar_medicao(
    cliente_id: int,
    medicao_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete measurement record"""
    try:
        service = MedicaoService(db=db)
        medicao = service.get_medicao_por_cliente(medicao_id, cliente_id)
        if not medicao:
            raise HTTPException(status_code=404, detail="Medição não encontrada")
        
        service.delete(medicao_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao deletar medição")
```

---

## 🔄 Padrão Geral para Novas Rotas

### Template: `services/[entity]_service.py`

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from services.base import BaseService
from models.[entity] import [Entity]
from schemas.[entity] import [EntityCreate], [EntityUpdate]


class [Entity]Service(BaseService[[Entity], [EntityCreate]]):
    def __init__(self, db: Session):
        super().__init__(db, [Entity])
    
    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 10):
        """List owned entities"""
        return (
            self.db.query(self.model)
            .filter(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_[entity]_por_owner(self, entity_id: int, owner_id: int):
        """Get entity by owner (authorization)"""
        return (
            self.db.query(self.model)
            .filter(
                self.model.id == entity_id,
                self.model.owner_id == owner_id
            )
            .first()
        )
```

### Template: `api/routes/[entity].py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db
from services.[entity]_service import [Entity]Service
from schemas.[entity] import [EntityCreate], [EntityUpdate], [EntityResponse]

router = APIRouter(prefix="/[entities]", tags=["[entities]"])

@router.post("", status_code=201, response_model=[EntityResponse])
async def criar_[entity](data: [EntityCreate], db: Session = Depends(get_db)):
    try:
        service = [Entity]Service(db=db)
        entity = service.create(data)
        return [EntityResponse].from_orm(entity)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.get("", response_model=List[[EntityResponse]])
async def listar_[entities](skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = [Entity]Service(db=db)
    entities = service.get_all(skip=skip, limit=limit)
    return [[EntityResponse].from_orm(e) for e in entities]

# Continue com GET {id}, PATCH, DELETE...
```

---

## 📅 Timeline Sugerido

| Semana | Tarefa | Status |
|--------|--------|--------|
| Semana 1 | ✅ Cliente (CRUD) | ✅ CONCLUÍDO |
| Semana 2 | Nutricionista (CRUD) | ⏳ PLANEJADO |
| Semana 3 | Medicao (CRUD) | ⏳ PLANEJADO |
| Semana 4 | Observacao (CRUD) | ⏳ PLANEJADO |
| Semana 5 | TokenAcesso (CRUD) | ⏳ PLANEJADO |
| Semana 6 | Documento (Upload) | ⏳ PLANEJADO |
| Semana 7 | Auth (JWT) | ⏳ PLANEJADO |
| Semana 8 | QA & Testing | ⏳ PLANEJADO |

---

## 🎯 Próximo Comando para Você

Deseja que eu:

1. **Implemente Nutricionista Service + Routes** agora?
2. **Implemente Medicao Service + Routes** agora?
3. **Crie um template automatizado** para gerar novas rotas?
4. **Implemente autenticação com JWT** para proteger rotas?
5. **Outra coisa?**

---

Última atualização: 2024-01-15
