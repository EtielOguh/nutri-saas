# 🔗 Guia de Integração - TMB com Cliente

Este arquivo documenta como integrar o serviço TMB com o modelo de Cliente existente.

---

## 📋 Visão Geral

O modelo `Cliente` pode ser estendido para:
1. Armazenar dados antropométricos (peso, altura, idade)
2. Calcular e armazenar TMB/TDEE
3. Rastrear histórico de cálculos
4. Fornecer recomendações personalizadas

---

## 🔄 Fluxo de Integração

```
Cliente (dados básicos)
    ↓
Cliente + campos TMB (peso, altura, idade, sexo, nivel_atividade)
    ↓
TMBService.calcular_gasto_calorico()
    ↓
Atualizar campos tmb, tdee no Cliente
    ↓
Salvar no banco
```

---

## 1️⃣ Estender o Modelo Cliente

### Arquivo: `models/user_example.py` (ou seu arquivo de Cliente)

```python
# Adicionar imports
from typing import Optional
from sqlalchemy import Column, Float, String, DateTime
from datetime import datetime

# Estender modelo existente
class Cliente(Base):
    __tablename__ = "clientes"
    
    # === Campos Existentes ===
    id = Column(Integer, primary_key=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # ... outros campos ...
    
    # === Novos Campos - Dados Antropométricos ===
    peso_kg = Column(Float, nullable=True)  # Peso em kg
    altura_cm = Column(Float, nullable=True)  # Altura em cm
    idade_anos = Column(Integer, nullable=True)  # Idade em anos
    sexo = Column(String(1), nullable=True)  # M ou F
    
    # === Novos Campos - Nível de Atividade ===
    nivel_atividade = Column(
        String(20),
        default="moderado",
        nullable=False
        # Opções: sedentario, leve, moderado, intenso, muito_intenso
    )
    
    # === Novos Campos - Calculados ===
    tmb = Column(Float, nullable=True)  # Taxa Metabólica Basal (kcal/dia)
    tdee = Column(Float, nullable=True)  # Gasto total de energia (kcal/dia)
    imc = Column(Float, nullable=True)  # Índice de Massa Corporal
    
    # === Novos Campos - Auditoria ===
    data_calculo_tmb = Column(DateTime, nullable=True)  # Última atualização
    
    # === Métodos de Cálculo ===
    
    def pode_calcular_metabolismo(self) -> bool:
        """Verifica se cliente tem dados suficientes para cálculo."""
        return all([
            self.peso_kg,
            self.altura_cm,
            self.idade_anos,
            self.sexo in ['M', 'F']
        ])
    
    def calcular_metabolismo(self) -> dict:
        """
        Calcula TMB, TDEE e IMC.
        Retorna dicionário com resultados ou erros.
        """
        if not self.pode_calcular_metabolismo():
            return {
                "sucesso": False,
                "erro": "Dados incompletos: peso, altura, idade e sexo são obrigatórios"
            }
        
        try:
            from services.tmb_service import TMBService
            
            # Calcular gasto calórico completo
            resultado = TMBService.calcular_gasto_calorico(
                peso_kg=self.peso_kg,
                altura_cm=self.altura_cm,
                idade_anos=self.idade_anos,
                sexo=self.sexo.upper(),
                nivel_atividade=self.nivel_atividade
            )
            
            # Calcular IMC
            altura_m = self.altura_cm / 100
            imc = self.peso_kg / (altura_m ** 2)
            
            # Atualizar campos
            self.tmb = resultado['tmb']
            self.tdee = resultado['tdee']
            self.imc = round(imc, 2)
            self.data_calculo_tmb = datetime.utcnow()
            
            return {
                "sucesso": True,
                "tmb": self.tmb,
                "tdee": self.tdee,
                "imc": self.imc
            }
        
        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e)
            }
    
    def obter_recomendacao_calorica(self, objetivo: str) -> dict:
        """
        Retorna recomendação calórica baseada no objetivo.
        
        Objetivos: perder_leve, perder_moderado, ganhar_leve, ganhar_moderado
        """
        if not self.tdee:
            return {"erro": "Calcule metabolismo primeiro"}
        
        recomendacoes = {
            "perder_leve": {
                "calorias": self.tdee - 500,
                "mudanca_semana_g": 250,
                "duracao_10kg_semanas": 40
            },
            "perder_moderado": {
                "calorias": self.tdee - 750,
                "mudanca_semana_g": 375,
                "duracao_10kg_semanas": 27
            },
            "ganhar_leve": {
                "calorias": self.tdee + 500,
                "mudanca_semana_g": 250,
                "duracao_10kg_semanas": 40
            },
            "ganhar_moderado": {
                "calorias": self.tdee + 750,
                "mudanca_semana_g": 375,
                "duracao_10kg_semanas": 27
            },
            "manter": {
                "calorias": self.tdee,
                "mudanca_semana_g": 0,
                "duracao_10kg_semanas": None
            }
        }
        
        if objetivo not in recomendacoes:
            return {"erro": f"Objetivo inválido. Use: {', '.join(recomendacoes.keys())}"}
        
        return {
            "objetivo": objetivo,
            **recomendacoes[objetivo]
        }
```

