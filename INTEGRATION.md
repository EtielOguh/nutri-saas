# 🔗 Guia de Integração Frontend-Backend

## Visão Geral da Integração

Este documento descreve como o frontend React se integra com o backend FastAPI para o NutriSaaS.

---

## 🎯 Fluxo Principal

### 1. **Login do Nutricionista**

**Frontend:**
- Usuário acessa `/login`
- Preenche email e senha
- Clica em "Entrar"

**Backend:**
- `POST /auth/login`
- Recebe: `{ email, senha }`
- Retorna: `{ id, nome, email, token }`

**Frontend (após sucesso):**
- Armazena token em `localStorage`
- Armazena dados do nutricionista em `localStorage`
- Redireciona para `/dashboard`

```javascript
// Armazenamento
localStorage.setItem('token', response.data.token)
localStorage.setItem('nutricionista', JSON.stringify({
  id: response.data.id,
  nome: response.data.nome,
  email: response.data.email
}))

// Uso em requisições
headers: {
  'Authorization': `Bearer ${token}`
}
```

---

### 2. **Dashboard**

**Frontend:**
- Acessa `/dashboard`
- Carrega dados do nutricionista logado

**Backend:**
- `GET /nutricionistas/{nutricionista_id}/dashboard`
- Retorna: `{ total_clients, clients_this_month, average_tmb, retention_rate }`

**Fluxo:**
```
[Dashboard Page]
  ↓
useEffect() → nutricionistaService.getDashboard(user.id)
  ↓
Axios com interceptor de auth
  ↓
GET /nutricionistas/1/dashboard
  ↓
Exibe 4 cards com métricas
```

---

### 3. **Cadastro de Cliente**

**Frontend:**
- Acessa `/clientes/novo`
- Preenche formulário com dados do cliente
- Clica em "Criar Cliente"

**Formulário de Cadastro:**
```
- Nome (obrigatório)
- Email (obrigatório)
- Telefone
- Idade (número)
- Gênero (select)
- Peso Inicial (kg)
- Altura (m)
- Objetivo (textarea)
- Notas (textarea)
```

**Backend:**
- `POST /nutricionistas/{nutricionista_id}/clientes`
- Recebe: Dados completos do cliente
- Retorna: Cliente criado com `{ id, name, email, ... }`

**Frontend (após sucesso):**
- Redireciona para `/clientes/{id}` (página de detalhe)

```javascript
const response = await clientService.createClient(user.id, {
  nutricionista_id: user.id,
  name: 'João Silva',
  email: 'joao@email.com',
  age: 30,
  ...
})

navigate(`/clientes/${response.id}`)
```

---

### 4. **Visualização de Cliente**

**Frontend:**
- Acessa `/clientes/{id}`
- Carrega dados do cliente

**Backend:**
- `GET /clientes/{id}` → Dados do cliente
- `GET /clientes/{id}/medicoes` → Histórico de medições

**Exibição:**
```
┌─────────────────────────────┐
│  Nome: João Silva           │
│  Email: joao@email.com      │
│  Idade: 30 anos             │
│  Peso Inicial: 75 kg        │
│  Altura: 1.75 m             │
│  Objetivo: Ganhar massa     │
│                             │
│  🌐 Link Público:           │
│  [Copiar]                   │
│  [📥 PDF] [✏️ Editar]       │
└─────────────────────────────┘
```

**Link Público:**
- O cliente tem um `public_token` (UUID)
- Link público: `/public/cliente/{public_token}`
- **Sem autenticação necessária**
- Mostra apenas dados públicos

---

### 5. **Medições**

**Frontend:**
- Na página de cliente (`/clientes/{id}`)
- Formulário para adicionar nova medição
- Histórico de medições com datas

**Backend:**
- `POST /clientes/{id}/medicoes` → Adiciona medição
- `GET /clientes/{id}/medicoes` → Lista medições

**Dados de Medição:**
```
{
  weight: 75.5,       // kg (obrigatório)
  height: 1.75,       // m
  waist: 85,          // cm
  hip: 95,            // cm
  notes: 'Observação',
  date: '2026-04-03T10:30:00'
}
```

---

### 6. **Geração de PDF**

**Frontend:**
- Botão "📥 PDF" na página de cliente
- Clica para baixar PDF do relatório

**Backend:**
- `POST /pdf/cliente/{id}/download`
- Retorna: PDF com dados do cliente
- Content-Type: `application/pdf`
- Header: `Content-Disposition: attachment`

**Frontend (download):**
```javascript
const response = await fetch(`/api/clientes/${id}/pdf`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`
  }
})

const blob = await response.blob()
const url = window.URL.createObjectURL(blob)
const a = document.createElement('a')
a.href = url
a.download = `cliente_${name}.pdf`
a.click()
```

---

### 7. **Link Público e Page Pública**

**Acesso Público (sem login):**
- URL: `/public/cliente/{token}`
- Retorna dados básicos do cliente
- Mostra informações que o nutricionista permitiu

**Frontend (page pública):**
- Não precisa estar logado
- Faz requisição a `GET /public/cliente/{token}`
- Exibe apenas: nome, idade, altura, objetivo, medições (opcionais)

```javascript
// Frontend
GET /public/cliente/550e8400-e29b-41d4-a716-446655440000

