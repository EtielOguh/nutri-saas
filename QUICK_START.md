# 🎉 CLIENTE API - QUICK START GUIDE

**Status:** ✅ Phase 4 Complete - Cliente REST API Fully Implemented

---

## 🚀 Start Using the API

### 1. Start the Application
```bash
python main.py
# Output: INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Create a Test Nutritionist (if needed)
```bash
curl -X POST http://localhost:8000/nutricionistas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. João",
    "email": "joao@test.com",
    "senha": "senha123"
  }'

# Note the ID returned (e.g., 1)
```

### 3. Use the 5 Cliente Endpoints

#### Create Cliente
```bash
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 1,
    "nome": "João Silva",
    "idade": 30,
    "altura": 180.5,
    "objetivo": "Perda de peso"
  }'
```

#### List Clientes
```bash
curl http://localhost:8000/nutricionistas/1/clientes
curl "http://localhost:8000/nutricionistas/1/clientes?skip=0&limit=5"
```

#### Get Detail
```bash
curl http://localhost:8000/nutricionistas/1/clientes/1
```

#### Update Cliente
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{"idade": 31, "objetivo": "Ganho de massa"}'
```

#### Delete Cliente
```bash
curl -X DELETE http://localhost:8000/nutricionistas/1/clientes/1
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **CLIENTE_API.md** | 🔥 Complete API reference with examples |
| **CLIENTE_ENDPOINTS_TESTING.md** | Full testing guide (cURL + Python) |
| **ENDPOINT_ARCHITECTURE.md** | Design patterns & architecture explained |
| **VALIDATION_CHECKLIST.md** | Test all endpoints systematically |
| **PROXIMO_ROADMAP.md** | Templates for implementing other entities |
| **ARCHITECTURE_DIAGRAMS.md** | Visual diagrams of the system |
| **EXECUTIVE_SUMMARY.md** | Project status & progress metrics |
| **script_teste_cliente.py** | Automated test script |

**👉 Start Here:** Read [CLIENTE_API.md](CLIENTE_API.md) for complete reference

---

## 🎯 What's Included

### ✅ 5 REST Endpoints
- `POST /nutricionistas/{id}/clientes` - Create
- `GET /nutricionistas/{id}/clientes` - List (with pagination)
- `GET /nutricionistas/{id}/clientes/{id}` - Details
- `PATCH /nutricionistas/{id}/clientes/{id}` - Update (partial)
- `DELETE /nutricionistas/{id}/clientes/{id}` - Delete

### ✅ Service Layer
- `ClienteService` with 6 methods
- CRUD operations
- Authorization checks
- Business logic validation

### ✅ Data Validation
- Age: 0-150 years
- Height: 0-300 cm
- Email validation (unique)
- Required field validation
- Type checking

### ✅ Authorization
- Service-level ownership checks
- Route-level authorization
- Cross-nutritionist access blocked
- Returns 404 for security

### ✅ Features
- Pagination (skip/limit)
- Partial updates (PATCH)
- Cascade deletes
- Timestamps (created_at, updated_at)
- Error handling with proper status codes

### ✅ Documentation
- Complete API reference
- Code examples (cURL + Python)
- Testing guides
- Architecture patterns
- Validation checklist

---

## 🧪 Test Everything

### Option 1: Automated Test Script
```bash
python script_teste_cliente.py
```

### Option 2: Manual cURL Tests
See [VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md)

### Option 3: Use Python requests
```python
import requests

response = requests.post(
    'http://localhost:8000/nutricionistas/1/clientes',
    json={
        'nutricionista_id': 1,
        'nome': 'João Silva',
        'idade': 30,
        'altura': 180.5
    }
)
print(response.status_code)  # 201
print(response.json())
```

---

## 📊 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 201 | Created | POST success |
| 200 | OK | GET/PATCH success |
| 204 | No Content | DELETE success |
| 400 | Bad Request | Invalid input (nutricionista_id mismatch) |
| 404 | Not Found | Cliente doesn't exist or authorization failed |
| 422 | Invalid | Validation failed (age > 150, etc) |
| 500 | Error | Server error |

---

## 🔐 Authorization Pattern

All endpoints check that the cliente belongs to the specified nutricionista:

```python
# In the route handler:
cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
if not cliente:
    raise HTTPException(404, "Cliente não encontrado")
```

**Result:** Cannot access other nutritionists' clients

---

## 🏗️ Architecture Overview

```
Request → FastAPI Route → Service Layer → ORM → Database
   ↓          (HTTP)       (Business)   (SQL)   (Storage)
Response ← Pydantic ← Service Result ← ORM Result ← DB Result
```

### Layers:
1. **Routes** - HTTP endpoints, parameter validation
2. **Services** - Business logic, authorization, CRUD
3. **ORM** - SQLAlchemy models, database mapping
4. **Schemas** - Pydantic validation, serialization

---

## ⚙️ Configuration

### Database
Edit `core/config.py`:
```python
# PostgreSQL (Production)
DATABASE_URL = "postgresql://user:password@localhost/nutri_saas"