---

## 2️⃣ Criar Schema Pydantic Atualizado

### Arquivo: `schemas/cliente.py` (atualizar)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    # ... campos existentes ...
    
    # Novos campos
    peso_kg: Optional[float] = Field(None, ge=1, le=635, description="Peso em kg")
    altura_cm: Optional[float] = Field(None, ge=50, le=300, description="Altura em cm")
    idade_anos: Optional[int] = Field(None, ge=1, le=150, description="Idade em anos")
    sexo: Optional[str] = Field(None, pattern="^[MF]$", description="M ou F")
    nivel_atividade: str = Field("moderado", description="Nível de atividade")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    tmb: Optional[float] = Field(None, description="Taxa Metabólica Basal")
    tdee: Optional[float] = Field(None, description="Gasto de Energia Diária Total")
    imc: Optional[float] = Field(None, description="Índice de Massa Corporal")
    data_calculo_tmb: Optional[datetime] = Field(None)
    
    class Config:
        from_attributes = True
```

---

## 3️⃣ Atualizar Service de Cliente

### Arquivo: `services/cliente_service.py` (atualizar)

```python
from typing import Optional
from sqlalchemy.orm import Session
from models.user_example import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteService:
    
    @staticmethod
    def criar_cliente(db: Session, cliente: ClienteCreate) -> dict:
        """Cria novo cliente e calcula metabolismo se dados disponíveis."""
        db_cliente = Cliente(**cliente.dict())
        
        # Calcular metabolismo se todos os dados estão presentes
        if db_cliente.pode_calcular_metabolismo():
            db_cliente.calcular_metabolismo()
        
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    
    @staticmethod
    def atualizar_cliente(db: Session, cliente_id: int, update_data: ClienteUpdate) -> dict:
        """Atualiza cliente e recalcula metabolismo se dados mudaram."""
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        
        if not db_cliente:
            return None
        
        # Atualizar campos
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_cliente, field, value)
        
        # Recalcular metabolismo se dados antropométricos mudaram
        if any(field in update_dict for field in ['peso_kg', 'altura_cm', 'idade_anos', 'sexo', 'nivel_atividade']):
            db_cliente.calcular_metabolismo()
        
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    
    @staticmethod
    def recalcular_tmb(db: Session, cliente_id: int) -> dict:
        """Força recálculo de TMB para um cliente."""
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        
        if not db_cliente:
            return {"erro": "Cliente não encontrado"}
        
        resultado = db_cliente.calcular_metabolismo()
        
        if resultado['sucesso']:
            db.commit()
            db.refresh(db_cliente)
        
        return resultado
