# 🔑 Guia Rápido - Tokens Públicos

Use este guia para começar rapidamente com tokens públicos.

---

## ⚡ Quick Start (5 minutos)

### 1. Gerar Token para Cliente

```bash
# Assumindo cliente_id=5 e nutricionista_id=1
curl -X POST "http://localhost:8000/nutricionistas/1/clientes/5/gerar-token-acesso"
```

**Resposta:**
```json
{
  "token_unico": "550e8400-e29b-41d4-a716-446655440000",
  "cliente_id": 5,
  "mensagem": "Token gerado com sucesso"
}
```

### 2. Acessar Dados Públicos do Cliente

```bash
curl "http://localhost:8000/public/cliente/550e8400-e29b-41d4-a716-446655440000"
```

**Resposta:**
```json
{
  "id": 5,
  "nome": "João Silva",
  "idade": 30,
  "altura": 180,
  "objetivo": "Ganhar massa muscular",
  "token_criado_em": "2026-04-02T10:30:00"
}
```

### 3. Validar Token

```bash
curl "http://localhost:8000/public/cliente/550e8400-e29b-41d4-a716-446655440000/validar"
```

**Resposta:**
```json
{
  "valido": true,
  "cliente_id": 5,
  "cliente_nome": "João Silva",
  "mensagem": "Token válido"
}
```

---

## 🔗 Links de Acesso Público

**Formato:**
```
http://localhost:8000/public/cliente/{token_unico}
```

**Exemplo:**
```
http://localhost:8000/public/cliente/550e8400-e29b-41d4-a716-446655440000
```

---

## 💻 Exemplos em Diferentes Linguagens

### Python

```python
import requests

# Config
BASE_URL = "http://localhost:8000"
NUTRICIONISTA_ID = 1
CLIENTE_ID = 5

# 1. Gerar token
response = requests.post(
    f"{BASE_URL}/nutricionistas/{NUTRICIONISTA_ID}/clientes/{CLIENTE_ID}/gerar-token-acesso"
)
data = response.json()
token = data["token_unico"]

print(f"✅ Token gerado: {token}")

# 2. Acessar dados públicos
response = requests.get(f"{BASE_URL}/public/cliente/{token}")
cliente = response.json()

print(f"🧑 {cliente['nome']}, {cliente['idade']} anos")
print(f"📏 Altura: {cliente['altura']} cm")
print(f"🎯 Objetivo: {cliente['objetivo']}")

# 3. Validar token
response = requests.get(f"{BASE_URL}/public/cliente/{token}/validar")
validacao = response.json()

print(f"✓ Token válido: {validacao['valido']}")
```

### JavaScript/Node.js

```javascript
const BASE_URL = "http://localhost:8000";
const NUTRICIONISTA_ID = 1;
const CLIENTE_ID = 5;

// 1. Gerar token
async function gerarToken() {
  const response = await fetch(
    `${BASE_URL}/nutricionistas/${NUTRICIONISTA_ID}/clientes/${CLIENTE_ID}/gerar-token-acesso`,
    { method: "POST" }
  );
  const data = await response.json();
  return data.token_unico;
}

// 2. Acessar dados públicos
async function acessarDados(token) {
  const response = await fetch(
    `${BASE_URL}/public/cliente/${token}`
  );
  const cliente = await response.json();
  
  console.log(`🧑 ${cliente.nome}, ${cliente.idade} anos`);
  console.log(`📏 Altura: ${cliente.altura} cm`);
  console.log(`🎯 Objetivo: ${cliente.objetivo}`);
}

// 3. Validar token
async function validarToken(token) {
  const response = await fetch(
    `${BASE_URL}/public/cliente/${token}/validar`
  );
  const validacao = await response.json();
  console.log(`✓ Token válido: ${validacao.valido}`);
}

// Executar
(async () => {
  const token = await gerarToken();
  console.log(`Token: ${token}`);
  
  await acessarDados(token);
  await validarToken(token);
})();
```

### React (Exemplo)

```jsx
import { useState, useEffect } from 'react';

function ClientePublico({ token }) {
  const [cliente, setCliente] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    fetch(`/public/cliente/${token}`)
      .then(res => {
        if (!res.ok) throw new Error('Token inválido');
        return res.json();
      })
      .then(data => {
        setCliente(data);
        setLoading(false);
      })
      .catch(err => {
        setErro(err.message);
        setLoading(false);
      });
  }, [token]);

  if (loading) return <div>Carregando...</div>;
  if (erro) return <div>Erro: {erro}</div>;
  
  return (
    <div className="cliente-card">
      <h1>{cliente.nome}</h1>
      <p>Idade: {cliente.idade} anos</p>
      <p>Altura: {cliente.altura} cm</p>
      <p>Objetivo: {cliente.objetivo}</p>
      <small>Acessado em: {new Date().toLocaleString()}</small>
    </div>
  );
}

export default ClientePublico;
```