// Backend retorna
{
  id: 1,
  nome: 'João Silva',
  idade: 30,
  altura: 1.75,
  objetivo: 'Ganhar massa',
  token_criado_em: '2026-04-02T10:30:00'
}
```

---

## 🔐 Autenticação e Autorização

### Token JWT

**Estrutura:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Payload:**
```json
{
  "sub": "1",
  "exp": 1680604253
}
```

**Requisição com Token:**
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Tratamento de 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### Proteção de Rotas

**Frontend:**
- Rotas protegidas validam `localStorage.getItem('token')`
- Se não existir token → Redireciona para login
- PrivateRoute component verifica autenticação

```javascript
<PrivateRoute>
  <DashboardPage />
</PrivateRoute>
```

---

## 📡 Endpoints da API

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/login` | Login com email e senha |
| POST | `/auth/verify` | Verificar validade do token |

### Nutricionista

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/nutricionistas/{id}` | Obter dados do nutricionista |
| GET | `/nutricionistas/{id}/dashboard` | Dashboard com métricas |
| GET | `/nutricionistas/{id}/configuracao` | Configurações do perfil |
| PUT | `/nutricionistas/{id}/configuracao` | Atualizar configurações |
| POST | `/nutricionistas/{id}/logo` | Upload de logo |

### Clientes

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/nutricionistas/{id}/clientes` | Criar novo cliente |
| GET | `/nutricionistas/{id}/clientes` | Listar clientes (paginado) |
| GET | `/clientes/{id}` | Obter dados do cliente |
| PUT | `/clientes/{id}` | Atualizar cliente |
| DELETE | `/clientes/{id}` | Deletar cliente |

### Medições

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/clientes/{id}/medicoes` | Listar medições |
| POST | `/clientes/{id}/medicoes` | Adicionar medição |

### PDF

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/pdf/cliente/{id}/download` | Download PDF do cliente |
| GET | `/pdf/cliente/{id}/inline` | Visualizar PDF no browser |

### Público (sem autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/public/cliente/{token}` | Acessar cliente por token |

---

## 🔄 StateManagement

### Context API (Autenticação)

**AuthContext:**
```javascript
{
  user: { id, nome, email },
  loading: boolean,
  error: null | string,
  login: (email, senha) => Promise,
  logout: () => void,
  isAuthenticated: boolean
}
```

**Uso:**
```javascript
const { user, login, logout, isAuthenticated } = useAuth()
```

### Service Layer (API Calls)

**authService:**
- login(email, senha)
- logout()
- getCurrentNutricionista()

**nutricionistaService:**
- getInfo(id)
- getDashboard(id)
- updateConfig(id, config)
- uploadLogo(id, file)

**clientService:**
- listClients(nutritionistId, page, size)
- getClient(id)
- createClient(nutritionistId, data)
- updateClient(id, data)
- deleteClient(id)
- getMeasurements(id)
- addMeasurement(id, data)

---

## 📊 Fluxo de Dados Completo

```
┌─────────────────────────────────────────────────────────────┐
│                     USUÁRIO                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (React)                           │
│  - Pages (Login, Dashboard, Clients)                        │
│  - Components (Header, Card, Form)                          │
│  - Services (auth, client, nutricionista)                   │
│  - Context (Auth)                                           │
│  - State (Component, localStorage)                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
         [Axios com Interceptors de Auth]
                              ↓
         [HTTP Requests com Bearer Token]
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                         │
│  - Routes (auth, client, nutricionista, pdf)               │
│  - Services (business logic)                                │
│  - Models (Database)                                        │
│  - Schemas (Validation)                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              BANCO DE DADOS (PostgreSQL)                    │
│  - Tables: nutricionistas, clientes, medicoes               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Exemplo de Fluxo Completo

### 1. Login
```javascript
// Frontend
POST /auth/login
{ email: 'nutri@email.com', senha: 'senha123' }

// Backend
✓ Valida email/senha
✓ Gera JWT
✓ Retorna { id: 1, nome: 'Dr. Silva', email, token }

// Frontend
✓ Armazena token e dados
✓ Redireciona para /dashboard
```

### 2. Dashboard
```javascript
// Frontend
GET /nutricionistas/1/dashboard

// Backend
✓ Verifica JWT (válido)
✓ Consulta banco de dados
✓ Retorna { total_clients: 15, clients_this_month: 3, ... }

// Frontend
✓ Exibe 4 cards com métricas
```

### 3. Criar Cliente
```javascript
// Frontend
POST /nutricionistas/1/clientes
{
  nutricionista_id: 1,
  name: 'João',
  email: 'joao@email.com',
  age: 30,
  ...
}

// Backend
✓ Valida dados (pydantic)
✓ Insere no banco de dados
✓ Retorna { id: 42, name: 'João', ... }

// Frontend
✓ Redireciona para /clientes/42
```

### 4. Exibir PDF Público
```javascript
// Frontend (URL)
GET /public/cliente/550e8400-e29b-41d4-a716-446655440000

// Backend
✓ Localiza cliente pelo token
✓ Gera PDF com dados
✓ Retorna arquivo PDF

// Frontend
✓ Browser faz download
```

---

## 🛠️ Variáveis de Ambiente

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000/api
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/nutri_saas
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ✅ Checklist de Integração

- [x] Login funcionando
- [x] Token armazenado e injetado
- [x] 401 redirect para login
- [x] Dashboard carregando métricas
- [x] Criar cliente funcionando
- [x] Visualizar cliente funcionando
- [x] Adicionar medição funcionando
- [x] Download PDF funcionando
- [x] Link público funcionando
- [x] Logout funcionando
- [x] Erro handling

---

## 📞 Suporte

Para dúvidas sobre a integração:
1. Verifique os logs do backend: `uvicorn main.py --reload`
2. Verifique o DevTools do navegador (Network, Console)
3. Verifique o localStorage para token e dados
4. Verifique o header Authorization nas requisições

