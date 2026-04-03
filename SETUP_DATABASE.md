# 🚀 Guia de Setup do Banco de Dados - PostgreSQL SaaS

Este documento descreve como configurar e usar o banco de dados PostgreSQL com SQLAlchemy para o Nutri SaaS.

## 📋 Quick Start (5 minutos)

### 1. Copiar e Configurar Environment

```bash
# Copie o arquivo de exemplo
cp .env.local .env

# Edite .env com suas credenciais PostgreSQL
# IMPORTANTE: Mude a senha "postgres" por uma senha segura
```

### 2. Verificar PostgreSQL

```bash
# macOS - Verificar se está rodando
brew services list | grep postgresql

# Se não estiver rodando, inicie
brew services start postgresql@15

# Teste conexão
psql -U postgres -c "SELECT 1"
```

### 3. Setup Automático

```bash
# Ativar virtual environment
source .venv/bin/activate

# Setup completo (cria banco, tabelas, migrations)
python scripts/db_manager.py init

# Verificar que funcionou
python scripts/db_manager.py check
```

### 4. Iniciar Aplicação

```bash
python main.py
```

Acesse: http://localhost:8000/api/docs

---

## 🔧 Configuração Detalhada

### Estrutura de Arquivos Importante

```
nutri_saas/
├── core/
│   ├── config.py              # Settings com DATABASE_URL ou componentes
│   ├── database.py            # Engine, SessionLocal, get_db()
│   ├── db_utils.py            # Utilitários de banco
│   └── dependencies.py        # Injeção de dependências
│
├── models/
│   ├── base.py               # Base declarativa + BaseModel
│   └── user_example.py       # Exemplo de modelo
│
├── alembic/                   # Migrations
│   ├── env.py                # Configuração Alembic
│   └── versions/             # Histórico de migrations
│
├── scripts/
│   ├── db_manager.py         # CLI de gerenciamento
│   └── db_setup.sh           # Script bash (legacy)
│
├── .env                       # Variáveis de ambiente
├── .env.example              # Template
├── .env.local                # Template local
└── DATABASE.md               # Esta documentação
```

### Configuração via .env

**Opção 1: URL Completa (Recomendado)**
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/nutri_saas
```

**Opção 2: Componentes**
```
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=senha_segura
DB_NAME=nutri_saas
DB_DRIVER=psycopg2
```

### Pool de Conexões para Escala

Para diferentes volumes de usuários:

```bash
# Pequeno (até 10 usuários simultâneos)
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Médio (10-50 usuários)
DB_POOL_SIZE=25
DB_MAX_OVERFLOW=50

# Grande (50-100 usuários)
DB_POOL_SIZE=50
DB_MAX_OVERFLOW=100