```

---

## 4️⃣ Atualizar Rotas de Cliente

### Arquivo: `api/routes/cliente.py` (atualizar)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from services.cliente_service import ClienteService
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# ... rotas existentes ...

@router.post("/", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Cria novo cliente e calcula metabolismo se dados disponíveis."""
    return ClienteService.criar_cliente(db, cliente)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém dados completos do cliente incluindo metabolismo."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, update_data: ClienteUpdate, db: Session = Depends(get_db)):
    """Atualiza cliente e recalcula metabolismo se necessário."""
    cliente = ClienteService.atualizar_cliente(db, cliente_id, update_data)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/{cliente_id}/recalcular-tmb")
def recalcular_tmb(cliente_id: int, db: Session = Depends(get_db)):
    """Força recálculo de TMB para o cliente."""
    resultado = ClienteService.recalcular_tmb(db, cliente_id)
    if "erro" in resultado:
        raise HTTPException(status_code=404, detail=resultado["erro"])
    return resultado

@router.get("/{cliente_id}/recomendacao/{objetivo}")
def obter_recomendacao(cliente_id: int, objetivo: str, db: Session = Depends(get_db)):
    """Obtém recomendação calórica para objetivo específico."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    recomendacao = cliente.obter_recomendacao_calorica(objetivo)
    
    if "erro" in recomendacao:
        raise HTTPException(status_code=400, detail=recomendacao["erro"])
    
    return recomendacao
```

---

## 5️⃣ Migration de Banco de Dados

### Arquivo: `alembic/versions/add_tmb_fields.py`

```python
"""Add TMB fields to cliente table.

Revision ID: add_tmb_001
Revises: <previous_revision>
Create Date: 2026-04-02 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'add_tmb_001'
down_revision = None  # Alterar para a revision anterior
branch_labels = None
depends_on = None

def upgrade():
    """Adiciona campos de TMB ao modelo Cliente."""
    op.add_column('clientes', sa.Column('peso_kg', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('altura_cm', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('idade_anos', sa.Integer(), nullable=True))
    op.add_column('clientes', sa.Column('sexo', sa.String(1), nullable=True))
    op.add_column('clientes', sa.Column('nivel_atividade', sa.String(20), nullable=False, server_default='moderado'))
    op.add_column('clientes', sa.Column('tmb', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('tdee', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('imc', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('data_calculo_tmb', sa.DateTime(), nullable=True))

def downgrade():
    """Remove campos de TMB."""
    op.drop_column('clientes', 'data_calculo_tmb')
    op.drop_column('clientes', 'imc')
    op.drop_column('clientes', 'tdee')
    op.drop_column('clientes', 'tmb')
    op.drop_column('clientes', 'nivel_atividade')
    op.drop_column('clientes', 'sexo')
    op.drop_column('clientes', 'idade_anos')
    op.drop_column('clientes', 'altura_cm')
    op.drop_column('clientes', 'peso_kg')
```

Execute:
```bash
alembic upgrade head
```

---

## 6️⃣ Exemplos de Uso

### Criar Cliente com TMB

```python
from fastapi import FastAPI
from core.dependencies import get_db
from services.cliente_service import ClienteService
from schemas.cliente import ClienteCreate

# Via API
POST /clientes/
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "peso_kg": 75,
  "altura_cm": 180,
  "idade_anos": 30,
  "sexo": "M",
  "nivel_atividade": "moderado"
}

# Resposta
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "peso_kg": 75,
  "altura_cm": 180,
  "idade_anos": 30,
  "sexo": "M",
  "nivel_atividade": "moderado",
  "tmb": 1680.0,
  "tdee": 2604.0,
  "imc": 23.15,
  "data_calculo_tmb": "2026-04-02T10:30:00"
}
```

### Atualizar Peso e Recalcular TMB

```python
PUT /clientes/1
{
  "peso_kg": 72  # Perdeu 3kg
}

# TMB e TDEE são automaticamente recalculados
```

### Obter Recomendação para Perder Peso

```bash
GET /clientes/1/recomendacao/perder_leve

# Resposta
{
  "objetivo": "perder_leve",
  "calorias": 2104.0,
  "mudanca_semana_g": 250,
  "duracao_10kg_semanas": 40
}
```

### Recalcular TMB Manualmente

```bash
POST /clientes/1/recalcular-tmb

# Resposta
{
  "sucesso": true,
  "tmb": 1680.0,
  "tdee": 2604.0,
  "imc": 23.15
}
```

---

## 7️⃣ Testes de Integração

### Arquivo: `test_cliente_tmb.py`

