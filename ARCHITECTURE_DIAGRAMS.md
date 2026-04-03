# Diagrama de Arquitetura - Visual Reference

## 🏗️ Arquitetura Geral do Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            CLIENT LAYER                                  │
│  (Web Browser, Mobile App, Desktop Client, Third-party Integrations)    │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   │ HTTP/HTTPS
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY LAYER                              │
│  (CORS, Rate Limiting, Request Validation, Load Balancing)             │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FASTAPI APPLICATION                               │
│                     (Dependency Injection, Routing)                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  @app.post("/nutricionistas/{id}/clientes")                      │  │
│  │  @app.get("/nutricionistas/{id}/clientes")                       │  │
│  │  @app.patch("/nutricionistas/{id}/clientes/{id}")                │  │
│  │  ... (5 endpoints for cliente)                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          SERVICE LAYER                                   │
│  (Business Logic, Authorization, Transaction Management)                │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ class BaseService[T, SchemaT]:                                 │    │
│  │   - get_by_id()                                                │    │
│  │   - get_all()                                                  │    │
│  │   - create()                                                   │    │
│  │   - update()                                                   │    │
│  │   - delete()                                                   │    │
│  │   - get_count()                                                │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                            ▲                                             │
│                            │ extends                                     │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ class ClienteService(BaseService[Cliente, ClienteCreate]):    │    │
│  │   + get_by_nutricionista()                                     │    │
│  │   + count_by_nutricionista()                                   │    │
│  │   + create_cliente()          [validates nutricionista]        │    │
│  │   + update_cliente()          [exclude_unset for partial]      │    │
│  │   + delete_cliente()          [cascade on relationships]       │    │
│  │   + get_cliente_por_nutricionista() [AUTHORIZATION]           │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     PYDANTIC VALIDATION LAYER                            │
│  (Request Validation, Response Serialization)                           │
│  ┌─────────────────────┐  ┌──────────────────────┐  ┌────────────────┐ │
│  │ ClienteCreate       │  │ ClienteUpdate        │  │ ClienteResponse│ │
│  │ - nome: str         │  │ - nome?: str         │  │ - id: int      │ │
│  │ - idade: int        │  │ - idade?: int        │  │ - nome: str    │ │
│  │   (0-150)           │  │   (0-150)            │  │ - created_at   │ │
│  │ - altura: float     │  │ - altura?: float     │  │ - updated_at   │ │
│  │   (0-300)           │  │   (0-300)            │  │ - ...          │ │
│  └─────────────────────┘  └──────────────────────┘  └────────────────┘ │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     SQLALCHEMY ORM LAYER                                 │
│  (Object-Relational Mapping, Query Building)                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ class Cliente(Base):                                           │    │
│  │   __tablename__ = "clientes"                                   │    │
│  │   id: Mapped[int] = mapped_column(primary_key=True)           │    │
│  │   nutricionista_id: Mapped[int] = mapped_column(ForeignKey()) │    │
│  │   nome: Mapped[str]                                            │    │
│  │   idade: Mapped[int]                                           │    │
│  │   altura: Mapped[float]                                        │    │
│  │   ...                                                          │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATABASE CONNECTION LAYER                             │
│  (Connection Pooling, Pre-ping Validation, ACID Transactions)           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ QueuePool(max_overflow=10, pool_size=20, pool_pre_ping=True)  │    │
│  │   - Maintains 20 persistent connections                        │    │
│  │   - Grows by 10 connections under high load                    │    │
│  │   - Verifies connection health before each operation           │    │
│  │   - Auto-reconnects on connection loss                         │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                                       │
│  PostgreSQL (Production) / SQLite (Development)                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ Database: nutricionistas_saas                                  │    │
│  │ ┌──────────────────────────────────────────────────────────┐   │    │
│  │ │ clientes                         medicoes                │   │    │
│  │ │ - id (PK)          ┌────────────>│ - id (PK)            │   │    │
│  │ │ - nutricionista_id (FK)          │ - cliente_id (FK) ──┘   │    │
│  │ │ - nome                           │ - peso                   │    │
│  │ │ - idade                          │ - data_medicao           │    │
│  │ │ - altura                         │                         │    │
│  │ │ - created_at                     │ observacoes             │    │
│  │ │ - updated_at            ┌───────>│ - id (PK)               │    │
│  │ │                         │        │ - cliente_id (FK) ──┐   │    │
│  │ │ nutricionistas          │        │ - texto              │   │    │
│  │ │ - id (PK)              │        │ - data               │   │    │
│  │ │ - nome                  │        │                     │   │    │
│  │ │ - email                 │        │ documentos          │   │    │
│  │ │ - created_at           └────────>│ - id (PK)            │   │    │
│  │ │ - updated_at                    │ - cliente_id (FK)    │   │    │
│  │ └──────────────────────────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Requisição - Cliente POST (Criar)

