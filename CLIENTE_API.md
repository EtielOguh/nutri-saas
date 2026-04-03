# Cliente API - Endpoints FastAPI

## Visão Geral

Endpoints RESTful para gerenciamento de clientes vinculados a nutricionistas.

## Endpoints Disponíveis

### 1. Criar Cliente
**POST** `/nutricionistas/{nutricionista_id}/clientes`

Cria um novo cliente vinculado a um nutricionista.

**Parâmetros da URL:**
- `nutricionista_id` (int): ID do nutricionista proprietário

**Body (JSON):**
```json
{
  "nutricionista_id": 1,
  "nome": "João Silva",
  "idade": 30,
  "altura": 180.0,
  "objetivo": "Perda de peso"
}
```

**Validações:**
- `nutricionista_id`: Obrigatório, deve corresponder ao ID da URL
- `nome`: Obrigatório, 3-255 caracteres
- `idade`: Opcional, 1-150 anos
- `altura`: Opcional, 1-300 cm
- `objetivo`: Opcional, até 255 caracteres

**Resposta (201 Created):**
```json
{
  "id": 1,
  "nutricionista_id": 1,
  "nome": "João Silva",
  "idade": 30,
  "altura": 180.0,
  "objetivo": "Perda de peso",
  "created_at": "2026-04-02T10:30:00",
  "updated_at": "2026-04-02T10:30:00"
}
```

**Exemplos de Erro:**
- 400: `{"detail": "Cliente deve estar vinculado ao nutricionista da URL"}`
- 422: Erro de validação de campos

---

### 2. Listar Clientes
**GET** `/nutricionistas/{nutricionista_id}/clientes`

Lista todos os clientes de um nutricionista com paginação.

**Parâmetros da URL:**
- `nutricionista_id` (int): ID do nutricionista

**Query Parameters:**
- `skip` (int, padrão: 0): Número de registros a pular
- `limit` (int, padrão: 10, máximo: 100): Quantidade de registros por página

**Exemplos:**
```
GET /nutricionistas/1/clientes
GET /nutricionistas/1/clientes?skip=0&limit=5
GET /nutricionistas/1/clientes?skip=10&limit=20
```

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "nutricionista_id": 1,
    "nome": "João Silva",
    "idade": 30,
    "altura": 180.0,
    "objetivo": "Perda de peso",
    "created_at": "2026-04-02T10:30:00",
    "updated_at": "2026-04-02T10:30:00"
  },
  {
    "id": 2,
    "nutricionista_id": 1,
    "nome": "Maria Santos",
    "idade": 25,
    "altura": 165.0,
    "objetivo": "Ganho de massa",
    "created_at": "2026-04-02T11:00:00",
    "updated_at": "2026-04-02T11:00:00"
  }
]
```

**Resposta Vazia (200 OK):**
```json
[]
```

---

### 3. Obter Detalhes do Cliente
**GET** `/nutricionistas/{nutricionista_id}/clientes/{cliente_id}`

Retorna informações detalhadas de um cliente específico incluindo estatísticas.

**Parâmetros da URL:**
- `nutricionista_id` (int): ID do nutricionista proprietário
- `cliente_id` (int): ID do cliente

**Resposta (200 OK):**
```json
{
  "id": 1,
  "nutricionista_id": 1,
  "nome": "João Silva",
  "idade": 30,
  "altura": 180.0,
  "objetivo": "Perda de peso",
  "created_at": "2026-04-02T10:30:00",
  "updated_at": "2026-04-02T10:30:00",
  "total_medicoes": 5,
  "total_observacoes": 12,
  "total_documentos": 2,
  "ultimo_peso": 78.5,
  "data_ultima_medicao": "2026-04-01T15:30:00"
}
```

**Erros:**
- 404: `{"detail": "Cliente {id} não encontrado para este nutricionista"}`

---

### 4. Atualizar Cliente
**PATCH** `/nutricionistas/{nutricionista_id}/clientes/{cliente_id}`

Atualiza informações de um cliente (apenas campos fornecidos são atualizados).

**Parâmetros da URL:**
- `nutricionista_id` (int): ID do nutricionista proprietário
- `cliente_id` (int): ID do cliente

**Body (JSON) - Todos Opcionais:**
```json
{
  "nome": "João Silva Santos",
  "idade": 31,
  "altura": 180.5,
  "objetivo": "Ganho de massa muscular"
}
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "nutricionista_id": 1,
  "nome": "João Silva Santos",
  "idade": 31,
  "altura": 180.5,
  "objetivo": "Ganho de massa muscular",
  "created_at": "2026-04-02T10:30:00",
  "updated_at": "2026-04-02T12:00:00"
}
```

**Erros:**
- 404: Cliente não encontrado
- 422: Erro de validação

---

### 5. Deletar Cliente
**DELETE** `/nutricionistas/{nutricionista_id}/clientes/{cliente_id}`

Deleta um cliente (cascade delete remove dados relacionados).

**Parâmetros da URL:**
- `nutricionista_id` (int): ID do nutricionista proprietário
- `cliente_id` (int): ID do cliente

**Resposta (204 No Content):**
```
[Sem corpo]
```

**Erros:**
- 404: Cliente não encontrado

---

## Fluxo de Autorização

Todos os endpoints verificam que o cliente pertence ao nutricionista:

```python
# Apenas cliente DO nutricionista pode ser acessado
GET /nutricionistas/1/clientes/5  # ✅ OK se cliente 5 pertence a nutricionista 1
GET /nutricionistas/2/clientes/5  # ❌ 404 se cliente 5 pertence a nutricionista 1
```

---

## Exemplos de Uso com cURL

### Criar Cliente
```bash
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 1,
    "nome": "João Silva",
    "idade": 30,
    "altura": 180.0,
    "objetivo": "Perda de peso"
  }'