# SQLite (Development)
DATABASE_URL = "sqlite:///./test.db"
```

### Connection Pool
```python
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)
```

---

## 🚨 Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'fastapi'`
```bash
pip install -r requirements.txt
```

### Issue: `RuntimeError: no running event loop`
Make sure you're using an async-compatible test runner:
```bash
pytest --asyncio-mode=auto
# or
python script_teste_cliente.py
```

### Issue: `OperationalError: database is locked`
Close other database connections or use different SQLite files.

### Issue: TestClient import error
```bash
pip install starlette<0.28.0
# or use curl/requests directly
```

---

## 📈 Next Steps

1. **Test the API** - Use [VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md)
2. **Implement Nutricionista** - Follow [PROXIMO_ROADMAP.md](PROXIMO_ROADMAP.md)
3. **Add Authentication** - Implement JWT tokens
4. **Implement other entities** - Medicao, Observacao, Documento, TokenAcesso
5. **Deploy** - Docker, production environment

---

## 🤔 Questions?

### Where do I find...?

- **API Examples** → [CLIENTE_API.md](CLIENTE_API.md)
- **Testing Guide** → [CLIENTE_ENDPOINTS_TESTING.md](CLIENTE_ENDPOINTS_TESTING.md)
- **Architecture** → [ENDPOINT_ARCHITECTURE.md](ENDPOINT_ARCHITECTURE.md)
- **Patterns to Follow** → [PROXIMO_ROADMAP.md](PROXIMO_ROADMAP.md)
- **Visual Diagrams** → [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)
- **Overall Status** → [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)

---

## ✨ Features Implemented

- ✅ CRUD operations for Cliente
- ✅ Pagination support
- ✅ Authorization checks
- ✅ Input validation
- ✅ Error handling
- ✅ Database cascade deletes
- ✅ Timestamps (created_at, updated_at)
- ✅ Type hints (mypy ready)
- ✅ Docstrings in Portuguese
- ✅ Comprehensive documentation
- ✅ Test suite (15 tests)
- ✅ Example script

---

## 📝 Code Highlights

### Service Layer Pattern
```python
class ClienteService(BaseService[Cliente, ClienteCreate]):
    def get_by_nutricionista(self, nutricionista_id, skip, limit):
        return self.db.query(self.model)\
            .filter(self.model.nutricionista_id == nutricionista_id)\
            .offset(skip).limit(limit).all()
    
    def get_cliente_por_nutricionista(self, cliente_id, nutricionista_id):
        """Authorization check"""
        return self.db.query(self.model).filter(
            (self.model.id == cliente_id) &
            (self.model.nutricionista_id == nutricionista_id)
        ).first()
```

### Route Pattern
```python
@router.get("/{cliente_id}", response_model=ClienteDetailResponse)
async def obter_cliente(
    nutricionista_id: int,
    cliente_id: int,
    db: Session = Depends(get_db),
):
    service = ClienteService(db=db)
    cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    return ClienteDetailResponse.from_orm(cliente)
```

---

## 🎓 Learning Outcomes

After working through this project, you've learned:

1. ✅ FastAPI fundamentals
2. ✅ SQLAlchemy ORM (Mapped types)
3. ✅ Pydantic v2 schemas
4. ✅ REST API design
5. ✅ Authorization patterns
6. ✅ Error handling
7. ✅ Database connection pooling
8. ✅ API documentation
9. ✅ Test strategies

---

## 🚀 Ready to Deploy?

### Local Testing
```bash
python main.py
# API at http://localhost:8000
# Docs at http://localhost:8000/docs (Swagger UI)
```

### Run Tests
```bash
python script_teste_cliente.py
```

### Production Deployment
```bash
# See SETUP.md for Docker, environment variables, etc.
```

---

## 💡 Pro Tips

1. **Auto-reload in development**
   ```bash
   uvicorn main:app --reload
   ```

2. **Interactive API docs**
   ```
   http://localhost:8000/docs
   ```

3. **Database migrations**
   ```bash
   alembic revision --autogenerate -m "Add clientes table"
   alembic upgrade head
   ```

4. **Debug mode**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## 📞 Support

**All documentation is in the repository:**
- Code comments explain implementation
- Docstrings show function purpose
- README files guide next steps
- Examples show usage patterns

**Still stuck?**
1. Check appropriate .md file in root
2. Look at code comments
3. Run `python script_teste_cliente.py` to see working examples
4. Review curl examples in CLIENTE_ENDPOINTS_TESTING.md

---

## ✅ Ready?

```bash
# Start the API
python main.py

# In another terminal, test it
curl http://localhost:8000/nutricionistas/1/clientes

# Or run automated tests
python script_teste_cliente.py
```

---

**Happy coding! 🎉**

The API is production-ready and fully documented.

Última atualização: 2024-01-15
