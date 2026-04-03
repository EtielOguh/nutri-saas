# 🚀 Guia de Setup e Execução

## Pré-requisitos

- Python 3.11+
- pip ou poetry
- PostgreSQL (opcional, para produção)
- Git

## 1. Clonar e Configurar

```bash
# Clonar repositório
git clone <seu-repo>
cd nutri-saas

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

## 2. Configurar Banco de Dados

### Opção A: SQLite (Desenvolvimento)

```bash
# Arquivo .env está pronto
cat .env
# DATABASE_URL=sqlite:///./nutri_saas.db
```

### Opção B: PostgreSQL (Produção)

```bash
# Instalar PostgreSQL
brew install postgresql@15  # macOS
# ou
sudo apt-get install postgresql  # Linux

# Iniciar serviço
brew services start postgresql@15  # macOS

# Criar banco de dados
createdb nutri_saas

# Atualizar .env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost/nutri_saas
```

## 3. Aplicar Migrations

```bash
# Criar tabelas inicial
alembic upgrade head

# Se for primeira vez e não houver migrations
alembic revision --autogenerate -m "Initial setup"
alembic upgrade head
```

## 4. Executar a Aplicação

### Modo Desenvolvimento

```bash
# Com auto-reload
uvicorn main:app --reload

# Ou diretamente
python main.py
```

### Modo Produção

```bash
# Com Gunicorn (4 workers)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Ou com uvicorn explicitamente
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 5. Acessar a API

Abra seu navegador ou use `curl`:

```bash
# Health check
curl http://localhost:8000/health

# Swagger UI (documentação interativa)
open http://localhost:8000/api/docs

# ReDoc (documentação alternativa)
open http://localhost:8000/api/redoc

# OpenAPI Schema (JSON)
curl http://localhost:8000/api/openapi.json
```

## 6. Estrutura de Pastas

```
nutri-saas/
├── api/              # Rotas e endpoints
├── core/             # Configuração central
├── models/           # Modelos de banco
├── schemas/          # Validação com Pydantic
├── services/         # Lógica de negócio
├── alembic/          # Migrations
├── scripts/          # Scripts úteis
├── main.py           # App principal
├── requirements.txt  # Dependências
├── .env              # Variáveis de ambiente
├── DATABASE.md       # Guia de banco de dados
├── ARCHITECTURE.md   # Arquitetura do projeto
└── SETUP.md          # Este arquivo
```

## 7. Próximas Etapas

### ✅ Criar um novo modelo

1. Adicione em `models/seu_modelo.py`:
```python
from models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Produto(BaseModel):
    __tablename__ = "produtos"
    nome: Mapped[str] = mapped_column(String(255))
```

2. Crie schema em `schemas/seu_schema.py`:
```python
from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    nome: str
```

3. Adicione serviço em `services/seu_service.py`:
```python
from services.base import BaseService
from models.seu_modelo import Produto
from schemas.seu_schema import ProdutoCreate

class ProdutoService(BaseService[Produto, ProdutoCreate]):
    pass
```

4. Crie rota em `api/routes/seu_modelo.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.seu_service import ProdutoService
from schemas.seu_schema import ProdutoCreate

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/")
async def listar(db: Session = Depends(get_db)):
    return ProdutoService(db).get_all()
```

5. Inclua em `main.py`:
```python
from api.routes import seu_modelo
app.include_router(seu_modelo.router)
```

6. Crie migration:
```bash
alembic revision --autogenerate -m "Add produtos table"
alembic upgrade head
```

## 8. Comandos Úteis

```bash
# Instalar novo pacote
pip install novo-pacote
pip freeze > requirements.txt

# Limpar cache Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Executar testes (se houver)
pytest

# Verificar sintaxe
python -m py_compile main.py

# Formatar código
black .

# Lint
pylint api/

# Type checking
mypy main.py
```

## 9. Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
# Certifique-se de estar no venv
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "DATABASE_URL" não encontrado
```bash
# Crie .env com DATABASE_URL
cp .env.example .env
# Edite .env se necessário
```

### Erro: "Alembic migration conflicts"
```bash
# Verifique revisões
alembic heads

# Downgrade e retry
alembic downgrade -1
alembic revision --autogenerate -m "Fix"
alembic upgrade head
```

### Porta 8000 já em uso
```bash
# Encontre o processo
lsof -i :8000

# Ou use outra porta
uvicorn main:app --port 8001
```

## 10. Variáveis de Ambiente

### Desenvolvimento (.env)
```
DEBUG=True
DATABASE_URL=sqlite:///./nutri_saas.db
SECRET_KEY=dev-key-only
```

### Produção
```
DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-server/nutri_saas
SECRET_KEY=super-secret-production-key
ALLOWED_ORIGINS=["https://meioapp.com"]
```

## 11. Deploy

### Com Docker (opcional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t nutri-saas .
docker run -p 8000:8000 nutri-saas
```

### Com Railway, Render, Heroku, etc.
- Configure `.env` com banco PostgreSQL
- Deploy o repositório
- Migrations rodão automaticamente (configure webhook)

## 12. Referências

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)

---

**Dúvidas?** Consulte `DATABASE.md` e `ARCHITECTURE.md` para mais detalhes!
