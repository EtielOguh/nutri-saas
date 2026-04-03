# 🔍 Debug - Login não funciona

## ✅ O que foi verificado

- ✅ Backend rodando em `http://localhost:8000`
- ✅ Frontend rodando em `http://localhost:3000`
- ✅ Dados de teste existem (teste@nutricionista.com)
- ✅ Login via API funciona (retorna token)

## 🐛 Possíveis problemas no Frontend

### 1. Abra o Console do Navegador
```
Chrome: F12 → Console
Firefox: F12 → Console
Safari: Cmd+Option+I → Console
```

### 2. Procure por Erros
Você deve ver uma mensagem como:
- `"Email ou senha inválidos"` - Problema na API
- Nada acontece - Erro na rede ou JavaScript
- Erro de CORS - Problema na comunicação

### 3. Teste o Login Digitando no Console

Copie e cole no **Console do navegador**:

```javascript
// Fazer login via Fetch API
fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'teste@nutricionista.com',
    senha: 'senha123456'
  })
})
.then(r => r.json())
.then(data => console.log('Resposta:', data))
.catch(err => console.error('Erro:', err))
```

Se retornar um objeto com `token`, a API está funcionando.

### 4. Verifique a URL da API

No Console, execute:
```javascript
console.log('API URL:', import.meta.env.VITE_API_URL)
```

Deve mostrar: `http://localhost:8000`

### 5. Reinicie o Frontend

Se fez qualquer mudança, reinicie:
```bash
# Terminal do frontend
Ctrl + C
npm run dev
```

## 🆘 Se ainda não funcionar

1. **Limpe o cache do navegador:**
   - F12 → Application → Clear Storage → Clear all

2. **Feche e abra de novo o navegador**

3. **Teste direto via API:**
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"teste@nutricionista.com","senha":"senha123456"}'
   ```
   
   Se retornar com `token`, o problema é no frontend.

4. **Compartilhe o erro do console** comigo para debugar.

---

**Dica:** Com a aba Console aberta (F12), tente fazer login novamente. Qualquer erro vai aparecer lá!