```python
import pytest
from sqlalchemy.orm import Session
from models.user_example import Cliente
from services.cliente_service import ClienteService
from schemas.cliente import ClienteCreate, ClienteUpdate

class TestClienteTMB:
    
    def test_cliente_calcula_tmb_ao_criar(self, db: Session):
        """Cliente com dados antropométricos calcula TMB automaticamente."""
        cliente = ClienteCreate(
            nome="Maria",
            email="maria@test.com",
            peso_kg=65,
            altura_cm=165,
            idade_anos=25,
            sexo="F",
            nivel_atividade="leve"
        )
        
        db_cliente = ClienteService.criar_cliente(db, cliente)
        
        assert db_cliente.tmb is not None
        assert db_cliente.tdee is not None
        assert db_cliente.imc is not None
        assert db_cliente.data_calculo_tmb is not None
    
    def test_cliente_sem_dados_nao_calcula_tmb(self, db: Session):
        """Cliente sem dados antropométricos não calcula TMB."""
        cliente = ClienteCreate(
            nome="João",
            email="joao@test.com"
            # Sem peso, altura, idade, sexo
        )
        
        db_cliente = ClienteService.criar_cliente(db, cliente)
        
        assert db_cliente.tmb is None
        assert db_cliente.tdee is None
        assert db_cliente.imc is None
    
    def test_atualizar_peso_recalcula_tmb(self, db: Session):
        """Atualizar peso recalcula TMB."""
        # Criar cliente
        cliente = ClienteCreate(
            nome="Pedro",
            email="pedro@test.com",
            peso_kg=80,
            altura_cm=180,
            idade_anos=35,
            sexo="M",
            nivel_atividade="moderado"
        )
        db_cliente = ClienteService.criar_cliente(db, cliente)
        tmb_original = db_cliente.tmb
        
        # Atualizar peso
        update = ClienteUpdate(peso_kg=70)
        db_cliente = ClienteService.atualizar_cliente(db, db_cliente.id, update)
        
        # TMB deve ter mudado (menos ~100 kcal)
        assert db_cliente.tmb != tmb_original
        assert db_cliente.tmb < tmb_original
    
    def test_recomendacao_calorica(self, db: Session):
        """Gera recomendação calórica correta."""
        cliente_create = ClienteCreate(
            nome="Ana",
            email="ana@test.com",
            peso_kg=70,
            altura_cm=175,
            idade_anos=30,
            sexo="F",
            nivel_atividade="intenso"
        )
        cliente = ClienteService.criar_cliente(db, cliente_create)
        
        # Teste cada objetivo
        for objetivo in ["perder_leve", "perder_moderado", "ganhar_leve", "ganhar_moderado", "manter"]:
            recomendacao = cliente.obter_recomendacao_calorica(objetivo)
            
            assert recomendacao["objetivo"] == objetivo
            assert "calorias" in recomendacao
            assert recomendacao["calorias"] > 0

pytest.main([__file__, "-v"])
```

---

## 8️⃣ Checklist de Implementação

- [ ] Adicionar campos ao modelo `Cliente`
- [ ] Adicionar métodos de cálculo ao modelo
- [ ] Atualizar schema Pydantic
- [ ] Atualizar service de Cliente
- [ ] Atualizar rotas de Cliente
- [ ] Criar migration de banco de dados
- [ ] Executar migration: `alembic upgrade head`
- [ ] Implementar testes de integração
- [ ] Executar testes: `pytest test_cliente_tmb.py -v`
- [ ] Testar endpoints via Swagger
- [ ] Documentar no README

---

## 9️⃣ Endpoints Finais

```
POST /clientes/                              → Criar cliente com TMB
GET  /clientes/{id}                          → Obter dados completos
PUT  /clientes/{id}                          → Atualizar cliente (recalcula se necessário)
POST /clientes/{id}/recalcular-tmb          → Forçar recálculo
GET  /clientes/{id}/recomendacao/{objetivo} → Obter recomendação calórica
```

---

## 🔟 Status

✅ Integração de TMB com Cliente: **Pronta para implementação**

Próximas ações:
1. Preparar migration de banco de dados
2. Implementar mudanças nos modelos
3. Atualizar schemas e services
4. Testar endpoints
5. Documentar para usuários

---

**Last Updated:** 2 de abril de 2026
