# 📚 Guia de Modelos SQLAlchemy - Sistema de Nutricionistas

Documentação prática para trabalhar com os modelos SQLAlchemy no sistema SaaS de nutricionistas.

## 🎯 Visão Geral dos Modelos

7 modelos com relacionamentos bem definidos:

| Modelo | Tabela | Tipo | Relacionamentos |
|--------|--------|------|-----------------|
| **Nutricionista** | nutricionistas | Principal | 1 → M Clientes<br>1 → 1 Configuracao |
| **ConfiguracaoNutricionista** | configuracoes_nutricionista | Config | M ← 1 Nutricionista |
| **Cliente** | clientes | Principal | M ← 1 Nutricionista<br>1 → M Medicoes<br>1 → M Observacoes<br>1 → 1 TokenAcesso<br>1 → M DocumentosPDF |
| **Medicao** | medicoes | Transacional | M ← 1 Cliente |
| **Observacao** | observacoes | Transacional | M ← 1 Cliente |
| **TokenAcessoCliente** | tokens_acesso_cliente | Autenticação | 1 ← 1 Cliente |
| **DocumentoPDF** | documentos_pdf | Armazenamento | M ← 1 Cliente |

---

## 🚀 Como Importar Modelos

**Forma 1: Importar individuais (recomendado)**
```python
from models import Nutricionista, Cliente, Medicao
```

**Forma 2: Importar quase tudo**
```python
from models import *
```

---

## 💻 Padrões de Uso em Rotas FastAPI

### Pattern 1: CRUD Básico com Dependency Injection

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import Nutricionista, Cliente

router = APIRouter()

@router.post("/nutricionistas/")
def criar_nutricionista(
    nome: str, 
    email: str, 
    senha: str,
    db: Session = Depends(get_db)
):
    """Cria novo nutricionista."""
    nutricionista = Nutricionista(
        nome=nome,
        email=email,
        senha_hash=hash_password(senha)  # Use bcrypt!
    )
    db.add(nutricionista)
    db.commit()
    db.refresh(nutricionista)
    return nutricionista


@router.get("/nutricionistas/{id}")
def obter_nutricionista(id: int, db: Session = Depends(get_db)):
    """Obtém nutricionista por ID."""
    nutricionista = db.query(Nutricionista).filter(
        Nutricionista.id == id
    ).first()
    if not nutricionista:
        raise HTTPException(status_code=404, detail="Não encontrado")
    return nutricionista
```

### Pattern 2: Criar Cliente com Configuração

```python
@router.post("/clientes/")
def criar_cliente(
    nutricionista_id: int,
    nome: str,
    idade: int,
    altura: float,
    db: Session = Depends(get_db)
):
    """Cria novo cliente."""
    # Verificar nutricionista
    nutricionista = db.query(Nutricionista).filter(
        Nutricionista.id == nutricionista_id
    ).first()
    if not nutricionista:
        raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
    
    # Criar cliente
    cliente = Cliente(
        nutricionista_id=nutricionista_id,
        nome=nome,
        idade=idade,
        altura=altura
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente
```

### Pattern 3: Registrar Medição com Histórico

```python
@router.post("/clientes/{cliente_id}/medicoes/")
def registrar_medicao(
    cliente_id: int,
    peso: float,
    db: Session = Depends(get_db)
):
    """Registra nova medição de peso."""
    # Verificar cliente
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404)
    
    # Criar medição
    medicao = Medicao(
        cliente_id=cliente_id,
        peso=peso
    )
    db.add(medicao)
    db.commit()
    
    return {"id": medicao.id, "peso": medicao.peso, "data": medicao.data_medicao}
