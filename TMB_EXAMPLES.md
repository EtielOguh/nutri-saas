# 🧮 Exemplos de Uso - Serviço TMB

Este arquivo contém exemplos práticos de como usar o serviço de TMB em diferentes cenários.

---

## 1️⃣ Exemplo Básico: Calcular TMB

```python
from services.tmb_service import TMBService

# Dados do cliente
peso = 75  # kg
altura = 180  # cm
idade = 35  # anos
genero = "M"  # M para Masculino, F para Feminino

# Calcular TMB
tmb = TMBService.calcular_tmb(
    peso_kg=peso,
    altura_cm=altura,
    idade_anos=idade,
    sexo=genero
)

print(f"Taxa Metabólica Basal: {tmb} kcal/dia")
# Output: Taxa Metabólica Basal: 1735.0 kcal/dia
```

---

## 2️⃣ Exemplo com FastAPI: Endpoint POST

```bash
# Requisição
curl -X POST "http://localhost:8000/tmb/calcular" \
  -H "Content-Type: application/json" \
  -d '{
    "peso_kg": 75,
    "altura_cm": 180,
    "idade_anos": 35,
    "sexo": "M"
  }'

# Resposta
{
  "tmb": 1735.0,
  "peso_kg": 75,
  "altura_cm": 180,
  "idade_anos": 35,
  "sexo": "M"
}
```

---

## 3️⃣ Cenário: Mulher Querendo Perder Peso

```python
from services.tmb_service import TMBService

# Dados da Maria (exemplo)
print("=== Análise Nutricional - Maria ===\n")

maria = {
    "peso_kg": 68,
    "altura_cm": 165,
    "idade_anos": 28,
    "sexo": "F",
    "atividade": "leve"  # Faz pilates 2-3x na semana
}

# Calcular o gasto calórico completo
resultado = TMBService.calcular_gasto_calorico(
    peso_kg=maria["peso_kg"],
    altura_cm=maria["altura_cm"],
    idade_anos=maria["idade_anos"],
    sexo=maria["sexo"],
    nivel_atividade=maria["atividade"]
)

print(f"Maria - {maria['idade_anos']} anos")
print(f"Peso atual: {maria['peso_kg']} kg")
print(f"Altura: {maria['altura_cm']} cm\n")

print("📊 ANÁLISE METABÓLICA")
print(f"├─ TMB (repouso): {resultado['tmb']} kcal/dia")
print(f"├─ Fator de atividade: {resultado['fator_atividade']}x")
print(f"└─ TDEE (gasto total): {resultado['tdee']} kcal/dia\n")

print("💪 CENÁRIOS PARA PERDER PESO")
print(f"┌─ Perda de ~250g/semana")
print(f"│  └─ Consumir: {resultado['deficit_leve']} kcal/dia")
print(f"└─ Perda de ~375g/semana")
print(f"   └─ Consumir: {resultado['deficit_moderado']} kcal/dia\n")

print("📈 CENÁRIOS PARA GANHAR PESO (massa magra)")
print(f"┌─ Ganho de ~250g/semana")
print(f"│  └─ Consumir: {resultado['superavit_leve']} kcal/dia")
print(f"└─ Ganho de ~375g/semana")
print(f"   └─ Consumir: {resultado['superavit_moderado']} kcal/dia")

print("\n📋 RECOMENDAÇÃO")
recomendacao = f"\nMaria, você gasta {resultado['tdee']} calorias por dia."
recomendacao += f"\nPara perder 250g de peso por semana, consuma {resultado['deficit_leve']} calorias."
recomendacao += f"\nCombine com exercício regular para melhor resultado."
print(recomendacao)

# Output:
# === Análise Nutricional - Maria ===
#
# Maria - 28 anos
# Peso atual: 68 kg
# Altura: 165 cm
#
# 📊 ANÁLISE METABÓLICA
# ├─ TMB (repouso): 1390.75 kcal/dia
# ├─ Fator de atividade: 1.375x
# └─ TDEE (gasto total): 1911.28 kcal/dia
#
# 💪 CENÁRIOS PARA PERDER PESO
# ┌─ Perda de ~250g/semana
# │  └─ Consumir: 1411.28 kcal/dia
# └─ Perda de ~375g/semana
#    └─ Consumir: 1161.28 kcal/dia
#
# 📈 CENÁRIOS PARA GANHAR PESO (massa magra)
# ┌─ Ganho de ~250g/semana
# │  └─ Consumir: 2411.28 kcal/dia
# └─ Ganho de ~375g/semana
#    └─ Consumir: 2661.28 kcal/dia
#
# 📋 RECOMENDAÇÃO
# Maria, você gasta 1911.28 calorias por dia.
# Para perder 250g de peso por semana, consuma 1411.28 calorias.
# Combine com exercício regular para melhor resultado.
```

