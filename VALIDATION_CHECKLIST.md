# ✅ Validation Checklist - Cliente API Endpoints

Use this checklist to verify that all endpoints are working correctly.

---

## 🚀 Pre-Flight Checks

- [ ] **Python Environment**
  ```bash
  python --version  # Should be 3.10+
  pip list | grep -E "fastapi|sqlalchemy|pydantic"
  ```

- [ ] **Dependencies Installed**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Database Configured**
  ```bash
  # Check core/config.py for DATABASE_URL
  # Should be: postgresql://user:pass@localhost/nutri_saas
  #       or: sqlite:///./test.db (for development)
  ```

- [ ] **Can Start App**
  ```bash
  python main.py
  # Should output: INFO:     Uvicorn running on http://127.0.0.1:8000
  ```

---

## 📝 Endpoint Validation

### Before Testing: Create Test Data

```bash
# Terminal 1: Start the app
python main.py

# Terminal 2: Create a test nutritionist
curl -X POST http://localhost:8000/nutricionistas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. Test",
    "email": "test@example.com",
    "senha": "password123"
  }'

# Note the returned ID (e.g., 1) for use in tests below
```

---

## ✅ Endpoint Test Cases

### 1️⃣ CREATE - POST /nutricionistas/{id}/clientes

**Test Case 1.1: Success (201 Created)**
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
✅ Expected: Status 201, response includes `id`, `created_at`, `updated_at`
- [ ] Status Code: 201
- [ ] Response has `id` field
- [ ] Response has `created_at` timestamp
- [ ] Response has all input fields

**Test Case 1.2: Validation - Idade > 150 (422 Unprocessable Entity)**
```bash
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 1,
    "nome": "Test",
    "idade": 200,
    "altura": 180.5
  }'
```
✅ Expected: Status 422, error message about age validation
- [ ] Status Code: 422
- [ ] Error message mentions "idade"

**Test Case 1.3: Validation - Altura > 300 (422 Unprocessable Entity)**
```bash
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 1,
    "nome": "Test",
    "idade": 30,
    "altura": 350
  }'
```
✅ Expected: Status 422
- [ ] Status Code: 422

**Test Case 1.4: nutricionista_id Mismatch (400 Bad Request)**
```bash
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 999,
    "nome": "Test",
    "idade": 30,
    "altura": 180.5
  }'
```
✅ Expected: Status 400, error about mismatch
- [ ] Status Code: 400
- [ ] Error mentions nutricionista mismatch

---

### 2️⃣ LIST - GET /nutricionistas/{id}/clientes

**Test Case 2.1: List Empty (200 OK, empty array)**
```bash
curl -X GET http://localhost:8000/nutricionistas/9999/clientes
```
✅ Expected: Status 200, empty array `[]`
- [ ] Status Code: 200
- [ ] Response is empty array (if no prior creates)

**Test Case 2.2: List with Data (200 OK, array)**
```bash
# First create 2 clientes (using test case 1.1 twice)
curl -X GET http://localhost:8000/nutricionistas/1/clientes
```
✅ Expected: Status 200, array with 2+ items
- [ ] Status Code: 200
- [ ] Response is array
- [ ] Array has 2+ items
- [ ] Each item has all fields

**Test Case 2.3: Pagination - Default (10 items)**
```bash
curl -X GET http://localhost:8000/nutricionistas/1/clientes
```
✅ Expected: Status 200, max 10 items
- [ ] Status Code: 200
- [ ] Array length ≤ 10

**Test Case 2.4: Pagination - With Limit (5 items)**
```bash
curl -X GET "http://localhost:8000/nutricionistas/1/clientes?limit=5"
```
✅ Expected: Status 200, max 5 items
- [ ] Status Code: 200
- [ ] Array length ≤ 5

**Test Case 2.5: Pagination - With Skip & Limit**
```bash
curl -X GET "http://localhost:8000/nutricionistas/1/clientes?skip=5&limit=5"
```
✅ Expected: Status 200, different items from test 2.4
- [ ] Status Code: 200
- [ ] Items are different from first page

**Test Case 2.6: Pagination - Invalid Limit (422)**
```bash
curl -X GET "http://localhost:8000/nutricionistas/1/clientes?limit=999"
```
✅ Expected: Status 422 (limit max is 100)
- [ ] Status Code: 422

---

### 3️⃣ GET DETAIL - GET /nutricionistas/{id}/clientes/{cliente_id}

**Test Case 3.1: Success (200 OK with details)**
```bash
# Replace {cliente_id} with ID from test 1.1
curl -X GET http://localhost:8000/nutricionistas/1/clientes/1
```
✅ Expected: Status 200, includes detail fields like `total_medicoes`
- [ ] Status Code: 200
- [ ] Response includes `id`, `nome`, `idade`
- [ ] Response includes `total_medicoes`, `total_observacoes`

