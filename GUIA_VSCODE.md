# 📺 Guia VS Code - Comoabrir 2 Terminais

## ✨ No VS Code (Seu Ambiente Atual)

### Você está AQUI:
```
┌─────────────────────────────────────────┐
│ VS Code - Nutri SaaS                    │
├─────────────────────────────────────────┤
│ Pastas (esquerda):                      │
│ ├── nutri saas/                         │
│ │   ├── main.py                         │
│ │   ├── requirements.txt                │
│ │   └── frontend/                       │
│ │       ├── src/                        │
│ │       └── package.json                │
│ │                                       │
│ └── Terminal (abaixo) ← CLIQUE AQUI     │
└─────────────────────────────────────────┘
```

---

## 📖 Passo a Passo Visual

### ✅ Passo 1: Abra o Terminal no VS Code

**Opção 1** (Keyboard):
```
Apertar: Ctrl + ~
```

**Opção 2** (Menu):
```
Terminal > New Terminal
```

Você verá:
```
┌────────────────────────────────────┐
│ zsh                                │
│ user@mac nutri saas % _            │
│                                    │
└────────────────────────────────────┘
```

---

### ✅ Passo 2: Terminal 1 - BACKEND

No terminal que abriu, execute:

```bash
source .venv/bin/activate
python main.py
```

Espere até ver:
```
✅ Iniciando Nutri SaaS API (v1.0.0)
✅ Servidor: http://0.0.0.0:8000
```

**NÃO FECHE ESTE TERMINAL!** (deixe rodando)

---

### ✅ Passo 3: Terminal 2 - FRONTEND

Abra um **NOVO terminal** à esquerda:

**Clique em `+` na aba do terminal:**
```
┌─────────────────────┐
│ zsh         +  🗑️   │  ← CLIQUE NO +
├─────────────────────┤
│ user@mac nutri saas │
│ % _                 │
└─────────────────────┘
```

Você terá agora **2 abas de terminal**.

---

### ✅ Passo 4: No NOVO Terminal (Terminal 2)

Execute:

```bash
cd frontend
npm run dev
```

Espere até ver:
```
✔️ VITE v5.4.21 ready in 150 ms

➜ Local: http://localhost:3000/
```

---

## 🎯 Resultado Final

Você terá **2 terminais abertos**:

```
┌────────────────────────────────────────────────┐
│ [Backend]      [Frontend] +  🗑️                │ ← Abas
├────────────────────────────────────────────────┤
│                                                │
│ ✅ Iniciando Nutri SaaS API (v1.0.0)           │
│ 🏠 Servidor: http://0.0.0.0:8000               │
│ INFO: Application startup complete             │
│                                                │
│ ← Backend rodando                              │
│ ← Não feche este!                              │
│                                                │
└────────────────────────────────────────────────┘
```

E no **outro terminal** (Frontend):

```
┌────────────────────────────────────────────────┐
│ [Backend]      [Frontend] +  🗑️                │ ← Abas
├────────────────────────────────────────────────┤
│                                                │
│ ✔️ VITE v5.4.21 ready in 150 ms                │
│                                                │
│ ➜ Local:   http://localhost:3000/              │
│                                                │
│ ← Frontend rodando                             │
│ ← Pronto para acessar!                         │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 🌐 Abra o Navegador

Digite na barra de endereço do seu navegador:

```
http://localhost:3000
```

Você verá a tela de login! 🎉

---

## 🆘 Trocar de Terminal

Para ir de um para outro, **clique na aba**:

```
Clique em [Backend] para ver os logs do backend
Clique em [Frontend] para ver os logs do frontend
```

---

## 🛑 Parar os Servidores

Quando quiser desligar:

**Terminal Backend:**
- Clique na aba `[Backend]`
- Aperte `Ctrl + C`

**Terminal Frontend:**
- Clique na aba `[Frontend]`
- Aperte `Ctrl + C`

---

## ✨ Dica Extra: Terminal Split

Se quiser ver **AMBOS os terminais ao mesmo tempo**:

Clique em qualquer terminal e arraste para cima/baixo para dividir a tela!

---

**Pronto? Agora é só rodar! 🚀**