```
1. REQUEST (HTTP)
   ├─ Method: POST
   ├─ Path: /nutricionistas/1/clientes
   ├─ Headers: Content-Type: application/json
   └─ Body: {
      "nutricionista_id": 1,
      "nome": "João Silva",
      "idade": 30,
      "altura": 180.5,
      "objetivo": "Perda de peso"
    }

2. FASTAPI ROUTE LAYER
   ├─ Match route: @router.post("")
   ├─ Extract params: nutricionista_id=1
   ├─ Dependency inject: Depends(get_db)
   │  └─ Creates Session with connection from pool
   └─ Parse request body with Pydantic
      └─ Validation:
         ├─ idade: 0 <= 30 <= 150 ✅
         ├─ altura: 0 <= 180.5 <= 300 ✅
         └─ nome: str, not empty ✅

3. SERVICE LAYER
   ├─ Call: service.create_cliente(nutricionista_id, cliente_data)
   ├─ Business logic:
   │  ├─ Verify nutricionista exists ✅
   │  ├─ Validate request data
   │  ├─ Prepare database row
   │  └─ Handle errors
   └─ Return: Cliente object (ORM instance)

4. SQLALCHEMY ORM LAYER
   ├─ Create instance: Cliente(nome="João...", ...)
   ├─ Add to session: session.add(cliente)
   ├─ Build SQL: INSERT INTO clientes (nutricionista_id, nome, ...) VALUES (...)
   ├─ Commit transaction: session.commit()
   ├─ Refresh with ID: session.refresh(cliente)
   └─ Return: Cliente with id=100

5. PYDANTIC SERIALIZATION
   ├─ Convert ORM object to dict
   ├─ ClienteResponse.from_orm(cliente)
   ├─ Serialize to JSON:
   │  {
   │    "id": 100,
   │    "nutricionista_id": 1,
   │    "nome": "João Silva",
   │    "idade": 30,
   │    "altura": 180.5,
   │    "objetivo": "Perda de peso",
   │    "created_at": "2024-01-15T10:30:45",
   │    "updated_at": "2024-01-15T10:30:45"
   │  }
   └─ Status code: 201 Created

6. HTTP RESPONSE
   ├─ Status: 201 Created
   ├─ Headers: Content-Type: application/json
   └─ Body: {JSON from step 5}

7. CLIENT RECEIVES
   └─ Success! New cliente with id=100
```

---

## 🔐 Authorization Pattern

```
┌────────────────────────────────────────────────────┐
│ REQUEST TO PROTECTED ENDPOINT                       │
│ GET /nutricionistas/5/clientes/100                 │
│ (Verify that cliente 100 belongs to nutri 5)      │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│ FASTAPI ROUTE HANDLER                               │
│ extract: nutricionista_id=5, cliente_id=100       │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│ SERVICE AUTHORIZATION CHECK                         │
│ get_cliente_por_nutricionista(100, 5)             │
│                                                     │
│ WITH clientes AS c:                                │
│   WHERE c.id = 100                                │
│   AND c.nutricionista_id = 5                      │
└────────────┬─────────────────────────────────────────┘
             │
             ├─ Result found ───> Return cliente ──> 200 OK
             │
             └─ Result NOT found ──> Raise 404 ──> 404 Not Found

WHY 404 NOT 403?
  - Prevents information leakage
  - Client either doesn't exist OR doesn't belong
  - Attack can't enumrate: which cliente IDs exist?
  - Better security posture
```