**Test Case 3.2: Not Found (404)**
```bash
curl -X GET http://localhost:8000/nutricionistas/1/clientes/9999
```
✅ Expected: Status 404
- [ ] Status Code: 404
- [ ] Error message about cliente not found

**Test Case 3.3: Authorization - Different Nutritionist (404)**
```bash
# Try to access cliente from nutricionista 2 as if it's from 1
curl -X GET http://localhost:8000/nutricionistas/2/clientes/1
```
✅ Expected: Status 404 (authorization prevents access)
- [ ] Status Code: 404
- [ ] Does NOT return cliente info (security)

---

### 4️⃣ UPDATE - PATCH /nutricionistas/{id}/clientes/{cliente_id}

**Test Case 4.1: Partial Update - Age Only (200 OK)**
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 35
  }'
```
✅ Expected: Status 200, idade changed, other fields unchanged
- [ ] Status Code: 200
- [ ] `idade` is now 35
- [ ] `nome` unchanged
- [ ] `updated_at` changed
- [ ] `created_at` unchanged

**Test Case 4.2: Full Update (200 OK)**
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Atualizado",
    "idade": 32,
    "altura": 181,
    "objetivo": "Ganho de massa"
  }'
```
✅ Expected: Status 200, all fields updated
- [ ] Status Code: 200
- [ ] `nome` changed
- [ ] `idade` changed
- [ ] `altura` changed
- [ ] `objetivo` changed

**Test Case 4.3: Validation - Age > 150 (422)**
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 200
  }'
```
✅ Expected: Status 422
- [ ] Status Code: 422

**Test Case 4.4: Not Found (404)**
```bash
curl -X PATCH http://localhost:8000/nutricionistas/1/clientes/9999 \
  -H "Content-Type: application/json" \
  -d '{"idade": 40}'
```
✅ Expected: Status 404
- [ ] Status Code: 404

**Test Case 4.5: Authorization - Different Nutritionist (404)**
```bash
curl -X PATCH http://localhost:8000/nutricionistas/2/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{"idade": 40}'
```
✅ Expected: Status 404 (authorization)
- [ ] Status Code: 404

---

### 5️⃣ DELETE - DELETE /nutricionistas/{id}/clientes/{cliente_id}

**Test Case 5.1: Success (204 No Content)**
```bash
curl -X DELETE http://localhost:8000/nutricionistas/1/clientes/1
```
✅ Expected: Status 204, no response body
- [ ] Status Code: 204
- [ ] No response body
- [ ] Cliente is gone (verify with GET)

**Test Case 5.2: Verify Cascade Delete**
After test 5.1:
```bash
# Try to GET deleted cliente
curl -X GET http://localhost:8000/nutricionistas/1/clientes/1
```
✅ Expected: Status 404 (cliente is deleted)
- [ ] Status Code: 404

**Test Case 5.3: Not Found (404)**
```bash
curl -X DELETE http://localhost:8000/nutricionistas/1/clientes/9999
```
✅ Expected: Status 404
- [ ] Status Code: 404

**Test Case 5.4: Authorization - Different Nutritionist (404)**
```bash
# Create cliente under nutri 1, try delete as nutri 2
curl -X DELETE http://localhost:8000/nutricionistas/2/clientes/1
```
✅ Expected: Status 404 (authorization)
- [ ] Status Code: 404

---

## 🧪 Integration Tests

### Full Workflow: Create → List → Read → Update → Delete

```bash
#!/bin/bash

# Variables
NUT_ID=1

# 1. CREATE
echo "📝 Creating cliente..."
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/nutricionistas/$NUT_ID/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": '$NUT_ID',
    "nome": "Integration Test",
    "idade": 25,
    "altura": 175,
    "objetivo": "Test"
  }')
CLIENT_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "✅ Created with ID: $CLIENT_ID"
[ ! -z "$CLIENT_ID" ] && echo "PASS" || echo "FAIL"

# 2. LIST
echo "📋 Listing clientes..."
LIST_RESPONSE=$(curl -s -X GET "http://localhost:8000/nutricionistas/$NUT_ID/clientes")
COUNT=$(echo $LIST_RESPONSE | grep -o '"id"' | wc -l)
echo "✅ Found $COUNT clientes"
[ "$COUNT" -gt 0 ] && echo "PASS" || echo "FAIL"

# 3. READ
echo "🔍 Getting cliente details..."
READ_RESPONSE=$(curl -s -X GET "http://localhost:8000/nutricionistas/$NUT_ID/clientes/$CLIENT_ID")
NOME=$(echo $READ_RESPONSE | grep -o '"nome":"[^"]*' | cut -d: -f2 | tr -d '"')
echo "✅ Got: $NOME"
[ ! -z "$NOME" ] && echo "PASS" || echo "FAIL"