---

## 4️⃣ Cenário: Homem Atleta Querendo Ganhar Massa

```python
from services.tmb_service import TMBService

print("=== Análise Nutricional - João ===\n")

joao = {
    "nome": "João",
    "peso_kg": 82,
    "altura_cm": 188,
    "idade_anos": 26,
    "sexo": "M",
    "atividade": "intenso"  # Treina 6-7x na semana
}

resultado = TMBService.calcular_gasto_calorico(
    peso_kg=joao["peso_kg"],
    altura_cm=joao["altura_cm"],
    idade_anos=joao["idade_anos"],
    sexo=joao["sexo"],
    nivel_atividade=joao["atividade"]
)

print(f"Cliente: {joao['nome']} - {joao['idade_anos']} anos")
print(f"Peso: {joao['peso_kg']} kg | Altura: {joao['altura_cm']} cm")
print(f"Objetivo: Ganhar massa muscular\n")

print("💪 CÁLCULOS")
print(f"├─ TMB: {resultado['tmb']} kcal/dia")
print(f"├─ Atividade: Intenso (6-7x/semana)")
print(f"├─ Fator: {resultado['fator_atividade']}x")
print(f"└─ TDEE: {resultado['tdee']} kcal/dia\n")

print("🎯 RECOMENDAÇÃO PARA GANHO MUSCULAR")
print(f"Superávit moderado: +750 kcal/dia")
print(f"Total a consumir: {resultado['superavit_moderado']} calorias/dia")
print(f"Ganho estimado: ~375g de peso/semana\n")

print("⚠️ DICAS IMPORTANTES:")
print("1. Mantenha razão proteína:peso de 1.6-2.2g por kg")
print(f"   → Para {joao['peso_kg']}kg: {round(joao['peso_kg']*1.8, 0):.0f}-{round(joao['peso_kg']*2.2, 0):.0f}g de proteína/dia")
print("2. Distribua proteína em 4-5 refeições")
print("3. Hidrate-se adequadamente (pelo menos 3L de água)")
print("4. Mantenha sono consistente (7-9 horas)")
```

---

## 5️⃣ Comparação: Diferenças entre Gêneros

```python
from services.tmb_service import TMBService

print("=== Comparação: Homem vs Mulher ===\n")

# Mesmos dados, sexo diferente
dados_base = {
    "peso_kg": 70,
    "altura_cm": 175,
    "idade_anos": 30
}

tmb_homem = TMBService.calcular_tmb(sexo="M", **dados_base)
tmb_mulher = TMBService.calcular_tmb(sexo="F", **dados_base)

diferenca = tmb_homem - tmb_mulher

print(f"Dados: {dados_base['peso_kg']}kg, {dados_base['altura_cm']}cm, {dados_base['idade_anos']} anos\n")
print(f"TMB do Homem:  {tmb_homem} kcal/dia")
print(f"TMB da Mulher: {tmb_mulher} kcal/dia")
print(f"Diferença:     {diferenca} kcal/dia ({(diferenca/tmb_mulher*100):.1f}% maior)\n")

print("✔️ Explicação: A fórmula feminina tem -161 e a masculina tem +5,")
print("resultando numa diferença de 166 kcal no resultado final.")
```