```

### Pattern 4: Listar com Filtros

```python
@router.get("/clientes/")
def listar_clientes(
    nutricionista_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista clientes com paginação."""
    clientes = db.query(Cliente).filter(
        Cliente.nutricionista_id == nutricionista_id
    ).offset(skip).limit(limit).all()
    return clientes
```

### Pattern 5: Obter Dados Relacionados

```python
@router.get("/clientes/{cliente_id}/completo")
def obter_cliente_completo(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém cliente com todos os dados relacionados."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404)
    
    return {
        "cliente": cliente,
        "nutricionista": cliente.nutricionista,
        "medicoes": cliente.medicoes,
        "observacoes": cliente.observacoes,
        "documentos": cliente.documentos,
        "ultimo_peso": cliente.medicoes[-1].peso if cliente.medicoes else None
    }
```

### Pattern 6: Autenticação por Token

```python
from fastapi import Header

@router.get("/meus-dados/")
def obter_meus_dados(
    x_token: str = Header(...),
    db: Session = Depends(get_db)
):
    """Obtém dados do cliente usando token."""
    from models import TokenAcessoCliente
    
    token_obj = db.query(TokenAcessoCliente).filter(
        TokenAcessoCliente.token_unico == x_token
    ).first()
    
    if not token_obj:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cliente = token_obj.cliente
    return {
        "nome": cliente.nome,
        "idade": cliente.idade,
        "altura": cliente.altura,
        "nutricionista": cliente.nutricionista.nome
    }
```

---

## 🔄 Transações e Context Managers

```python
from core.db_utils import DBTransaction
from core.database import SessionLocal

# Usar com context manager
db = SessionLocal()
try:
    with DBTransaction(db):
        # Adicionar múltiplos itens
        cliente = Cliente(...)
        db.add(cliente)
        medicao = Medicao(cliente_id=cliente.id, ...)
        db.add(medicao)
        # Auto-commit aqui
except Exception as e:
    print(f"Rollback automático: {e}")
```

---

## 📊 Queries Avançadas

### Encontrar Clientes sem Medição Recente

```python
from datetime import datetime, timedelta

def clientes_sem_medicao_recente(nutricionista_id, dias=30):
    db = SessionLocal()
    
    data_limite = datetime.utcnow() - timedelta(days=dias)
    
    clientes = db.query(Cliente).filter(
        Cliente.nutricionista_id == nutricionista_id
    ).all()
    
    resultado = []
    for cliente in clientes:
        if not cliente.medicoes or cliente.medicoes[-1].data_medicao < data_limite:
            resultado.append(cliente)
    
    return resultado
```

### Peso Médio por Cliente

```python
from sqlalchemy import func

def peso_medio_cliente(cliente_id):
    db = SessionLocal()
    
    media = db.query(func.avg(Medicao.peso)).filter(
        Medicao.cliente_id == cliente_id
    ).scalar()
    
    return media or 0.0
```

### Acompanhamento de Progresso

```python
def acompanhamento_cliente(cliente_id):
    db = SessionLocal()
    
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    medicoes = sorted(cliente.medicoes, key=lambda x: x.data_medicao)
    
    if len(medicoes) < 2:
        return {"status": "Insuficientes medições"}
    
    primeiro = medicoes[0].peso
    ultimo = medicoes[-1].peso
    variacao = primeiro - ultimo  # Positivo = perda de peso
    
    return {
        "peso_inicial": primeiro,
        "peso_atual": ultimo,
        "variacao": variacao,
        "percentual": (variacao / primeiro * 100),
        "total_medicoes": len(medicoes)
    }
```

---

## 🔐 Boas Práticas

### ✅ Faça

```python
# 1. Use dependency injection
def minha_rota(db: Session = Depends(get_db)):
    pass

# 2. Feche a sessão
try:
    resultado = db.query(...).first()
finally:
    db.close()

# 3. Use índices para queries frequentes
cliente = db.query(Cliente).filter(Cliente.email == email).first()

# 4. Use relacionamentos
print(cliente.nutricionista.nome)  # Lazy load automático

# 5. Valide relacionamentos
if not cliente:
    raise HTTPException(status_code=404)
```

### ❌ Não Faça

```python
# 1. Não crie sessão global
db_global = SessionLocal()  # ❌

# 2. Não use strings em queries
query = f"SELECT * FROM clientes WHERE id = {id}"  # ❌ SQL Injection!

# 3. Não faça queries em loops
for cliente in clientes:
    medicoes = db.query(Medicao).filter(...)  # ❌ N+1 queries

# 4. Não ignore exceptions
try:
    db.commit()
except:
    pass  # ❌

# 5. Não esqueça de refresh após commit
db.add(cliente)
db.commit()
print(cliente.id)  # Pode ser None! Use db.refresh(cliente)
```

---

## 🧪 Testes com Modelos

```python
import pytest
from core.database import SessionLocal

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_criar_nutricionista(db):
    nutricionista = Nutricionista(
        nome="Test",
        email="test@example.com",
        senha_hash="hash"
    )
    db.add(nutricionista)
    db.commit()
    
    assert nutricionista.id is not None
    
    result = db.query(Nutricionista).filter(
        Nutricionista.id == nutricionista.id
    ).first()
    assert result.nome == "Test"
```

---

## 📈 Escalabilidade

Para sistemas com muitos usuários:

1. **Use lazy=True em relacionamentos pesados:**
```python
medicoes: Mapped[List["Medicao"]] = relationship(
    "Medicao",
    back_populates="cliente",
    lazy="select",  # Carrega sob demanda
    cascade="all, delete-orphan"
)
```

2. **Crie índices compostos:**
```python
__table_args__ = (
    Index("idx_cliente_nutricionista_data", "nutricionista_id", "created_at"),
)
```

3. **Use pagination:**
```python
page = 0
limit = 10
clientes = db.query(Cliente).offset(page*limit).limit(limit).all()
```

4. **Cache resultados:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_nutricionista_config(id):
    return db.query(ConfiguracaoNutricionista).filter(...).first()
```

---

## 📚 Referências

- [MODELS.md](MODELS.md) - Documentação detalhada dos modelos
- [exemplos_modelos.py](exemplos_modelos.py) - Exemplos de código
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [FastAPI + SQLAlchemy](https://fastapi.tiangolo.com/advanced/sql-databases/)

---

**Versão:** 1.0
**Última atualização:** 2 abril 2026