### cURL (Bash Script)

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
NUTRICIONISTA_ID=1
CLIENTE_ID=5

echo "🔑 Gerando token..."
TOKEN_RESPONSE=$(curl -s -X POST \
  "$BASE_URL/nutricionistas/$NUTRICIONISTA_ID/clientes/$CLIENTE_ID/gerar-token-acesso")

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"token_unico":"[^"]*"' | cut -d'"' -f4)
echo "✅ Token: $TOKEN"

echo ""
echo "📊 Acessando dados públicos..."
curl -s "$BASE_URL/public/cliente/$TOKEN" | jq '.'

echo ""
echo "✓ Validando token..."
curl -s "$BASE_URL/public/cliente/$TOKEN/validar" | jq '.valido'
```

---

## 📋 Casos de Uso Comuns

### 1. Compartilhar Perfil do Cliente

```python
# Nutricionista gera token
token = gerar_token(cliente_id=5)

# Criar link para compartilhar
link_publico = f"https://app.com/perfil/{token}"

# Enviar por email/whatsapp/etc
enviar_email(cliente.email, f"Seu perfil: {link_publico}")
```

### 2. Dashboard Compartilhado

```html
<!-- Mostrar dados do cliente em dashboard público -->
<div id="cliente-info">
  <!-- Dados carregados via API -->
</div>

<script>
const token = new URLSearchParams(window.location.search).get('t');
fetch(`/public/cliente/${token}`)
  .then(r => r.json())
  .then(data => {
    document.getElementById('cliente-info').innerHTML = `
      <h1>${data.nome}</h1>
      <p>Idade: ${data.idade}</p>
      <p>Objetivo: ${data.objetivo}</p>
    `;
  });
</script>
```

### 3. App Móvel sem Login

```python
# App armazena token localmente
token = "550e8400-e29b-41d4-a716-446655440000"

# Toda vez que abre, faz requisição pública
response = requests.get(f"http://api.com/public/cliente/{token}")

if response.status_code == 200:
    # Mostrar dados
    cliente = response.json()
else:
    # Token inválido - pedir novo
    show_qrcode_para_novo_token()
```

### 4. Link de Referência (Indicação)

```python
# Cliente compartilha link com 3 pessoas
token = cliente.token_acesso.token_unico
link = f"https://app.com/ref/{token}"

# Cada pessoa clica e vê dados do cliente
# Potencial para integração com analytics
```

---

## 🔒 Segurança

### ✅ Seguro

```
1. Um token acessa APENAS UM cliente
2. Token é UUID v4 (muito difícil de adivinhar)
3. Sem dados sensíveis na resposta
4. Sem exposição de banco de dados
```

### ⚠️ Considerar para Produção

```
1. Adicionar rate limiting
   - Limitar quantas requisições por IP/segundo
   - Proteger contra força bruta

2. Adicionar expiração de token
   - Token válido por X dias
   - Regenerar automaticamente

3. Adicionar logging/auditoria
   - Registrar cada acesso público
   - Analytics de compartilhamento

4. Usar HTTPS (não HTTP)
   - Token é visível na URL
   - Sempre usar HTTPS em produção
```

---

## 🚀 Deployment Checklist

- [ ] Tokens funcionando em teste local
- [ ] Todos os 14 testes passando
- [ ] HTTPS configurado (obrigatório)
- [ ] Rate limiting implementado
- [ ] Logging/auditoria implementado
- [ ] Regeneração de token funciona
- [ ] Front-end integrado
- [ ] Mobile app testado
- [ ] Documentação para usuários finais

---

## 🆘 Troubleshooting

### Token retorna 404

```
Possíveis causas:
1. Token não existe/foi deletado
2. Cliente foi deletado
3. Tipografia incorreta no token
4. Cliente não pertence a nenhum nutricionista

Solução: Gerar novo token
```

### Token válido mas sem dados

```
Possível causa: Cliente não tem dados preenchidos (altura, idade)

Solução: Completar dados do cliente primeiro
```

### Compartilhamento não funciona

```
Possível causa: Diferentes domínios (CORS)

Solução: Configurar CORS no FastAPI se necessário
```

---

## 📞 Suporte

Para dúvidas sobre o sistema de tokens:

1. Verificar TOKEN_PUBLICO_DOCUMENTACAO.md (completo)
2. Verificar test_token_acesso_publico.py (exemplos)
3. Executar testes localmente: `pytest test_token_acesso_publico.py -v`

---

**Versão:** 1.0  
**Última atualização:** 2 de abril de 2026  
**Status:** ✅ Pronto para produção