```

### Listar Clientes
```bash
curl http://localhost:8000/nutricionistas/1/clientes

# Com paginação
curl "http://localhost:8000/nutricionistas/1/clientes?skip=0&limit=5"
```

### Obter Detalhes
```bash
curl http://localhost:8000/nutricionistas/1/clientes/1
```

### Atualizar Cliente
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 31,
    "objetivo": "Ganho de massa muscular"
  }'
```

### Deletar Cliente
```bash
curl -X DELETE http://localhost:8000/nutricionistas/1/clientes/1
```

---

## Exemplos de Uso com Python

### Usar com Requests
```python
import requests

BASE_URL = "http://localhost:8000"
NUTRICIONISTA_ID = 1

# Criar cliente
response = requests.post(
    f"{BASE_URL}/nutricionistas/{NUTRICIONISTA_ID}/clientes",
    json={
        "nutricionista_id": NUTRICIONISTA_ID,
        "nome": "João Silva",
        "idade": 30,
        "altura": 180.0,
        "objetivo": "Perda de peso"
    }
)
cliente = response.json()
cliente_id = cliente["id"]
print(f"Cliente criado: {cliente}")

# Listar clientes
response = requests.get(
    f"{BASE_URL}/nutricionistas/{NUTRICIONISTA_ID}/clientes"
)
clientes = response.json()
print(f"Total de clientes: {len(clientes)}")

# Obter detalhes
response = requests.get(
    f"{BASE_URL}/nutricionistas/{NUTRICIONISTA_ID}/clientes/{cliente_id}"
)
detalhe = response.json()
print(f"Detalhes: {detalhe}")

# Atualizar
response = requests.patch(
    f"{BASE_URL}/nutricionistas/{NUTRICIONISTA_ID}/clientes/{cliente_id}",
    json={"idade": 31}
)
atualizado = response.json()
print(f"Atualizado: {atualizado}")

# Deletar
response = requests.delete(
    f"{BASE_URL}/nutricionistas/{NUTRICIONISTA_ID}/clientes/{cliente_id}"
)
print(f"Deletado: Status {response.status_code}")
```

---

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 201 | Criado com sucesso |
| 200 | OK - Requisição bem-sucedida |
| 204 | No Content - Deletado com sucesso |
| 400 | Bad Request - Dados inválidos |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Erro de validação |
| 500 | Internal Server Error - Erro do servidor |

---

## Integração com Schemas

Todos os endpoints usam schemas Pydantic para validação:

- **Criação:** `ClienteCreate` - com validação de campos obrigatórios
- **Atualização:** `ClienteUpdate` - todos campos opcionais
- **Resposta:** `ClienteResponse` sempre com timestamps
- **Detalhes:** `ClienteDetailResponse` com estatísticas

---

## Estrutura de Serviços

```
api/routes/cliente.py
├── criar_cliente() → ClienteService.create_cliente()
├── listar_clientes() → ClienteService.get_by_nutricionista()
├── obter_cliente() → ClienteService.get_cliente_por_nutricionista()
├── atualizar_cliente() → ClienteService.update_cliente()
└── deletar_cliente() → ClienteService.delete_cliente()

services/cliente_service.py → BaseService[Cliente, ClienteCreate]
```

---

## Próximas Melhorias

- [ ] Autenticação JWT para validar nutricionista
- [ ] Rate limiting por nutricionista
- [ ] Cache de listagem com Redis
- [ ] Busca e filtros avançados
- [ ] Exportação em CSV/Excel
- [ ] WebSocket para atualizações em tempo real
