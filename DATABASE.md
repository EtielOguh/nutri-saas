# 📊 Configuração de Banco de Dados - PostgreSQL SaaS

## 🎯 Visão Geral

Configuração completa para aplicação SaaS com:
- **PostgreSQL** como banco principal
- **SQLAlchemy 2.0** como ORM
- **Alembic** para gerenciamento de migrations
- **Connection pooling** otimizado para múltiplos usuários simultâneos

## 🚀 Quick Start

### 1. Pré-requisitos

```bash
# macOS - Instalar PostgreSQL
brew install postgresql@15

# Iniciar servidor
brew services start postgresql@15

# Verificar
psql --version
```

### 2. Configuração Automática

```bash
# Setup completo do banco
python scripts/db_manager.py init

# Verificar configuração
python scripts/db_manager.py check
```

### 3. Iniciar Aplicação

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

Acesse: http://localhost:8000/api/docs

## 📁 Estrutura de Arquivos

```
core/
├── config.py          # Variáveis de ambiente (Settings + get_database_url)
├── database.py        # Engine, SessionLocal, get_db(), init_db(), close_db()
├── db_utils.py        # Utilitários (Health, Transactions, Bulk, Schema, Migration)
└── dependencies.py    # Injeção de dependências

models/
├── base.py           # Base (DeclarativeBase) + BaseModel (com timestamps)
└── user_example.py   # Exemplo de modelo

alembic/
├── env.py            # Configuração Alembic (usa settings.get_database_url)
├── versions/         # Histórico de migrations
└── templates/        # Templates

scripts/
├── db_manager.py     # CLI para gerenciar banco (check, init, reset, seed)
├── db_setup.sh       # Setup script bash (legacy)
└── migrations.sh     # Wrapper para Alembic
```

## 🔧 Configuração PostgreSQL

### Variáveis de Ambiente (`.env`)

Crie arquivo `.env` na raiz com:

```bash
# APLICAÇÃO
ENVIRONMENT=development
DEBUG=True

# POSTGRESQL - Opção 1: URL Completa (prioritária)
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/nutri_saas

# OU Opção 2: Componentes (usada se DATABASE_URL vazia)
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=nutri_saas
DB_DRIVER=psycopg2

# Pool de Conexões (otimizado para SaaS)
DB_POOL_SIZE=10         # Conexões mantidas
DB_MAX_OVERFLOW=20      # Conexões adicionais em picos
DB_POOL_RECYCLE=3600    # Reciclar a cada 1h (segundos)
DB_ECHO=True            # Log SQL em desenvolvimento

# JWT
SECRET_KEY=sua-chave-secreta-muito-segura-em-producao
ALGORITHM=HS256
```

### Pool de Conexões para Sistema SaaS

Dimensionamento baseado em usuários simultâneos:

| Usuários | pool_size | max_overflow | Observação |
|----------|-----------|--------------|-----------|
| 5-10     | 10        | 20           | Padrão (pequeno time) |
| 20-50    | 25        | 50           | Startup médio |
| 50-100   | 50        | 100          | Aplicação em crescimento |
| 100+     | 100+      | 200+         | Grande escala |

## 📝 Usando em Rotas FastAPI

### Dependency Injection (Recomendado)

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import get_db

app = FastAPI()

@app.get("/usuarios")
def list_usuarios(db: Session = Depends(get_db)):
    from models.user_example import User
    return db.query(User).all()

@app.post("/usuarios")
def create_usuario(name: str, db: Session = Depends(get_db)):
    from models.user_example import User
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### Transactions com Context Manager

```python
from core.db_utils import DBTransaction
from core.database import SessionLocal

db = SessionLocal()
with DBTransaction(db):
    # Seu código
    # Commit automático ao sair
    # Rollback automático em erro
    pass
```

### Operações em Lote

```python
from core.db_utils import DBBulkOperations
from core.database import SessionLocal

db = SessionLocal()
users = [User(name=f"User {i}") for i in range(1000)]
total = DBBulkOperations.bulk_insert(db, users, batch_size=500)
```

## 🔄 Migrations com Alembic

### Criar Nova Migration

```bash
# Automática (detecta mudanças no modelo)
alembic revision --autogenerate -m "Desc. da mudança"

# Manual
alembic revision -m "Desc. da mudança"
```

### Aplicar Migrations

```bash
# Atualizar para versão mais recente
alembic upgrade head

# Atualizar +2 versões
alembic upgrade +2

# Voltar -1 versão
alembic downgrade -1
```

### Verificar Status

```bash
# Ver versão atual
alembic current

# Ver histórico completo
alembic history

# Ver detalhes da versão
alembic show <revision_id>
```

## 🛠️ CLI de Gerenciamento (db_manager.py)

### Verificar Status

```bash
python scripts/db_manager.py check

# Saída:
# 🔍 Verificando configuracao do banco de dados...
# 📍 Host: localhost:5432
# 📚 Database: nutri_saas
# ✅ PostgreSQL esta acessivel
# ✅ Banco 'nutri_saas' ja existe
# 📊 Tabelas encontradas (3)
```

### Inicializar Banco

```bash
# Setup completo
python scripts/db_manager.py init

# Skip migrations
python scripts/db_manager.py init --skip-migrations
```

### Resetar Banco

```bash
# CUIDADO: Deleta todos os dados!
python scripts/db_manager.py reset
```

### Popular com Dados de Exemplo

```bash
python scripts/db_manager.py seed
```

## 🏥 Verificação de Saúde

### Checar Conexão

