# Cliente API - Guia Completo de Testes

Este guia demonstra como testar todos os 5 endpoints da API de Cliente usando diferentes métodos.

## 🚀 Início Rápido

### Carregar os dados necessários (Optional)

```bash
# Cria um nutricionista de teste
curl -X POST http://localhost:8000/nutricionistas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. João Silva",
    "email": "joao@test.com",
    "senha": "senha123"
  }'

# Resposta esperada:
# {
#   "id": 1,
#   "nome": "Dr. João Silva",
#   "email": "joao@test.com",
#   "created_at": "2024-01-15T10:00:00",
#   "updated_at": "2024-01-15T10:00:00"
# }
```

## 📝 Teste 1: Criar Cliente (POST)

### Endpoint
```
POST /nutricionistas/{nutricionista_id}/clientes
```

### Request (cURL)
```bash
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 1,
    "nome": "João Silva",
    "idade": 30,
    "altura": 180.5,
    "objetivo": "Perda de peso",
    "notas": "Cliente com histórico familiar de diabetes"
  }'
```

### Request (Python)
```python
import requests

response = requests.post(
    'http://localhost:8000/nutricionistas/1/clientes',
    json={
        'nutricionista_id': 1,
        'nome': 'João Silva',
        'idade': 30,
        'altura': 180.5,
        'objetivo': 'Perda de peso',
        'notas': 'Cliente com histórico familiar de diabetes'
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### Response (201 CREATED)
```json
{
  "id": 1,
  "nutricionista_id": 1,
  "nome": "João Silva",
  "idade": 30,
  "altura": 180.5,
  "objetivo": "Perda de peso",
  "notas": "Cliente com histórico familiar de diabetes",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

### Validações
- ❌ `idade > 150` → 422 Unprocessable Entity
- ❌ `altura > 300` → 422 Unprocessable Entity
- ❌ `nutricionista_id` diferente do URL → 400 Bad Request
- ❌ `nutricionista_id` não existente → 400 Bad Request

---

## 📋 Teste 2: Listar Clientes (GET)

### Endpoint
```
GET /nutricionistas/{nutricionista_id}/clientes?skip=0&limit=10
```

### Request (cURL - Sem Paginação)
```bash
curl -X GET http://localhost:8000/nutricionistas/1/clientes
```

### Request (cURL - Com Paginação)
```bash
# Primeira página (primeiros 5)
curl -X GET "http://localhost:8000/nutricionistas/1/clientes?skip=0&limit=5"

# Segunda página
curl -X GET "http://localhost:8000/nutricionistas/1/clientes?skip=5&limit=5"
```

### Request (Python)
```python
import requests

# Sem paginação
response = requests.get('http://localhost:8000/nutricionistas/1/clientes')

# Com paginação
response = requests.get(
    'http://localhost:8000/nutricionistas/1/clientes',
    params={'skip': 0, 'limit': 5}
)

clientes = response.json()
print(f"Total: {len(clientes)} clientes")
for cliente in clientes:
    print(f"- {cliente['nome']} ({cliente['idade']} anos)")
```

### Response (200 OK)
```json
[
  {
    "id": 1,
    "nutricionista_id": 1,
    "nome": "João Silva",
    "idade": 30,
    "altura": 180.5,
    "objetivo": "Perda de peso",
    "notas": "Cliente com histórico familiar de diabetes",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  },
  {
    "id": 2,
    "nutricionista_id": 1,
    "nome": "Maria Santos",
    "idade": 28,
    "altura": 165.0,
    "objetivo": "Ganho de massa muscular",
    "notas": null,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

### Query Parameters
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| skip | integer | 0 | Número de clientes a pular |
| limit | integer | 10 | Máximo de clientes (1-100) |

### Validações
- ❌ `skip < 0` → 422 Unprocessable Entity
- ❌ `limit < 1 ou limit > 100` → 422 Unprocessable Entity

---

## 🔍 Teste 3: Obter Detalhes do Cliente (GET)

### Endpoint
```
GET /nutricionistas/{nutricionista_id}/clientes/{cliente_id}
```

### Request (cURL)
```bash
curl -X GET http://localhost:8000/nutricionistas/1/clientes/1
```

### Request (Python)
```python
import requests

response = requests.get('http://localhost:8000/nutricionistas/1/clientes/1')
cliente = response.json()

print(f"Cliente: {cliente['nome']}")
print(f"Idade: {cliente['idade']} anos")
print(f"Altura: {cliente['altura']} cm")
print(f"Total de medições: {cliente.get('total_medicoes', 0)}")
print(f"Total de observações: {cliente.get('total_observacoes', 0)}")
print(f"Total de documentos: {cliente.get('total_documentos', 0)}")
```

### Response (200 OK)
```json
{
  "id": 1,
  "nutricionista_id": 1,
  "nome": "João Silva",
  "idade": 30,
  "altura": 180.5,
  "objetivo": "Perda de peso",
  "notas": "Cliente com histórico familiar de diabetes",
  "total_medicoes": 5,
  "total_observacoes": 3,
  "total_documentos": 2,
  "ultimo_peso": 85.5,
  "data_ultima_medicao": "2024-01-14T09:00:00",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

### Validações
- ❌ `cliente_id` não existe → 404 Not Found
- ❌ Cliente de outro nutricionista → 404 Not Found (autorização)

---

## ✏️ Teste 4: Atualizar Cliente (PATCH)

### Endpoint
```
PATCH /nutricionistas/{nutricionista_id}/clientes/{cliente_id}
```

### Request (cURL - Atualizar Alguns Campos)
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 31,
    "objetivo": "Ganho de massa muscular"
  }'
```

### Request (cURL - Atualizar Todos os Campos)
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Atualizado",
    "idade": 31,
    "altura": 181.0,
    "objetivo": "Ganho de massa muscular",
    "notas": "Novas notas"
  }'
```

### Request (Python - Atualização Parcial)
```python
import requests

response = requests.patch(
    'http://localhost:8000/nutricionistas/1/clientes/1',
    json={
        'idade': 31,
        'objetivo': 'Ganho de massa muscular'
    }
)

print(f"Status: {response.status_code}")
cliente = response.json()
print(f"Cliente atualizado: {cliente['nome']}")
print(f"Nova idade: {cliente['idade']}")
print(f"Novo objetivo: {cliente['objetivo']}")
```

### Response (200 OK)
```json
{
  "id": 1,
  "nutricionista_id": 1,
  "nome": "João Silva",
  "idade": 31,
  "altura": 180.5,
  "objetivo": "Ganho de massa muscular",
  "notas": "Cliente com histórico familiar de diabetes",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:01:30"
}
```

### Validações
- ❌ `cliente_id` não existe → 404 Not Found
- ❌ `idade > 150` → 422 Unprocessable Entity
- ❌ `altura > 300` → 422 Unprocessable Entity
- ❌ Cliente de outro nutricionista → 404 Not Found (autorização)

---

## 🗑️ Teste 5: Deletar Cliente (DELETE)

### Endpoint
```
DELETE /nutricionistas/{nutricionista_id}/clientes/{cliente_id}
```

### Request (cURL)
```bash
curl -X DELETE http://localhost:8000/nutricionistas/1/clientes/1
```

### Request (Python)
```python
import requests

response = requests.delete('http://localhost:8000/nutricionistas/1/clientes/1')

print(f"Status: {response.status_code}")
if response.status_code == 204:
    print("Cliente deletado com sucesso!")
else:
    print(f"Erro: {response.json()}")
```

### Response (204 NO CONTENT)
```
(Sem corpo de resposta)
```

### Validações
- ❌ `cliente_id` não existe → 404 Not Found
- ❌ Cliente de outro nutricionista → 404 Not Found (autorização)

### Efeitos Colaterais
- ✅ Todas as medições do cliente são deletadas
- ✅ Todas as observações do cliente são deletadas
- ✅ Todos os documentos do cliente são deletados
- ✅ Todos os tokens de acesso do cliente são deletados

---

## 🧪 Testes de Integração

### Fluxo Completo: Criar → Listar → Atualizar → Deletar

```bash
#!/bin/bash

NUTRICIONISTA_ID=1

# 1. Criar cliente
echo "1️⃣ Criando cliente..."
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/nutricionistas/$NUTRICIONISTA_ID/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": '$NUTRICIONISTA_ID',
    "nome": "João Silva",
    "idade": 30,
    "altura": 180.5,
    "objetivo": "Perda de peso"
  }')

CLIENTE_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "   ✅ Cliente criado com ID: $CLIENTE_ID"

# 2. Listar clientes
echo "2️⃣ Listando clientes..."
curl -s -X GET "http://localhost:8000/nutricionistas/$NUTRICIONISTA_ID/clientes" | jq .

# 3. Obter detalhes
echo "3️⃣ Obtendo detalhes do cliente..."
curl -s -X GET "http://localhost:8000/nutricionistas/$NUTRICIONISTA_ID/clientes/$CLIENTE_ID" | jq .

# 4. Atualizar
echo "4️⃣ Atualizando cliente..."
curl -s -X PATCH "http://localhost:8000/nutricionistas/$NUTRICIONISTA_ID/clientes/$CLIENTE_ID" \
  -H "Content-Type: application/json" \
  -d '{"idade": 31, "objetivo": "Ganho de massa"}' | jq .

# 5. Deletar
echo "5️⃣ Deletando cliente..."
DELETE_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "http://localhost:8000/nutricionistas/$NUTRICIONISTA_ID/clientes/$CLIENTE_ID")
STATUS_CODE="${DELETE_RESPONSE: -3}"
echo "   Status: $STATUS_CODE"

# 6. Verificar que foi deletado
echo "6️⃣ Verificando que foi deletado (404 esperado)..."
curl -s -X GET "http://localhost:8000/nutricionistas/$NUTRICIONISTA_ID/clientes/$CLIENTE_ID" | jq .
```

---

## 📊 Códigos de Status HTTP

| Status | Significado | Cenário |
|--------|-------------|---------|
| 201 | Created | Cliente criado com sucesso |
| 200 | OK | Operação GET/PATCH bem-sucedida |
| 204 | No Content | Operação DELETE bem-sucedida |
| 400 | Bad Request | Validação falhou (nutricionista_id desabilitado, etc) |
| 404 | Not Found | Cliente não existe ou pertence a outro nutricionista |
| 422 | Unprocessable Entity | Validação de dados falhou |
| 500 | Internal Server Error | Erro do servidor |

---

## 🔐 Autorização (Authorization Pattern)

Todos os endpoints verificam se o cliente pertence ao nutricionista especificado:

```python
# Verificação interna na service layer
cliente = service.get_cliente_por_nutricionista(cliente_id, nutricionista_id)
if not cliente:
    raise HTTPException(404, "Cliente não encontrado para este nutricionista")
```

**Implicações:**
- Você NÃO pode acessar clientes de outro nutricionista
- GET em cliente de outro nutricionista retorna 404
- PATCH em cliente de outro nutricionista retorna 404
- DELETE em cliente de outro nutricionista retorna 404

---

## 🛠️ Troubleshooting

### Erro: `404 Not Found`
- ✅ Verifique se o `nutricionista_id` está correto
- ✅ Verifique se o `cliente_id` está correto
- ✅ Verifique se o cliente pertence ao nutricionista (verif. autorização)

### Erro: `422 Unprocessable Entity`
Verifique as validações:
- ✅ `idade` deve estar entre 0 e 150
- ✅ `altura` deve estar entre 0 e 300 cm
- ✅ `nome` deve ser uma string não-vazia
- ✅ `nutricionista_id` deve ser um inteiro válido

### Erro: `400 Bad Request`
- ✅ `nutricionista_id` no JSON não corresponde ao URL
- ✅ `nutricionista_id` fornecido não existe

---

## 📌 Notas Importantes

### Comportamento de Paginação
- Default: `skip=0, limit=10`
- `limit` máximo: 100 registros por página
- Use `skip` para navegar entre páginas: `skip = (page - 1) * limit`

### Comportamento de Atualização (PATCH)
- Usa `exclude_unset=True` para permitir atualizações parciais
- Campos não fornecidos não são alterados
- `created_at` nunca é alterado
- `updated_at` é atualizado automaticamente

### Comportamento de Deleção (DELETE)
- DELETE em cascata: todas as entidades relacionadas são removidas
- Medições, observações, documentos e tokens são deletados junto
- Não há soft delete - é uma deleção permanente

---

## 🚀 Executar Script de Teste

Para testar todos os endpoints automaticamente:

```bash
python script_teste_cliente.py
```

O script irá:
1. ✅ Criar um TestClient FastAPI
2. ✅ Executar testes para: criar, listar, paginar, obter, atualizar, deletar
3. ✅ Executar testes de validação
4. ✅ Exibir resultados com emojis de status

---

## 📚 Referências Adicionais

- API completa: [CLIENTE_API.md](CLIENTE_API.md)
- Service layer: [services/cliente_service.py](services/cliente_service.py)
- Routes: [api/routes/cliente.py](api/routes/cliente.py)
- Models: [models/cliente.py](models/cliente.py)
- Schemas: [schemas/cliente.py](schemas/cliente.py)

---

## ✅ Checklist de Testes

Use este checklist para validar manualmente todos os endpoints:

- [ ] **POST /nutricionistas/{id}/clientes** - Criar cliente com sucesso (201)
- [ ] **POST /nutricionistas/{id}/clientes** - Rejeitar idade > 150 (422)
- [ ] **POST /nutricionistas/{id}/clientes** - Rejeitar altura > 300 (422)
- [ ] **POST /nutricionistas/{id}/clientes** - Rejeitar nutricionista_id desabilitado (400)
- [ ] **GET /nutricionistas/{id}/clientes** - Listar clientes vazios (200, [])
- [ ] **GET /nutricionistas/{id}/clientes** - Listar com 3+ clientes (200, array)
- [ ] **GET /nutricionistas/{id}/clientes?skip=0&limit=5** - Paginação (200, limit respeitado)
- [ ] **GET /nutricionistas/{id}/clientes/{id}** - Obter detalhes (200, com stats)
- [ ] **GET /nutricionistas/{id}/clientes/{invalid}** - 404 Not Found
- [ ] **GET /nutricionistas/{id}/clientes/{outro_nut_cliente}** - 404 (autorização)
- [ ] **PATCH /nutricionistas/{id}/clientes/{id}** - Atualizar alguns campos (200)
- [ ] **PATCH /nutricionistas/{id}/clientes/{id}** - Atualizar age > 150 (422)
- [ ] **PATCH /nutricionistas/{id}/clientes/{invalid}** - 404 Not Found
- [ ] **DELETE /nutricionistas/{id}/clientes/{id}** - Deletar com sucesso (204)
- [ ] **DELETE /nutricionistas/{id}/clientes/{id}** - Verificar cascade delete
- [ ] **DELETE /nutricionistas/{id}/clientes/{invalid}** - 404 Not Found

---

Última atualização: 2024-01-15
