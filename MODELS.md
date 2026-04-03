# 📊 Modelos SQLAlchemy - Sistema de Nutricionistas

Dokumentação completa dos modelos SQLAlchemy criados para o sistema SaaS de nutricionistas.

## 📈 Diagrama de Relacionamentos

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  NUTRICIONISTA                    CONFIGURACAO_NUTRICIONISTA         │
│  ├─ id (PK)                       ├─ id (PK)                         │
│  ├─ nome                          ├─ nutricionista_id (FK, UQ) ──────┤┐
│  ├─ email (UQ)                    ├─ logo_url                        ││
│  ├─ senha_hash                    ├─ cor_primaria                    ││ 1:1
│  ├─ created_at                    ├─ valor_consulta                  ││
│  ├─ updated_at                    ├─ link_agendamento                ││
│  │                                ├─ created_at                      ││
│  │ (1)                            ├─ updated_at                      ││
│  │                                                                    ││
│  │ ┌──── (M) CLIENTE              └────────────────────────────────┘│
│  └─────┬─────────────────────────────────────────────────────────────┘
│        │
│        │
│        ├─ id (PK)
│        ├─ nutricionista_id (FK)
│        ├─ nome
│        ├─ idade
│        ├─ altura
│        ├─ objetivo
│        ├─ created_at
│        ├─ updated_at
│        │
│        ├─── (M) MEDICOES
│        │    ├─ id (PK)
│        │    ├─ cliente_id (FK)
│        │    ├─ peso
│        │    ├─ data_medicao
│        │    ├─ created_at
│        │    └─ updated_at
│        │
│        ├─── (M) OBSERVACOES
│        │    ├─ id (PK)
│        │    ├─ cliente_id (FK)
│        │    ├─ texto
│        │    ├─ created_at
│        │    └─ updated_at
│        │
│        ├─── (1) TOKEN_ACESSO_CLIENTE
│        │    ├─ id (PK)
│        │    ├─ cliente_id (FK, UQ)
│        │    ├─ token_unico (UQ)
│        │    ├─ created_at
│        │    └─ updated_at
│        │
│        └─── (M) DOCUMENTOS_PDF
│             ├─ id (PK)
│             ├─ cliente_id (FK)
│             ├─ url_pdf
│             ├─ created_at
│             └─ updated_at
│
│ PK = Primary Key
│ FK = Foreign Key
│ UQ = Unique
│ (1) = One to One
│ (M) = One to Many

```

---

## 📋 Referência de Modelos

### 1. **Nutricionista**

Representa um profissional nutricionista no sistema.

```python
class Nutricionista(BaseModel):
    __tablename__ = "nutricionistas"
    
    # Campos
    nome: Mapped[str]           # Obrigatório
    email: Mapped[str]          # Obrigatório, Único
    senha_hash: Mapped[str]     # Obrigatório
    
    # Relacionamentos
    clientes: Mapped[List["Cliente"]]                    # 1:M
    configuracao: Mapped["ConfiguracaoNutricionista"]   # 1:1
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_nutricionista_email` em `email`

**Deletar:**
- Cascade: Deleta todos os clientes

---

### 2. **ConfiguracaoNutricionista**

Configurações personalizadas do nutricionista.

```python
class ConfiguracaoNutricionista(BaseModel):
    __tablename__ = "configuracoes_nutricionista"
    
    # Foreign Key
    nutricionista_id: Mapped[int]       # PK, FK (Cascade)
    
    # Campos
    logo_url: Mapped[str | None]        # Opcional
    cor_primaria: Mapped[str]           # Padrão: #0066CC
    valor_consulta: Mapped[float]       # Obrigatório
    link_agendamento: Mapped[str | None] # Opcional
    
    # Relacionamento
    nutricionista: Mapped["Nutricionista"]  # Reverso: configuracao
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_config_nutricionista_id` em `nutricionista_id`

**Relação:**
- 1:1 com Nutricionista (uselist=False)

---

### 3. **Cliente**

Representa um cliente/paciente de um nutricionista.

```python
class Cliente(BaseModel):
    __tablename__ = "clientes"
    
    # Foreign Key
    nutricionista_id: Mapped[int]   # Obrigatório, FK (Cascade)
    
    # Campos
    nome: Mapped[str]               # Obrigatório
    idade: Mapped[int | None]       # Opcional
    altura: Mapped[float | None]    # Opcional (em cm)
    objetivo: Mapped[str | None]    # Opcional
    
    # Relacionamentos
    nutricionista: Mapped["Nutricionista"]              # Reverso: clientes
    medicoes: Mapped[List["Medicao"]]                   # 1:M
    observacoes: Mapped[List["Observacao"]]             # 1:M
    token_acesso: Mapped[Optional["TokenAcessoCliente"]] # 1:1
    documentos: Mapped[List["DocumentoPDF"]]            # 1:M
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_cliente_nutricionista_id` em `nutricionista_id`
- `idx_cliente_nome` em `nome`

**Deletar:**
- Cascade: Deleta todas medicoes, observacoes, token_acesso, documentos

---

### 4. **Medicao**

Registros de peso e data de medição.

```python
class Medicao(BaseModel):
    __tablename__ = "medicoes"
    
    # Foreign Key
    cliente_id: Mapped[int]         # Obrigatório, FK (Cascade)
    
    # Campos
    peso: Mapped[float]             # Obrigatório (em kg)
    data_medicao: Mapped[datetime]  # Obrigatório (auto: agora)
    
    # Relacionamento
    cliente: Mapped["Cliente"]      # Reverso: medicoes
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_medicao_cliente_id` em `cliente_id`
- `idx_medicao_data` em `data_medicao`
- `idx_medicao_cliente_data` em `(cliente_id, data_medicao)` - Composite

---

### 5. **Observacao**

Notas e observações do nutricionista.

```python
class Observacao(BaseModel):
    __tablename__ = "observacoes"
    
    # Foreign Key
    cliente_id: Mapped[int]         # Obrigatório, FK (Cascade)
    
    # Campos
    texto: Mapped[str]              # Obrigatório (Text)
    
    # Relacionamento
    cliente: Mapped["Cliente"]      # Reverso: observacoes
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_observacao_cliente_id` em `cliente_id`

---

### 6. **TokenAcessoCliente**

Token único para acesso restrito (1:1 com Cliente).

```python
class TokenAcessoCliente(BaseModel):
    __tablename__ = "tokens_acesso_cliente"
    
    # Foreign Key
    cliente_id: Mapped[int]         # PK, FK (Cascade), UQ
    
    # Campos
    token_unico: Mapped[str]        # Obrigatório, Único
    
    # Relacionamento
    cliente: Mapped["Cliente"]      # Reverso: token_acesso
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_token_cliente_id` em `cliente_id`
- `idx_token_unico` em `token_unico`

**Relação:**
- 1:1 com Cliente (uselist=False)

---

### 7. **DocumentoPDF**

Referências a documentos PDF associados.

```python
class DocumentoPDF(BaseModel):
    __tablename__ = "documentos_pdf"
    
    # Foreign Key
    cliente_id: Mapped[int]         # Obrigatório, FK (Cascade)
    
    # Campos
    url_pdf: Mapped[str]            # Obrigatório
    
    # Relacionamento
    cliente: Mapped["Cliente"]      # Reverso: documentos
    
    # Herança de BaseModel
    id: Mapped[int]             # PK
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Índices:**
- `idx_documento_cliente_id` em `cliente_id`