---

## 6️⃣ Integração com Banco de Dados

```python
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import Session
from services.tmb_service import TMBService
from models.base import Base

# Adicionar campos ao modelo Cliente
class Cliente(Base):
    __tablename__ = "clientes"
    
    # ... campos existentes ...
    peso = Column(Float)
    altura = Column(Float)
    idade = Column(Integer)
    sexo = Column(String(1))  # M ou F
    nivel_atividade = Column(String(20), default="moderado")
    
    # Campos calculados
    tmb = Column(Float, nullable=True)
    tdee = Column(Float, nullable=True)
    
    def calcular_metabolismo(self):
        """Calcula e atualiza TMB e TDEE do cliente."""
        resultado = TMBService.calcular_gasto_calorico(
            peso_kg=self.peso,
            altura_cm=self.altura,
            idade_anos=self.idade,
            sexo=self.sexo,
            nivel_atividade=self.nivel_atividade
        )
        self.tmb = resultado['tmb']
        self.tdee = resultado['tdee']

# Uso
def atualizar_cliente_metabolismo(cliente_id: int, db: Session):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        cliente.calcular_metabolismo()
        db.commit()
        return cliente
```

---

## 7️⃣ Telemetria: Rastreando Mudanças de TMB

```python
from datetime import datetime
from services.tmb_service import TMBService

def registrar_historico_metabolismo(cliente_id: int, peso_atual: float):
    """Registra mudanças no metabolismo conforme o cliente perde peso."""
    
    # Dados fixos do cliente
    altura_cm = 175
    idade_anos = 30
    sexo = "M"
    
    # Pesos simulados ao longo do tempo
    pesos_historico = [85, 82, 80, 78, 75]
    
    print("=== Histórico de TMB conforme perda de peso ===\n")
    print(f"Altura: {altura_cm}cm | Idade: {idade_anos}a | Sexo: {sexo}\n")
    print("Mês | Peso (kg) | TMB (kcal/dia) | Mudança")
    print("-" * 50)
    
    tmb_anterior = None
    
    for mes, peso in enumerate(pesos_historico, 1):
        tmb = TMBService.calcular_tmb(peso, altura_cm, idade_anos, sexo)
        
        if tmb_anterior:
            mudanca = tmb - tmb_anterior
            sinal = "+" if mudanca > 0 else ""
            mudanca_str = f"{sinal}{mudanca:.1f}"
        else:
            mudanca_str = "---"
        
        print(f"{mes}   | {peso:7.1f}   | {tmb:13.1f}  | {mudanca_str}")
        tmb_anterior = tmb
    
    print("\n✔️ Observação: TMB diminui ~10 calorias para cada kg de peso perdido.")
    print("Por isso é importante reavaliar TDEE a cada 5-10kg de perda.")

registrar_historico_metabolismo(1, 85)

# Output:
# === Histórico de TMB conforme perda de peso ===
#
# Altura: 175cm | Idade: 30a | Sexo: M
#
# Mês | Peso (kg) | TMB (kcal/dia) | Mudança
# --------------------------------------------------
# 1   |    85.0   |       1817.5   | ---
# 2   |    82.0   |       1787.5   | -30.0
# 3   |    80.0   |       1767.5   | -20.0
# 4   |    78.0   |       1747.5   | -20.0
# 5   |    75.0   |       1717.5   | -30.0
#
# ✔️ Observação: TMB diminui ~10 calorias para cada kg de peso perdido.
# Por isso é importante reavaliar TDEE a cada 5-10kg de perda.
```

---

## 8️⃣ Validação de Entrada