---

## 📊 Database Schema

```
┌────────────────────────────────────────────────────────────────┐
│ TABLE: nutricionistas                                           │
├────────────────────────────────────────────────────────────────┤
│ id (PK)                               INT AUTO_INCREMENT        │
│ nome                                  VARCHAR(255) NOT NULL    │
│ email                                 VARCHAR(255) UNIQUE      │
│ senha                                 VARCHAR(255)             │
│ crm                                   VARCHAR(50)              │
│ especialidade                         VARCHAR(255)             │
│ created_at                            TIMESTAMP DEFAULT NOW    │
│ updated_at                            TIMESTAMP DEFAULT NOW    │
│                                                                  │
│ INDEXES:                                                        │
│ - PRIMARY KEY (id)                                             │
│ - UNIQUE (email)                                               │
└────────────────────────────────────────────────────────────────┘
                          │
                          │ 1:N
                          ▼
┌────────────────────────────────────────────────────────────────┐
│ TABLE: clientes                                                 │
├────────────────────────────────────────────────────────────────┤
│ id (PK)                               INT AUTO_INCREMENT        │
│ nutricionista_id (FK)                 INT → nutricionistas.id  │
│ nome                                  VARCHAR(255) NOT NULL    │
│ idade                                 INT (0-150)              │
│ altura                                FLOAT (0-300)            │
│ peso                                  FLOAT                    │
│ objetivo                              VARCHAR(255)             │
│ notas                                 TEXT                     │
│ created_at                            TIMESTAMP                │
│ updated_at                            TIMESTAMP                │
│                                                                  │
│ INDEXES:                                                        │
│ - PRIMARY KEY (id)                                             │
│ - FOREIGN KEY (nutricionista_id)                               │
│   CASCADE DELETE                                               │
│ - INDEX (nutricionista_id) [for queries by owner]             │
│ - INDEX (created_at) [for date range queries]                 │
└────────────────────────────────────────────────────────────────┘
                          │
         ┌────────┬───────┼───────┬────────┐
         │        │       │       │        │
         │ 1:N    │ 1:N   │ 1:N   │ 1:N    │
         ▼        ▼       ▼       ▼        ▼
    ┌────────┐ ┌────────────┐ ┌──────────┐
    │medicoes│ │observacoes │ │documentos│
    │        │ │            │ │          │
    └────────┘ └────────────┘ └──────────┘

CASCADE DELETE:
  DELETE FROM clientes WHERE id = 100
  ├─ DELETE FROM medicoes WHERE cliente_id = 100
  ├─ DELETE FROM observacoes WHERE cliente_id = 100
  └─ DELETE FROM documentos WHERE cliente_id = 100
```

---

## 🗂️ Project Structure with Types