---

## 💻 Exemplos de Uso

### Importar Modelos

```python
from models import (
    Nutricionista,
    ConfiguracaoNutricionista,
    Cliente,
    Medicao,
    Observacao,
    TokenAcessoCliente,
    DocumentoPDF,
)
```

### Criar um Nutricionista

```python
from core.database import SessionLocal

db = SessionLocal()

nutricionista = Nutricionista(
    nome="Dr. João Silva",
    email="joao@example.com",
    senha_hash="hashed_password"
)
db.add(nutricionista)
db.commit()
db.refresh(nutricionista)

print(f"Criado: {nutricionista}")
```

### Criar Cliente para um Nutricionista

```python
cliente = Cliente(
    nutricionista_id=nutricionista.id,
    nome="Maria Santos",
    idade=35,
    altura=165.0,  # em cm
    objetivo="Perder peso"
)
db.add(cliente)
db.commit()
```

### Registrar Medição

```python
medicao = Medicao(
    cliente_id=cliente.id,
    peso=75.5  # em kg
)
db.add(medicao)
db.commit()
```

### Adicionar Observação

```python
obs = Observacao(
    cliente_id=cliente.id,
    texto="Cliente apresenta boa adesão ao tratamento"
)
db.add(obs)
db.commit()
```

### Criar Token de Acesso

```python
import secrets

token = TokenAcessoCliente(
    cliente_id=cliente.id,
    token_unico=secrets.token_urlsafe(32)
)
db.add(token)
db.commit()
```

### Fazer Queries

```python
# Todos os clientes de um nutricionista
clientes = db.query(Cliente).filter(
    Cliente.nutricionista_id == nutricionista.id
).all()

# Últimas 5 medições de um cliente
medicoes = db.query(Medicao).filter(
    Medicao.cliente_id == cliente.id
).order_by(Medicao.data_medicao.desc()).limit(5).all()

# Encontrar cliente por token
token = db.query(TokenAcessoCliente).filter(
    TokenAcessoCliente.token_unico == "123abc..."
).first()

if token:
    cliente = token.cliente
```

### Acessar Relacionamentos

```python
# A partir de Nutricionista
print(nutricionista.clientes)    # List[Cliente]
print(nutricionista.configuracao) # ConfiguracaoNutricionista

# A partir de Cliente
print(cliente.nutricionista)  # Nutricionista
print(cliente.medicoes)       # List[Medicao]
print(cliente.observacoes)    # List[Observacao]
print(cliente.token_acesso)   # TokenAcessoCliente
print(cliente.documentos)     # List[DocumentoPDF]

# A partir de Medicao
print(medicao.cliente)        # Cliente
```

---

## 🔄 Cascade e Deletar

Todos os relacionamentos principais usam `cascade="all, delete-orphan"`:

```
Deletar Nutricionista
    ↓
Deleta todos Clientes
    ↓
    ├─ Deleta todas Medicoes
    ├─ Deleta todas Observacoes
    ├─ Deleta TokenAcessoCliente
    └─ Deleta todos DocumentosPDF
```

---

## 📚 Herança de BaseModel

Todos os modelos herdam de `BaseModel` que inclui:

```python
class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[int]             # Primary Key
    created_at: Mapped[datetime] # Auto: agora()
    updated_at: Mapped[datetime] # Auto: agora(), onupdate: agora()
```

---

## ✅ Testes

Executar suite de testes dos modelos:

```bash
python test_models.py

# Esperado:
# ✅ test_imports
# ✅ test_model_structure
# ✅ test_relationships
# ✅ test_foreign_keys
# ✅ test_table_creation
# 5/5 testes passaram 🎉
```

---

## 🚀 Próximos Passos

1. ✅ Modelos criados
2. Criar migrations: `alembic revision --autogenerate -m "Create tables"`
3. Aplicar migrations: `alembic upgrade head`
4. Criar schemas Pydantic em `schemas/`
5. Criar services em `services/`
6. Criar rotas em `api/routes/`

---

**Versão:** 1.0
**Data:** 2 de abril de 2026