```python
from core.db_utils import DBHealthCheck
from core.database import SessionLocal

db = SessionLocal()
if DBHealthCheck.check_connection(db):
    print("✅ Conexão ativa")
```

### Inspeccionar Schema

```python
from core.db_utils import DBSchema
from core.database import SessionLocal

db = SessionLocal()

# Colunas de uma tabela
columns = DBSchema.get_table_columns(db, User)
# {'id': 'INTEGER', 'name': 'VARCHAR', 'created_at': 'DATETIME'}

# Todas as tabelas
tables = DBSchema.get_all_tables(db)
# ['users', 'orders', 'products']
```

## 🚨 Troubleshooting

### PostgreSQL não inicia

```bash
# Verificar status
brew services list

# Iniciar serviço
brew services start postgresql@15

# Verificar conexão
psql -U postgres -c "SELECT 1"
```

### Erro: "database does not exist"

```bash
# Criar banco manualmente
psql -U postgres -c "CREATE DATABASE nutri_saas;"

# Ou usar CLI
python scripts/db_manager.py init
```

### Erro: "Connection pool exhausted"

Aumentar em `.env`:
```bash
DB_POOL_SIZE=25
DB_MAX_OVERFLOW=50
```

### Migration falha

```bash
# Ver status
alembic current

# Reverter última migration
alembic downgrade -1

# Tentar novamente
alembic upgrade head
```

## 📚 Arquivos de Referência

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [FastAPI + Databases](https://fastapi.tiangolo.com/advanced/sql-databases/)
    preco: float = Field(..., gt=0)
    quantidade: int = Field(default=0)

class ProdutoResponse(ProdutoCreate):
    id: int
```

3. Crie o serviço em `services/seu_service.py`:

```python
from services.base import BaseService
from models.seu_modelo import Produto
from schemas.seu_schema import ProdutoCreate

class ProdutoService(BaseService[Produto, ProdutoCreate]):
    def __init__(self, db):
        super().__init__(Produto, db)
```

### Usar em uma Rota

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.seu_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/")
async def listar_produtos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return {"items": service.get_all(skip, limit)}

@router.post("/")
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    novo_produto = service.create(produto)
    return novo_produto
```

## Migrations com Alembic

### Inicializar Migrations

```bash
# Alembic já está setado, mas se precisar reinicializar:
alembic init alembic
```

### Criar uma Migration

```bash
# Automática - detecta mudanças nos modelos
alembic revision --autogenerate -m "Add user table"

# Manual - para migrations mais complexas
alembic revision -m "Add custom logic"
```

### Aplicar Migrations

```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Aplicar para uma versão específica
alembic upgrade 1a2b3c4d5e6f

# Reverter para versão anterior
alembic downgrade -1

# Ver versão atual
alembic current

# Ver histórico
alembic history
```

### Scripts Úteis

```bash
# Tornar script executável
chmod +x scripts/migrations.sh

# Usar os comandos
./scripts/migrations.sh help
./scripts/migrations.sh revision "nome da migracao"
./scripts/migrations.sh upgrade
./scripts/migrations.sh history
```

## Exemplo Completo: Sistema de Usuários

### 1. Modelo (`models/user.py`)

```python
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
```

### 2. Schema (`schemas/user.py`)

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)

class UserResponse(UserCreate):
    id: int
    is_active: bool
```

### 3. Serviço (`services/user.py`)

```python
from services.base import BaseService
from models.user import User
from schemas.user import UserCreate

class UserService(BaseService[User, UserCreate]):
    def __init__(self, db):
        super().__init__(User, db)
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
```

### 4. Rota (`api/routes/users.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.user import UserService
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all(skip, limit)

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    existing = service.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 5. Incluir Rota em `main.py`

```python
from api.routes import users
app.include_router(users.router)
```

### 6. Aplicar Migration

```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head
```

## Conexão com Banco de Dados

### SQLite (Desenvolvimento)

```env
DATABASE_URL=sqlite:///./nutri_saas.db
```

Vantagens:
- Sem setup externo
- Ideal para desenvolvimento
- Arquivo único

### PostgreSQL (Produção)

```env
DATABASE_URL=postgresql://usuario:senha@localhost/nutri_saas
```

Instalação do PostgreSQL no macOS:

```bash
# Com Homebrew
brew install postgresql@15
brew services start postgresql@15

# Criar banco de dados
createdb nutri_saas

# Criar usuário
psql -d nutri_saas -c "CREATE USER app_user WITH PASSWORD 'sua_senha_segura';"
```

## Boas Práticas

1. **Sempre use Sessions**: Injete `Session = Depends(get_db)` nas rotas
2. **Modularize**: Coloque lógica em services, não em rotas
3. **Validações**: Use Pydantic para validar dados
4. **Migrations**: Faça commits pequenos na migrations
5. **Índices**: Adicione índices em campos frequentemente consultados
6. **Constraints**: Use unique, foreign keys, etc.

## Troubleshooting

### Erro de Importação de Modelos

Se o Alembic não detecta seus modelos:

```bash
# Importe seus modelos em alembic/env.py
from models import user, produto, ...  # Adicione aqui
```

### Migrations Conflitantes

```bash
# Verifique branches
alembic branches

# Mescle branches
alembic merge
```

### Redefinir Banco de Dados

```bash
# CUIDADO: Deleta tudo!
alembic downgrade base
alembic upgrade head
```

## Referências

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [FastAPI Database](https://fastapi.tiangolo.com/advanced/sql-databases/)
