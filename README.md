# Nutri SaaS - Backend API

Backend moderno e escalável de um sistema SaaS para gerenciamento nutricional construído com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

## 🚀 Início Rápido

```bash
# 1. Clonar e configurar
git clone <seu-repo>Endpoints e rotas
│   ├── routes/            # Módulos de rotas
│   │   ├── health.py      # Health check
│   │   └── ...
│   └── __init__.py
├── core/                  # Configuração centralizada
│   ├── config.py         # Variáveis de ambiente
│   ├── constants.py      # Constantes
│   ├── database.py       # SQLAlchemy + SessionLocal
│   ├── dependencies.py   # Injeção de dependências
│   └── __init__.py
├── models/               # Modelos SQLAlchemy
│   ├── base.py          # BaseModel com timestamps
│   └── __init__.py
├── schemas/             # Validação com Pydantic
│   ├── base.py          # Schemas base
│   └── __init__.py
├── services/            # Lógica de negócio
│   ├── base.py          # BaseService genérico
│   └── __init__.py
├── alembic/             # Database migrations
│   ├── env.py
│   ├── versions/        # Histórico de migrations
│   └── templates/
├── scripts/             # Scripts utilitários
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências
├── .env                 # Variáveis (desenvolvimento)
├── .env.example         # Template
├── alembic.ini          # Configuração Alembic
├── DATABASE.md          # Guia de banco 📖
├── ARCHITECTURE.md      # Arquitetura 🏗️
└── SETUP.md            # Setup & Deploy 🚀mpleto de instalação e configuração
- [**DATABASE.md**](DATABASE.md) - Configuração de banco de dados e migrations
- [**ARCHITECTURE.md**](ARCHITECTURE.md) - Arquitetura e padrões do projeto

## 📋 Estrutura do Projeto

```
nutri-saas/
├── api/                    # Rotas e endpoints
│   ├── routes/            # Módulos de rotas
│   │   ├── health.py      # Verificação de saúde
│   │   └── ...
│   └── __init__.py
├── core/                  # Configurações centrais
│   ├── config.py         # Variáveis de ambiente
│   ├── constants.py      # Constantes da aplicação
│   └── __init__.py
├── models/               # Modelos SQLAlchemy
│   ├── base.py          # Classe base para modelos
│   └── __init__.py
├── schemas/             # Schemas Pydantic
│  🎯 Stack Tecnológico

- **Framework**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23
- **Banco de Dados**: PostgreSQL / SQLite
- **Migrations**: Alembic
- **Validação**: Pydantic v2
- **Server**: Uvicorn
- **Python**: 3.11+
# Edite .env com suas configurações
```

5. Execute a aplicação:
```bash
python main.py
# ou
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/openapi.json`

## 🏗️ Arquitetura

### Módulos

- **api**: Contém todas as rotas e endpoints da API
- **core**: Configurações, constantes e utilidades centralizadas
- **models**: Definições dos modelos de banco de dados
- **schemas**: Validações e serialização de dados com Pydantic
- **services**: Lógica de negócio, separada das rotas

### Fluxo de Requisição

```� Documentação

- **Swagger UI**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **ReDoc**: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)
- **OpenAPI Schema**: [http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

## 🔧 Configuração

Edite o arquivo `.env` para configurar:

- `DATABASE_URL`: URL de conexão com o banco de dados
- `SECRET_KEY`: Chave secreta para JWT (mude em produção)
- `DEBUG`: Modo debug (desabilite em produção)
- `ALLOWED_ORIGINS`: Origens permitidas para CORS

## 📝 Adicionar Novas Rotas

1. Crie um novo arquivo em `api/routes/`:
```python
```
HTTP Request
    ↓
API Routes (api/routes/)
    ↓
Schema Validation (schemas/)
    ↓
Services (services/) - Lógica de Negócio
    ↓
Models (models/) - SQLAlchemy ORM
    ↓
Database (PostgreSQL/SQLite)
```

**Para detalhes completos, veja [ARCHITECTURE.md](ARCHITECTURE.md)**
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(BaseModel):
    __tablename__ = "users"
    
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

2. Crie o schema correspondente em `schemas/`
3. Use nos services para lógica de negócio

## 🧪 Testes

```bash
pytest
```

## 🚀 Deploy

Para produção:
1. Mude `DEBUG=False` em `.env`
2. Configure `SECRET_KEY` com um valor seguro
3. Configure o banco de dados produção
4. Use um gerenciador de processos (Gunicorn, Supervisor)

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 📄 Licença

MIT

## 👥 Autor

Seu Nome

---

**Status**: 🟡 Em Desenvolvimento
♻️ Database Migrations

```bash
# Criar nova migration
alembic revision --autogenerate -m "Add users table"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history

# Usar script helper (Unix/macOS)
chmod +x scripts/migrations.sh
./scripts/migrations.sh help
```

**Mais detalhes em [DATABASE.md](DATABASE.md)**