```
nutri_saas/
│
├── Models Layer (SQL→ORM)
│   ├── ORM Models ────────────────> Database Tables
│   │   ├── class Nutricionista
│   │   ├── class Cliente
│   │   └── relationships: ForeignKey, relationships()
│   │
│   └── Base Timestamp Tracking
│       ├── id: Mapped[int]
│       ├── created_at: Mapped[datetime]
│       └── updated_at: Mapped[datetime]
│
├── Schema Layer (Request/Response)
│   ├── Request Validation (Pydantic)
│   │   ├── ClienteCreate (POST body)
│   │   └── ClienteUpdate (PATCH body)
│   │
│   └── Response Serialization (JSON)
│       ├── ClienteResponse
│       └── ClienteDetailResponse
│
├── Service Layer (Business Logic)
│   ├── BaseService[T, SchemaT]
│   │   ├── generic get_by_id(id: int) → T
│   │   ├── generic get_all(skip, limit) → List[T]
│   │   ├── generic create(data: SchemaT) → T
│   │   ├── generic update(id, data) → T | None
│   │   ├── generic delete(id) → bool
│   │   └── generic get_count() → int
│   │
│   └── ClienteService extends BaseService
│       ├── get_by_nutricionista(nut_id, skip, limit)
│       ├── count_by_nutricionista(nut_id)
│       ├── create_cliente(nut_id, data) [validate]
│       ├── update_cliente(id, data) [partial]
│       ├── delete_cliente(id) [cascade]
│       └── get_cliente_por_nutricionista(id, nut_id) [AUTH]
│
└── Route Layer (HTTP Endpoints)
    ├── POST /nutricionistas/{id}/clientes
    │   ├─ Validate URL params
    │   ├─ Parse request body
    │   ├─ Call service.create_cliente()
    │   ├─ Serialize response
    │   └─ Return 201 Created
    │
    ├── GET /nutricionistas/{id}/clientes
    │   ├─ Parse query params (skip, limit)
    │   ├─ Call service.get_by_nutricionista()
    │   ├─ Serialize list
    │   └─ Return 200 OK
    │
    ├── GET /nutricionistas/{id}/clientes/{id}
    │   ├─ AUTH: verify ownership
    │   ├─ Get client details
    │   ├─ Compute stats
    │   └─ Return 200 OK or 404
    │
    ├── PATCH /nutricionistas/{id}/clientes/{id}
    │   ├─ AUTH: verify ownership
    │   ├─ Parse partial body
    │   ├─ Call service.update_cliente()
    │   ├─ Serialize response
    │   └─ Return 200 OK
    │
    └── DELETE /nutricionistas/{id}/clientes/{id}
        ├─ AUTH: verify ownership
        ├─ Call service.delete_cliente()
        ├─ (cascade deletes triggered)
        └─ Return 204 No Content
```

---

## 🔄 Data Flow: Full Cycle

```
INCOMING REQUEST
       │
       ▼
    ┌─────────────────────┐
    │ FastAPI Route       │ ← Receives HTTP request
    │ @router.post("")    │   Extracts params, parses body
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Pydantic Schema     │ ← Validates request data
    │ ClienteCreate       │   Converts to Python object
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Service Layer       │ ← Business logic
    │ ClienteService      │   Authorization checks
    │ .create_cliente()   │   Validation rules
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ SQLAlchemy ORM      │ ← Object mapped to table
    │ Cliente(...)        │   Builds SQL INSERT
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Connection Pool     │ ← Acquires DB connection
    │ Pool.getconn()      │   Pre-ping validation
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ PostgreSQL/SQLite   │ ← Executes INSERT
    │ INSERT INTO clientes│   Commits transaction
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ SQLAlchemy Refresh  │ ← Gets generated ID
    │ session.refresh()   │   Loads timestamps
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Pydantic Response   │ ← Converts ORM to JSON
    │ ClienteResponse     │   from_orm(cliente)
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ JSON Serialization  │ ← Converts to string
    │ json.dumps()        │   Sets content-type
    └────────┬────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ HTTP Response       │ ← Returns to client
    │ 201 Created         │   With JSON body
    └────────┬────────────┘
             │
             ▼
  CLIENT RECEIVES DATA
         │
         └─ Parse JSON
            Process response
            Update UI
```

---

## 📈 Performance Considerations

```
┌─────────────────────────────────────────────────────────────┐
│ OPTIMIZATION ARCHITECTURE                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. CONNECTION POOLING                                       │
│    ├─ Pool Size: 20 connections                            │
│    ├─ Max Overflow: 10 connections                         │
│    ├─ Pre-ping: Health check every request                 │
│    └─ Result: No connection exhaustion, fast reconnect     │
│                                                              │
│ 2. QUERY OPTIMIZATION                                        │
│    ├─ Offset/Limit for pagination                          │
│    ├─ Indexed columns: nutricionista_id, created_at        │
│    ├─ Select only needed fields                            │
│    └─ Result: O(log n) query performance                   │
│                                                              │
│ 3. CACHING STRATEGY (Future)                                │
│    ├─ Cache common queries (Redis)                         │
│    ├─ Invalidate on updates                                │
│    ├─ ETag support for conditional requests                │
│    └─ Result: Reduced database load                        │
│                                                              │
│ 4. ASYNC SUPPORT (Ready)                                    │
│    ├─ async def route handlers                             │
│    ├─ Can handle multiple concurrent requests              │
│    ├─ Non-blocking I/O                                     │
│    └─ Result: Better concurrency                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

Última atualização: 2024-01-15