# Enterprise (100+ usuários)
DB_POOL_SIZE=100+
DB_MAX_OVERFLOW=200+
```

---

## 💻 Usando em Rotas

### Pattern 1: Dependency Injection (Recommended)

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import get_db

app = FastAPI()

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    from models.user_example import User
    return db.query(User).all()

@app.post("/users/")
def create_user(name: str, db: Session = Depends(get_db)):
    from models.user_example import User
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### Pattern 2: Service Layer

```python
# services/user_service.py
from sqlalchemy.orm import Session
from models.user_example import User

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, name: str):
        user = User(name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all(self):
        return self.db.query(User).all()

# routes/users.py
from fastapi import APIRouter, Depends
from core.database import get_db
from services.user_service import UserService

router = APIRouter()

@router.get("/users/")
def list_users(db: Session = Depends(get_db)):
    service = UserService(db=db)
    return service.get_all()
```

### Pattern 3: Transactions com Context Manager

```python
from core.db_utils import DBTransaction
from core.database import SessionLocal

db = SessionLocal()

try:
    with DBTransaction(db):
        # Seu código aqui
        # Commit automático ao sair
        # Rollback automático se houver erro
        pass
except Exception as e:
    print(f"Erro: {e}")
```

### Pattern 4: Bulk Operations

```python
from core.db_utils import DBBulkOperations
from core.database import SessionLocal
from models.user_example import User

db = SessionLocal()

# Inserir 1000 usuários em lotes de 500
users = [User(name=f"User {i}") for i in range(1000)]
total = DBBulkOperations.bulk_insert(db, users, batch_size=500)
print(f"Inseridos: {total} usuários")
```

---

## 🔄 Gerenciamento de Migrations

### Criar Nova Migration

```bash
# Automática (detecta mudanças nos modelos)
alembic revision --autogenerate -m "Adiciona tabela de pedidos"

# Manual (para migrações complexas)
alembic revision -m "Setup inicial"
```

### Aplicar Migrations

```bash
# Atualizar para a versão mais recente
alembic upgrade head

# Atualizar para uma versão específica
alembic upgrade abc123def456

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

# Ver detalhes de uma versão
alembic show abc123def456
```

---

## 🛠️ Ferramentas CLI

### python scripts/db_manager.py

```bash
# Verificar saúde do banco
python scripts/db_manager.py check

# Setup completo (criar banco, tabelas, migrations)
python scripts/db_manager.py init

# Setup sem aplicar migrations
python scripts/db_manager.py init --skip-migrations

# Resetar banco (CUIDADO: deleta todos os dados!)
python scripts/db_manager.py reset

# Popular com dados de exemplo
python scripts/db_manager.py seed
```

---

## 🧪 Testes

### Testar Configuração Completa

```bash
python test_database.py

# Saída esperada:
# ✅ test_imports
# ✅ test_config
# ✅ test_engine
# ✅ test_session
# ✅ test_models
# ✅ test_db_utils
# 6/6 testes passaram
```

---

## 🚨 Troubleshooting

### PostgreSQL não inicia

```bash
# Verificar status
brew services list

# Iniciar
brew services start postgresql@15

# Verificar logs
brew services log postgresql@15

# Testar conexão
psql -U postgres -c "SELECT 1"
```

### Erro: "database does not exist"

```bash
# Criar manualmente
psql -U postgres -c "CREATE DATABASE nutri_saas;"

# Ou automático
python scripts/db_manager.py init
```

### Erro: "connection refused"

```bash
# Verifique se PostgreSQL está rodando
ps aux | grep postgres

# Verifique .env (especialmente DB_HOST e DB_PORT)
cat .env

# Teste conexão
psql -h localhost -U postgres -c "SELECT 1"
```

### Erro: "pool exhausted"

Aumentar pool em `.env`:
```
DB_POOL_SIZE=25
DB_MAX_OVERFLOW=50
```

### Erro: "stale connection"

Já está resolvido com pool_pre_ping=True e pool_recycle=3600

---

## 📊 Monitoramento

### Verificar Saúde da Conexão

```python
from core.db_utils import DBHealthCheck
from core.database import SessionLocal

db = SessionLocal()
if DBHealthCheck.check_connection(db):
    print("✅ Banco saudável")
```

### Inspeccionar Schema

```python
from core.db_utils import DBSchema
from core.database import SessionLocal

db = SessionLocal()

# Ver colunas
columns = DBSchema.get_table_columns(db, User)
print(columns)

# Ver todas as tabelas
tables = DBSchema.get_all_tables(db)
print(tables)
```

### Ver Logs SQL

Em `.env`, defina:
```
DB_ECHO=True    # Mostra todas as queries SQL
DEBUG=True
```

---

## 🎯 Próximos Passos

1. ✅ Configurar `.env` com credenciais PostgreSQL
2. ✅ Executar `python scripts/db_manager.py init`
3. ✅ Executar `python test_database.py` para validar
4. ✅ Criar primeiros modelos em `models/`
5. ✅ Criar migrations: `alembic revision --autogenerate -m "Desc."`
6. ✅ Aplicar migrations: `alembic upgrade head`
7. ✅ Implementar rotas em `api/routes/`
8. ✅ Testar em http://localhost:8000/api/docs

---

## 📚 Referências

- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [FastAPI + Databases](https://fastapi.tiangolo.com/advanced/sql-databases/)
- [psycopg2 Docs](https://www.psycopg.org/)

---

**Criado em:** 2 de abril de 2026
**Versão:** 1.0
**Contato:** Seu Email Aqui