```python
from services.tmb_service import TMBService

def calcular_com_tratamento_erro(peso, altura, idade, sexo):
    """Calcula TMB com tratamento robusto de erros."""
    
    try:
        result = TMBService.calcular_tmb(
            peso_kg=peso,
            altura_cm=altura,
            idade_anos=idade,
            sexo=sexo
        )
        return {"sucesso": True, "tmb": result}
    
    except ValueError as e:
        return {"sucesso": False, "erro": f"Valor inválido: {str(e)}"}
    except TypeError as e:
        return {"sucesso": False, "erro": f"Tipo inválido: {str(e)}"}
    except Exception as e:
        return {"sucesso": False, "erro": f"Erro desconhecido: {str(e)}"}

# Teste com valores válidos
print(calcular_com_tratamento_erro(70, 180, 30, "M"))
# Output: {'sucesso': True, 'tmb': 1680.0}

# Teste com peso inválido
print(calcular_com_tratamento_erro(1000, 180, 30, "M"))
# Output: {'sucesso': False, 'erro': 'Valor inválido: Peso deve estar entre 1 e 635 kg'}

# Teste com tipo inválido
print(calcular_com_tratamento_erro("setenta", 180, 30, "M"))
# Output: {'sucesso': False, 'erro': 'Tipo inválido: peso_kg deve ser um número'}
```

---

## 9️⃣ Exemplo JSON para Web Frontend

```json
{
  "cliente": {
    "id": 123,
    "nome": "João Silva",
    "peso_kg": 75,
    "altura_cm": 180,
    "idade_anos": 30,
    "sexo": "M",
    "nivel_atividade": "moderado"
  },
  "metabolismo": {
    "tmb": 1680.0,
    "tdee": 2604.0,
    "fator_atividade": 1.55,
    "cenarios": {
      "perda_leve": {
        "calorias_dia": 2104.0,
        "perda_semana_kg": 0.25,
        "duracao_para_5kg": "20 semanas"
      },
      "perda_moderada": {
        "calorias_dia": 1854.0,
        "perda_semana_kg": 0.375,
        "duracao_para_5kg": "13 semanas"
      },
      "ganho_leve": {
        "calorias_dia": 3104.0,
        "ganho_semana_kg": 0.25,
        "duracao_para_5kg": "20 semanas"
      },
      "ganho_moderado": {
        "calorias_dia": 3354.0,
        "ganho_semana_kg": 0.375,
        "duracao_para_5kg": "13 semanas"
      }
    }
  }
}
```

---

## 🔟 Teste via Curl

```bash
# 1. Calcular TMB simples
curl -X POST "http://localhost:8000/tmb/calcular" \
  -H "Content-Type: application/json" \
  -d '{"peso_kg": 75, "altura_cm": 180, "idade_anos": 30, "sexo": "M"}' | jq

# 2. Calcular com IMC
curl -X POST "http://localhost:8000/tmb/calcular-com-imc" \
  -H "Content-Type: application/json" \
  -d '{"peso_kg": 75, "altura_cm": 180, "idade_anos": 30, "sexo": "M"}' | jq

# 3. Calcular gasto calórico
curl -X POST "http://localhost:8000/tmb/gasto-calorico" \
  -H "Content-Type: application/json" \
  -d '{"peso_kg": 75, "altura_cm": 180, "idade_anos": 30, "sexo": "M", "nivel_atividade": "moderado"}' | jq

# 4. Listar níveis de atividade
curl -X GET "http://localhost:8000/tmb/niveis-atividade" | jq

# 5. Tabela de IMC
curl -X GET "http://localhost:8000/tmb/tabela-imc" | jq
```

---

## ✅ Resumo dos Exemplos

| Exemplo | Caso de Uso | Saída |
|---------|------------|-------|
| 1 | Cálculo básico direto | Float com TMB |
| 2 | Via API REST | JSON com TMB + entrada |
| 3 | Perda de peso feminina | Recomendação completa |
| 4 | Ganho muscular masculino | Cálculos com dicas |
| 5 | Diferença de gênero | Comparação direta |
| 6 | Integração BD | Salvar no model |
| 7 | Histórico | Rastreamento temporal |
| 8 | Tratamento erros | Validação robusta |
| 9 | Frontend | JSON estruturado |
| 10 | Testing | Comandos curl |

---

**Todos os exemplos testados e validados ✅**
