# 🚀 Como Rodar o Nutri SaaS

## 📋 Pré-requisitos

- **Python 3.12+** (backend)
- **Node.js 18+** (frontend)
- **npm** (gerenciador de pacotes)

---

## ⚡ Quick Start (Forma Rápida) - Usando VS Code

### ⚙️ Setup Inicial (só uma vez)

No VS Code, abra o Terminal: `Ctrl + ~` (ou **Terminal > New Terminal**)

```bash
# 1. Entre na pasta frontend
cd frontend

# 2. Instale dependências do npm (só na primeira vez)
npm install
```

### 🚀 Rodar o Projeto - 2 Terminais

**Terminal 1 - Backend:**

No terminal que está aberto, execute:
```bash
source .venv/bin/activate
python main.py
```

Quando ver `✅ Iniciando Nutri SaaS API` = ✅ Backend OK

---

**Terminal 2 - Frontend:**

Abra **novo terminal** no VS Code:
- Clique no `+` ao lado da aba do terminal (ou `Ctrl + Shift + ~`)
- Execute:

```bash
cd frontend
npm run dev
```

Quando ver `➜ Local: http://localhost:3000/` = ✅ Frontend OK

### 💻 Acesse no Navegador
```
http://localhost:3000
```

Pronto! ✅

---

## � Fazer Login

### Credenciais de Teste

```
Email: teste@nutricionista.com
Senha: senha123456
```

1. Digite o **Email** e **Senha**
2. Clique em **"Entrar"**
3. Você verá o **Dashboard** com a lista de clientes

---

## 📱 O que você pode fazer

### Dashboard
Após login, você verá:
- **Total de clientes**: 3 (João, Maria, Pedro)
- **Dados dos clientes**
- **Métricas de saúde**

### Criar Novo Cliente
1. Clique em **"+ Novo Cliente"**
2. Preencha os dados:
   - Nome
   - Idade
   - Altura
   - Objetivo
3. Clique em **"Salvar"**

### Ver Detalhes do Cliente
1. Clique em um cliente na lista
2. Veja todas as informações
3. **Baixe PDF** (botão no topo)
4. **Copie link público** (compartilhe com cliente)

---

## 🐛 Troubleshooting

### ❌ Erro: "Address already in use" (porta 8000)

Significa que há um processo antigo rodando na porta 8000.

**Solução rápida:**
```bash
# Matar processo na porta 8000
lsof -ti :8000 | xargs kill -9

# Depois rodar novamente
source .venv/bin/activate
python main.py
```

### ❌ Erro: "Cannot find module" no npm

**Solução**: 
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### ❌ Backend retorna erro 404

Certifique-se que backend está rodando com `python main.py`

---

## 📚 Documentação Útil

- **Integração**: Ver [INTEGRATION.md](INTEGRATION.md)
- **API Docs**: `http://localhost:8000/api/docs`
- **Frontend**: Ver [frontend/FRONTEND.md](frontend/FRONTEND.md)

---

## 🛑 Parar os Servidores

### Terminal do Backend
Pressione: `Ctrl + C`

### Terminal do Frontend
Pressione: `Ctrl + C`

---

## ✨ Dicas Úteis

### Ver logs do Backend em tempo real
O backend mostra logs de todas as requisições:
```
INFO:     127.0.0.1:12345 - "POST /auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:12345 - "GET /nutricionistas/1/dashboard HTTP/1.1" 200 OK
```

### Recarregar o frontend automaticamente
Se mudar código do frontend, ele recarrega sozinho (hot reload).

### Recarregar o backend automaticamente
Se mudar código do backend, ele reinicia sozinho com `--reload`.

---

## 🎯 Estrutura de Pastas

```
/Users/hugo/Desktop/nutri saas/
├── main.py                 ← Backend (FastAPI)
├── database.db            ← Banco de dados
├── requirements.txt       ← Dependências Python
│
└── frontend/              ← Frontend (React + Vite)
    ├── package.json       ← Dependências Node
    ├── src/
    │   ├── pages/         ← Páginas
    │   ├── components/    ← Componentes
    │   └── services/      ← Serviços API
    └── dist/              ← Build para produção
```

---

## 🚀 Próximos Passos

1. ✅ Backend rodando
2. ✅ Frontend rodando
3. ✅ Fazer login
4. ✅ Criar cliente
5. ⏭️ Treinar no sistema
6. ⏭️ Customizar estilos
7. ⏭️ Deploar para produção

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique se ambos servidores estão rodando** (backend + frontend)
2. **Limpe o cache**: `Ctrl + Shift + Delete` no navegador
3. **Reinicie tudo**: Pare os servidores e comece novamente
4. **Verifique os logs**: Olhe console do backend e frontend

---

**Boa sorte! 🎉**
