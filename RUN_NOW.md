# 🚀 Rodar Nutri SaaS Agora

## Versão Super Rápida (MAC + VS Code)

### Terminal 1 - Backend ✅ (Já está rodando)
Backend em `http://localhost:8000`  
API Docs em `http://localhost:8000/api/docs`

```bash
# Já tá rodando lá ^
```

### Terminal 2 - Frontend (Nova aba no VS Code)

Abra um **novo terminal** no VS Code (tecla **`Ctrl + Shift + Backtick`** ou use o "+"):

```bash
cd frontend
npm run dev
```

Isso vai abrir automaticamente em `http://localhost:3000`

---

## 🧪 Testar Agora

### 1️⃣ Fazer Login
- **Email:** `teste@nutricionista.com`
- **Senha:** `senha123456`

### 2️⃣ Testar Configurações (Settings)
- Clique em **⚙️ Configurações** (canto superior direito)
- ✅ Deve carregar **SEM redirecionar para login**
- Tente salvar uma configuração

### 3️⃣ Criar Novo Cliente
- Clique em **"Novo Cliente"** ou por URL: `http://localhost:3000/clientes`
- Preencha o formulário
- ✅ Deve **criar com sucesso**

### 4️⃣ Abrir Cliente Existente
- Clique em um cliente da lista
- ✅ Deve **carregar os dados** (antes dava erro)

---

## 🐛 Debugging

### Abra o Console do Browser (F12)
- **Aba "Network":** Veja se todas requisições retornam `200` ou `201`
- **Aba "Console":** Procure por erros vermelhos
- **Aba "Application":** Procure por token no `localStorage` em `auth_data`

### Backend Logs
Se der erro 401 ou 403, veja no **Terminal 1** qual foi o erro

---

## ✅ Checklist Rápido

- [ ] Backend rodando em `8000` (Terminal 1)
- [ ] Frontend rodando em `3000` (Terminal 2)
- [ ] Conseguiu fazer login
- [ ] Configurações carregam sem redirecionar
- [ ] Conseguiu criar cliente
- [ ] Conseguiu abrir cliente já criado
- [ ] Nenhum erro no browser console (F12)

---

**Pronto? Comanca!** 🎯
