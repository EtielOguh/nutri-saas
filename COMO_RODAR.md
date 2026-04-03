# 🚀 Como Rodar o Nutri SaaS

## 📋 Pré-requisitos

- **Python 3.12+** (backend)
- **Node.js 18+** (frontend)
- **npm** (gerenciador de pacotes)

---

## ⚡ Quick Start (Forma Rápida)

### Terminal 1 - Backend
```bash
cd /Users/hugo/Desktop/nutri\ saas
source .venv/bin/activate
python main.py
```

### Terminal 2 - Frontend
```bash
cd /Users/hugo/Desktop/nutri\ saas/frontend
npm install  # Apenas primeira vez
npm run dev
```

### Abra seu navegador
```
http://localhost:3000
```

Pronto! ✅

---

## 📖 Guia Detalhado

### Passo 1: Ativar Backend

**1.1 - Abra um terminal nova e navegue até a pasta do projeto:**
```bash
cd /Users/hugo/Desktop/nutri\ saas
```

**1.2 - Ative o ambiente virtual Python:**
```bash
source .venv/bin/activate
```

Você verá `(.venv)` aparecer no terminal.

**1.3 - Inicie o servidor:**
```bash
python main.py
```

Você verá algo como:
```
✅ Iniciando Nutri SaaS! (v1.0.0)
📊 Banco de dados: database.db
🏠 Servidor: http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/api/docs
```

✅ Backend rodando em `http://localhost:8000`

---

### Passo 2: Ativar Frontend

**2.1 - Abra outro terminal E navegue até a pasta frontend:**
```bash
cd /Users/hugo/Desktop/nutri\ saas/frontend
```

**2.2 - Instale as dependências (apenas na primeira vez):**
```bash
npm install
```

Aguarde o npm baixar e instalar todos os pacotes.

**2.3 - Inicie o servidor de desenvolvimento:**
```bash
npm run dev
```

Você verá:
```
  VITE v4.x.x  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

✅ Frontend rodando em `http://localhost:3000`

---

### Passo 3: Abra o Navegador

Vá até: **`http://localhost:3000`**

---

## 🔐 Fazer Login

### Credenciais de Teste

```
Email: teste@nutricionista.com
Senha: senha123456
```

![login-screen]

1. **Email**: Digite `teste@nutricionista.com`
2. **Senha**: Digite `senha123456`
3. **Clique em "Entrar"**

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

### Erro: "Address already in use" (porta 8000)

**Solução**: Matou o servidor anterior? Tente:
```bash
# Encontre qual processo está usando a porta 8000
lsof -i :8000

# Ou simplesmente use outra porta:
python main.py --port 8001
```

### Erro: "Cannot find module" no npm

**Solução**: Reinstale as dependências:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend retorna erro 404

**Solução**: Certifique-se que:
1. Backend está rodando em `http://localhost:8000`
2. Banco de dados existe em `/Users/hugo/Desktop/nutri saas/database.db`

Verifique:
```bash
ls -la /Users/hugo/Desktop/nutri\ saas/database.db
```

### Dados de teste não existem

**Solução**: Execute:
```bash
cd /Users/hugo/Desktop/nutri\ saas
source .venv/bin/activate
python setup_test_data.py
```

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
