"""
Endpoints FastAPI para cálculo de TMB e gasto calórico.

Fornece endpoints REST para calcular Taxa Metabólica Basal e gasto energético diário.
"""

from fastapi import APIRouter, HTTPException
from schemas.tmb import (
    TMBRequest,
    TMBResponse,
    TMBComIMCResponse,
    GastoCaloricRequest,
    GastoCaloricResponse,
    IndiceIMC,
)
from services.tmb_service import TMBService

router = APIRouter(
    prefix="/tmb",
    tags=["TMB - Taxa Metabólica Basal"],
)


@router.post(
    "/calcular",
    response_model=TMBResponse,
    status_code=200,
    summary="Calcular TMB",
    description=(
        "Calcula a Taxa Metabólica Basal usando a fórmula de Mifflin-St Jeor.\n\n"
        "A TMB é o número mínimo de calorias que o corpo necessita em repouso completo "
        "para manter funções vitais como respiração, circulação e temperatura corporal."
    ),
)
async def calcular_tmb(dados: TMBRequest) -> TMBResponse:
    """
    Calcula TMB para uma pessoa.

    **Parâmetros:**
    - peso_kg: Peso corporal em quilogramas (1-635)
    - altura_cm: Altura em centímetros (50-300)
    - idade_anos: Idade em anos (1-150)
    - sexo: Sexo biológico (M = Masculino, F = Feminino)

    **Retorna:**
    - tmb: Taxa Metabólica Basal em kcal/dia

    **Exemplo:**
    ```json
    {
      "peso_kg": 70.5,
      "altura_cm": 180,
      "idade_anos": 30,
      "sexo": "M"
    }
    ```

    **Resposta:**
    ```json
    {
      "tmb": 1662.25,
      "peso_kg": 70.5,
      "altura_cm": 180,
      "idade_anos": 30,
      "sexo": "M"
    }
    ```
    """
    try:
        tmb = TMBService.calcular_tmb(
            peso_kg=dados.peso_kg,
            altura_cm=dados.altura_cm,
            idade_anos=dados.idade_anos,
            sexo=dados.sexo,
        )

        return TMBResponse(
            tmb=tmb,
            peso_kg=dados.peso_kg,
            altura_cm=dados.altura_cm,
            idade_anos=dados.idade_anos,
            sexo=dados.sexo,
        )
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422, detail=f"Erro na validação dos dados: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao calcular TMB: {str(e)}"
        )


@router.post(
    "/calcular-com-imc",
    response_model=TMBComIMCResponse,
    status_code=200,
    summary="Calcular TMB com IMC",
    description="Calcula TMB e incluindo o Índice de Massa Corporal (IMC).",
)
async def calcular_tmb_com_imc(dados: TMBRequest) -> TMBComIMCResponse:
    """
    Calcula TMB e IMC para uma pessoa.

    Além da TMB, calcula o Índice de Massa Corporal e sua classificação.

    **Retorna também:**
    - imc: Índice de Massa Corporal
    - imc_classificacao: Classificação (Peso baixo, Normal, Sobrepeso, etc)

    **Classificações de IMC:**
    - Menor que 18.5: Peso baixo
    - 18.5 - 24.9: Peso normal
    - 25.0 - 29.9: Sobrepeso
    - 30.0 - 34.9: Obesidade grau 1
    - 35.0 - 39.9: Obesidade grau 2
    - Maior ou igual a 40.0: Obesidade grau 3
    """
    try:
        tmb = TMBService.calcular_tmb(
            peso_kg=dados.peso_kg,
            altura_cm=dados.altura_cm,
            idade_anos=dados.idade_anos,
            sexo=dados.sexo,
        )

        # Calcular IMC
        altura_m = dados.altura_cm / 100
        imc = dados.peso_kg / (altura_m ** 2)
        imc = round(imc, 2)

        # Classificar IMC
        if imc < 18.5:
            classificacao = "Peso baixo"
        elif 18.5 <= imc < 25.0:
            classificacao = "Peso normal"
        elif 25.0 <= imc < 30.0:
            classificacao = "Sobrepeso"
        elif 30.0 <= imc < 35.0:
            classificacao = "Obesidade grau 1"
        elif 35.0 <= imc < 40.0:
            classificacao = "Obesidade grau 2"
        else:
            classificacao = "Obesidade grau 3"

        return TMBComIMCResponse(
            tmb=tmb,
            peso_kg=dados.peso_kg,
            altura_cm=dados.altura_cm,
            idade_anos=dados.idade_anos,
            sexo=dados.sexo,
            imc=imc,
            imc_classificacao=classificacao,
        )
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422, detail=f"Erro na validação dos dados: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao calcular TMB e IMC: {str(e)}"
        )


