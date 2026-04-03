# 🏗️ Arquitetura do Backend

## Fluxo de Requisição

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP REQUEST                              │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Application (main.py)                   │
│  ├─ CORSMiddleware                                           │
│  └─ Request Routing                                          │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           API Routes (api/routes/*)                          │
│  ├─ GET /users      → Router Handler                         │
│  ├─ POST /users     → Router Handler                         │
│  └─ DELETE /users   → Router Handler                         │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│      Schema Validation (schemas/*)                           │
│  ├─ Pydantic BaseModel                                       │
│  ├─ Type checking                                            │
│  └─ Error handling                                           │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│      Business Logic (services/*)                             │
│  ├─ UserService                                              │
│  ├─ ProdutoService                                           │
│  └─ CustomLogic                                              │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│      Database Operations (models/*)                          │
│  ├─ SQLAlchemy ORM                                           │
│  ├─ Query building                                           │
│  └─ Relationships                                            │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           Database Layer (core/database.py)                  │
│  ├─ SQLAlchemy Engine                                        │
│  ├─ SessionLocal                                             │
│  └─ Connection Pool                                          │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│     PostgreSQL / SQLite                                      │
│  └─ Persistent Data Storage                                  │
└─────────────────────────────────────────────────────────────┘
```

## Estrutura de Diretórios

```
nutri-saas/
│
├── api/                          # Camada de Apresentação
│   └── routes/
│       ├── __init__.py
│       ├── health.py            # Health check
│       ├── users.py             # Endpoints de usuário
│       ├── produtos.py          # Endpoints de produto
│       └── ...
│
├── services/                     # Camada de Lógica de Negócio
│   ├── __init__.py
│   ├── base.py                  # BaseService genérico
│   ├── user_service.py          # Lógica de usuário
│   ├── produto_service.py       # Lógica de produto
│   └── ...
│
├── models/                       # Camada de Dados (ORM)
│   ├── __init__.py
│   ├── base.py                  # BaseModel com timestamps
│   ├── user.py                  # Modelo User
│   ├── produto.py               # Modelo Produto
│   └── ...
│
├── schemas/                      # Validação de Dados
│   ├── __init__.py
│   ├── base.py                  # Schemas base (paginação, erro)
│   ├── user.py                  # UserCreate, UserResponse
│   ├── produto.py               # ProdutoCreate, ProdutoResponse
│   └── ...
│
├── core/                         # Configuração Central
│   ├── __init__.py
│   ├── config.py                # Settings (variáveis de ambiente)
│   ├── constants.py             # Constantes da aplicação
│   ├── database.py              # Conexão SQLAlchemy
│   └── dependencies.py          # Injeção de dependências
│
├── alembic/                      # Database Migrations
│   ├── env.py                   # Configuração Alembic
│   ├── versions/                # Histórico de migrations
│   └── templates/               # Templates de migration
│
├── scripts/                      # Scripts Utilitários
│   ├── migrations.sh            # Helper de migrations
│   └── README.md
│
├── main.py                       # Aplicação Principal
├── requirements.txt             # Dependências Python
├── .env                         # Variáveis de ambiente (development)
├── .env.example                 # Template de .env
├── alembic.ini                  # Configuração de migrations
├── DATABASE.md                  # Documentação de banco
├── README.md                    # Documentação geral
└── .gitignore
```

## Camadas da Arquitetura

### 1️⃣ API Layer (Presentation)
- **Responsabilidade**: Receber requisições HTTP, validar entrada, retornar respostas
- **Localização**: `api/routes/`
- **Exemplo**:
  ```python
  @router.post("/users")
  async def create_user(user: UserCreate, db: Session = Depends(get_db)):
      service = UserService(db)
      return service.create_user(user)
  ```

### 2️⃣ Schema Layer (Validation)
- **Responsabilidade**: Validar dados com Pydantic, serialização
- **Localização**: `schemas/`
- **Exemplo**:
  ```python
  class UserCreate(BaseModel):
      email: EmailStr
      name: str = Field(..., min_length=1)
  ```

### 3️⃣ Service Layer (Business Logic)
- **Responsabilidade**: Implementar regras de negócio, lógica complexa
- **Localização**: `services/`
- **Exemplo**:
  ```python
  class UserService(BaseService):
      def create_user(self, user: UserCreate):
          if self.get_by_email(user.email):
              raise ValueError("Email já registrado")
          return self.create(user)
  ```

### 4️⃣ Model Layer (Data Access)
- **Responsabilidade**: Definir estrutura de dados, relacionamentos
- **Localização**: `models/`
- **Exemplo**:
  ```python
  class User(BaseModel):
      __tablename__ = "users"
      email: Mapped[str] = mapped_column(String(255), unique=True)
  ```

### 5️⃣ Database Layer (Persistence)
- **Responsabilidade**: Gerenciar conexões, sessions, pool
- **Localização**: `core/database.py`

## Padrões Utilizados

### ✅ Dependency Injection
```python
async def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_by_id(user_id)
```

### ✅ Generic Base Service
```python
class BaseService(Generic[T, SchemaT]):
    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(self.model).offset(skip).limit(limit).all()
```

### ✅ SQLAlchemy 2.0 Modern Syntax
```python
class User(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

### ✅ Pydantic v2
```python
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
```

## Fluxo de Dados: Exemplo Prático

### Criar um novo usuário:

```
1. POST /api/users
   └── Receive: {"email": "user@example.com", "name": "John"}

2. FastAPI receives request
   └── Calls create_user(user: UserCreate, db: Session)

3. Schema Validation (Pydantic)
   └── Validates email format, name length
   └── Returns: UserCreate(email=..., name=...)

4. Route Handler
   └── Instantiates UserService(db)
   └── Calls service.create_user(user)

5. Service Layer (Business Logic)
   └── Checks if email already exists
   └── Hashes password (se aplicável)
   └── Calls super().create(user)

6. Base Service
   └── Calls self.db.add(user)
   └── Calls self.db.commit()
   └── Calls self.db.refresh(user)

7. SQLAlchemy ORM
   └── Builds SQL: INSERT INTO users (email, name, ...)
   └── Sends to database driver

8. Database (PostgreSQL/SQLite)
   └── Executes query
   └── Returns new row with generated ID

9. Response
   └── Service returns User object
   └── Route converts to UserResponse schema
   └── FastAPI returns JSON: {"id": 1, "email": "...", ...}
```

## Configuração de Banco de Dados

### SQLite (Desenvolvimento)
- ✅ Sem setup externo
- ✅ Rápido para testes
- ❌ Não para produção
- 📝 `DATABASE_URL=sqlite:///./nutri_saas.db`

### PostgreSQL (Produção)
- ✅ Escalável
- ✅ ACID compliance
- ✅ Multi-usuário
- 📝 `DATABASE_URL=postgresql://user:pass@localhost/nutri_saas`

## Migrations com Alembic

```
├── alembic/
│   ├── env.py                    # Configuração
│   └── versions/
│       ├── 001_add_users.py
│       ├── 002_add_produtos.py
│       └── ...
```

### Workflow:

```bash
# 1. Criar modelo
vim models/user.py

# 2. Gerar migration automática
alembic revision --autogenerate -m "Add users table"

# 3. Aplicar
alembic upgrade head

# 4. Resultado: tabela criada no banco
```

## Boas Práticas

1. **Separação de Responsabilidades**
   - Rotas: apenas HTTP handling
   - Services: lógica de negócio
   - Models: apenas ORM definition

2. **Type Hints Rigorosos**
   - Melhora autocompletar
   - Previne bugs
   - Facilita manutenção

3. **Dependency Injection**
   - Testabilidade
   - Flexibilidade
   - Desacoplamento

4. **Validação em Camadas**
   - Pydantic (schema)
   - Database constraints
   - Service logic

5. **Logging & Monitoring**
   - Debug em desenvolvimento
   - Observabilidade em produção

## Próximos Passos

1. Criar modelos específicos do seu negócio
2. Implementar serviços com lógica de negócio
3. Criar rotas para cada entidade
4. Gerar migrations
5. Escrever testes

## Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