# 4. UPDATE
echo "✏️ Updating cliente..."
UPDATE_RESPONSE=$(curl -s -X PATCH "http://localhost:8000/nutricionistas/$NUT_ID/clientes/$CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"idade": 26}')
NEW_IDADE=$(echo $UPDATE_RESPONSE | grep -o '"idade":[0-9]*' | cut -d: -f2)
echo "✅ New age: $NEW_IDADE"
[ "$NEW_IDADE" -eq 26 ] && echo "PASS" || echo "FAIL"

# 5. DELETE
echo "🗑️ Deleting cliente..."
DELETE_STATUS=$(curl -s -w "%{http_code}" -o /dev/null -X DELETE "http://localhost:8000/nutricionistas/$NUT_ID/clientes/$CLIENT_ID")
echo "✅ Delete status: $DELETE_STATUS"
[ "$DELETE_STATUS" -eq 204 ] && echo "PASS" || echo "FAIL"

# 6. VERIFY DELETED
echo "🔎 Verifying deletion..."
VERIFY_STATUS=$(curl -s -w "%{http_code}" -o /dev/null -X GET "http://localhost:8000/nutricionistas/$NUT_ID/clientes/$CLIENT_ID")
echo "✅ Verify status: $VERIFY_STATUS"
[ "$VERIFY_STATUS" -eq 404 ] && echo "PASS" || echo "FAIL"

echo ""
echo "✅ INTEGRATION TEST COMPLETE"
```

- [ ] All 6 steps passed

---

## 🧪 Automated Test Script

Run all tests at once:
```bash
python script_teste_cliente.py
```

- [ ] Script runs without errors
- [ ] Output shows ✅ for each test section
- [ ] No exceptions or tracebacks

---

## 📊 Performance Tests

### Response Time Test (should be < 500ms)

```bash
# Single request timing
time curl -X GET http://localhost:8000/nutricionistas/1/clientes/1

# Bulk requests (100 requests)
for i in {1..100}; do
  curl -s http://localhost:8000/nutricionista/1/clientes > /dev/null
done
```

- [ ] Average response time < 500ms
- [ ] Can handle 100+ requests without errors

### Pagination Performance (with lots of data)

```bash
# List first page
time curl -X GET "http://localhost:8000/nutricionistas/1/clientes?skip=0&limit=10"

# List last page (assuming 1000+ items)
time curl -X GET "http://localhost:8000/nutricionistas/1/clientes?skip=1000&limit=10"
```

- [ ] Both responses < 500ms
- [ ] Pagination works consistently

---

## 🔐 Security Validation

### Authorization Checks

**Test A: Cross-Nutritionist Access Blocked**
```bash
# Create 2 nutritionists
# Create client under nutri_1
# Verify nutri_2 cannot access nutri_1's client
curl -X GET "http://localhost:8000/nutricionistas/2/clientes/{nutri_1_cliente_id}"
# Should return 404, not the cliente
```
- [ ] Returns 404 (not 200)
- [ ] Doesn't leak client data

**Test B: Invalid Cliente ID Returns 404**
```bash
curl -X GET "http://localhost:8000/nutricionistas/1/clientes/99999"
```
- [ ] Returns 404
- [ ] Not 401 or 403

**Test C: Input Validation Works**
```bash
# SQL injection attempt
curl -X POST http://localhost:8000/nutricionistas/1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nutricionista_id": 1,
    "nome": "Test\"; DROP TABLE clientes; --",
    "idade": 30,
    "altura": 180.5
  }'
```
- [ ] Returns 201 (nome is literal string, no injection)
- [ ] Database is intact

---

## 📝 Documentation Validation

- [ ] CLIENTE_API.md exists and has examples
- [ ] CLIENTE_ENDPOINTS_TESTING.md has step-by-step guides
- [ ] ENDPOINT_ARCHITECTURE.md explains the patterns
- [ ] All examples in docs are syntactically correct

---

## 🎯 Final Sign-Off

Once all checks pass:

```
✅ CLIENTE API VALIDATION COMPLETE

Status: READY FOR PRODUCTION
  - All 5 endpoints working
  - All validations passing
  - Authorization working
  - Documentation complete
  - Performance acceptable

Known Issues:
  - TestClient execution blocked by starlette version
    (Use script_teste_cliente.py or curl as workaround)

Next Steps:
  1. Implement Nutricionista endpoints
  2. Implement Medicao endpoints
  3. Add JWT authentication
  4. Deploy to staging environment
```

- [ ] All checks complete
- [ ] All endpoints validated
- [ ] Documentation confirmed
- [ ] Ready to proceed to next phase

---

**Validated By:** _________________  
**Date:** _________________  
**Status:** ✅ PASSED / ❌ FAILED  

---

Última atualização: 2024-01-15