@router.post(
    "/gasto-calorico",
    response_model=GastoCaloricResponse,
    status_code=200,
    summary="Calcular Gasto Calórico",
    description=(
        "Calcula o gasto energético diário total (TDEE) com base no nível de atividade "
        "e fornece cenários de déficit e superávit calórico para perda/ganho de peso."
    ),
)
async def calcular_gasto_calorico(
    dados: GastoCaloricRequest,
) -> GastoCaloricResponse:
    """
    Calcula o gasto energético diário total (TDEE).

    A TDEE é o número de calorias que o corpo queima em um dia, considerando
    o nível de atividade física. É utilizada para calcular cenários de perda
    ou ganho de peso.

    **Níveis de Atividade:**
    - sedentario: Pouco ou nenhum exercício (fator: 1.2 × TMB)
    - leve: 1-3 dias por semana de exercício (fator: 1.375 × TMB)
    - moderado: 3-5 dias por semana de exercício (fator: 1.55 × TMB)
    - intenso: 6-7 dias por semana de exercício (fator: 1.725 × TMB)
    - muito_intenso: 2x por dia ou trabalho físico (fator: 1.9 × TMB)

    **Cenários de Perda/Ganho:**
    - Déficit leve: -500 kcal (~250g de perda por semana)
    - Déficit moderado: -750 kcal (~375g de perda por semana)
    - Superávit leve: +500 kcal (~250g de ganho por semana)
    - Superávit moderado: +750 kcal (~375g de ganho por semana)

    **Exemplo:**
    ```json
    {
      "peso_kg": 70.5,
      "altura_cm": 180,
      "idade_anos": 30,
      "sexo": "M",
      "nivel_atividade": "moderado"
    }
    ```

    **Resposta:**
    ```json
    {
      "tmb": 1662.25,
      "fator_atividade": 1.55,
      "nivel_atividade": "moderado",
      "tdee": 2576.49,
      "deficit_leve": 2076.49,
      "deficit_moderado": 1826.49,
      "superavit_leve": 3076.49,
      "superavit_moderado": 3326.49,
      "peso_kg": 70.5,
      "altura_cm": 180,
      "idade_anos": 30,
      "sexo": "M"
    }
    ```
    """
    try:
        resultado = TMBService.calcular_gasto_calorico(
            peso_kg=dados.peso_kg,
            altura_cm=dados.altura_cm,
            idade_anos=dados.idade_anos,
            sexo=dados.sexo,
            nivel_atividade=dados.nivel_atividade,
        )

        return GastoCaloricResponse(
            **resultado,
            peso_kg=dados.peso_kg,
            altura_cm=dados.altura_cm,
            idade_anos=dados.idade_anos,
            sexo=dados.sexo,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=422, detail=f"Erro na validação dos dados: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao calcular gasto calórico: {str(e)}"
        )


@router.get(
    "/niveis-atividade",
    response_model=dict,
    status_code=200,
    summary="Listar Níveis de Atividade",
    description="Retorna os níveis de atividade disponíveis com suas descrições e fatores.",
)
async def listar_niveis_atividade() -> dict:
    """
    Retorna informações sobre os níveis de atividade disponíveis.

    **Descrição de Fatores:**
    - Fator = Multiplicador da TMB para calcular TDEE
    - Quanto maior a atividade, maior o fator

    **Exemplo:**
    ```json
    {
      "sedentario": {
        "descricao": "Pouco ou nenhum exercício",
        "frequencia": "0 dias por semana",
        "fator": 1.2,
        "tdee": "TMB × 1.2"
      },
      ...
    }
    ```
    """
    return {
        "sedentario": {
            "descricao": "Pouco ou nenhum exercício",
            "frequencia": "0 dias por semana",
            "fator": 1.2,
            "recomendacao": "Trabalho sedentário, sem exercício regular",
        },
        "leve": {
            "descricao": "Exercício leve",
            "frequencia": "1-3 dias por semana",
            "fator": 1.375,
            "recomendacao": "Atividade leve na maioria dos dias ou exercício leve alguns dias",
        },
        "moderado": {
            "descricao": "Exercício moderado",
            "frequencia": "3-5 dias por semana",
            "fator": 1.55,
            "recomendacao": "Exercício moderado 3-5 dias por semana",
        },
        "intenso": {
            "descricao": "Exercício intenso",
            "frequencia": "6-7 dias por semana",
            "fator": 1.725,
            "recomendacao": "Exercício intenso 6-7 dias por semana",
        },
        "muito_intenso": {
            "descricao": "Exercício muito intenso",
            "frequencia": "2x por dia ou trabalho físico",
            "fator": 1.9,
            "recomendacao": "Exercício intenso 2x por dia ou trabalho físico pesado",
        },
    }


@router.get(
    "/tabela-imc",
    response_model=dict,
    status_code=200,
    summary="Tabela de Classificação de IMC",
    description="Retorna a tabela oficial de classificação de IMC pela OMS.",
)
async def obter_tabela_imc() -> dict:
    """
    Retorna a tabela de classificação de Índice de Massa Corporal (IMC).

    Padrões definidos pela Organização Mundial de Saúde (OMS).

    **Fórmula:** IMC = peso(kg) / altura(m)²

    **Exemplo:**
    ```json
    {
      "abaixo_de_18.5": {
        "classificacao": "Peso baixo",
        "risco": "Desnutrição, osteoporose, anemia",
        "recomendacao": "Consultar nutricionista"
      },
      ...
    }
    ```
    """
    return {
        "abaixo_de_18.5": {
            "classificacao": "Peso baixo",
            "risco": "Desnutrição, osteoporose, anemia",
            "recomendacao": "Aumentar ingestão calórica e consultar nutricionista",
        },
        "18.5_a_24.9": {
            "classificacao": "Peso normal",
            "risco": "Mínimo",
            "recomendacao": "Manter hábitos saudáveis",
        },
        "25.0_a_29.9": {
            "classificacao": "Sobrepeso",
            "risco": "Aumentado para doenças crônicas",
            "recomendacao": "Perder peso através de dieta e exercício",
        },
        "30.0_a_34.9": {
            "classificacao": "Obesidade grau 1",
            "risco": "Alto para doenças crônicas",
            "recomendacao": "Consultar nutricionista e endocrinologista",
        },
        "35.0_a_39.9": {
            "classificacao": "Obesidade grau 2",
            "risco": "Muito alto",
            "recomendacao": "Acompanhamento médico e nutricional obrigatório",
        },
        "40.0_ou_mais": {
            "classificacao": "Obesidade grau 3",
            "risco": "Crítico",
            "recomendacao": "Acompanhamento médico intensivo necessário",
        },
    }
