"""
Serviço para cálculo de TMB (Taxa Metabólica Basal).

Implementa a fórmula de Mifflin-St Jeor para cálculo da taxa metabólica basal,
que é o número de calorias que o corpo necessita em repouso completo.

Referência: https://en.wikipedia.org/wiki/Basal_metabolic_rate
"""

from typing import Literal
from pydantic import ValidationError


class TMBService:
    """Serviço para cálculo de Taxa Metabólica Basal (TMB)."""

    @staticmethod
    def calcular_tmb(
        peso_kg: float,
        altura_cm: float,
        idade_anos: int,
        sexo: Literal["M", "F"],
    ) -> float:
        """
        Calcula a Taxa Metabólica Basal usando a fórmula de Mifflin-St Jeor.

        A TMB é a quantidade mínima de calorias que o corpo necessita em repouso
        completo para manter funções vitais como respiração, circulação e
        manutenção da temperatura corporal.

        Args:
            peso_kg: Peso corporal em quilogramas (1-635 kg)
            altura_cm: Altura en centímetros (50-300 cm)
            idade_anos: Idade em anos (1-150 anos)
            sexo: Sexo biológico ("M" para masculino, "F" para feminino)

        Returns:
            float: TMB em kcal/dia

        Raises:
            ValueError: Se os valores estiverem fora do intervalo esperado
            TypeError: Se os tipos de dados forem inválidos

        Examples:
            >>> tmb = TMBService.calcular_tmb(70, 180, 30, "M")
            >>> print(f"TMB: {tmb:.2f} kcal/dia")
            TMB: 1662.25 kcal/dia

            >>> tmb = TMBService.calcular_tmb(65, 165, 25, "F")
            >>> print(f"TMB: {tmb:.2f} kcal/dia")
            TMB: 1415.25 kcal/dia

        Notes:
            Fórmula de Mifflin-St Jeor:
            - Homens: TMB = (10 × peso) + (6.25 × altura) - (5 × idade) + 5
            - Mulheres: TMB = (10 × peso) + (6.25 × altura) - (5 × idade) - 161

            A fórmula foi desenvolvida em 1990 e é considerada uma das mais
            precisas para cálculo de TMB em populações caucasianas.
        """
        # Validar tipos de dados
        if not isinstance(peso_kg, (int, float)):
            raise TypeError(f"peso_kg deve ser um número, recebido: {type(peso_kg)}")
        if not isinstance(altura_cm, (int, float)):
            raise TypeError(f"altura_cm deve ser um número, recebido: {type(altura_cm)}")
        if not isinstance(idade_anos, int):
            raise TypeError(f"idade_anos deve ser um inteiro, recebido: {type(idade_anos)}")
        if not isinstance(sexo, str):
            raise TypeError(f"sexo deve ser uma string, recebido: {type(sexo)}")

        # Converter sexo para maiúscula para aceitar ambos os casos
        sexo = sexo.upper()
        if sexo not in ("M", "F"):
            raise ValueError(f"sexo deve ser 'M' ou 'F', recebido: '{sexo}'")

        # Validar intervalos de valores
        if not (1 <= peso_kg <= 635):
            raise ValueError(
                f"peso_kg deve estar entre 1 e 635 kg, recebido: {peso_kg}"
            )
        if not (50 <= altura_cm <= 300):
            raise ValueError(
                f"altura_cm deve estar entre 50 e 300 cm, recebido: {altura_cm}"
            )
        if not (1 <= idade_anos <= 150):
            raise ValueError(
                f"idade_anos deve estar entre 1 e 150 anos, recebido: {idade_anos}"
            )

        # Fórmula de Mifflin-St Jeor
        base_tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * idade_anos)

        # Adicionar fator baseado no sexo
        if sexo == "M":
            tmb = base_tmb + 5
        else:  # sexo == "F"
            tmb = base_tmb - 161

        # Arredondar para 2 casas decimais
        return round(tmb, 2)

    @staticmethod
    def calcular_gasto_calorico(
        peso_kg: float,
        altura_cm: float,
        idade_anos: int,
        sexo: Literal["M", "F"],
        nivel_atividade: Literal["sedentario", "leve", "moderado", "intenso", "muito_intenso"],
    ) -> dict:
        """
        Calcula o gasto calórico total com base no nível de atividade.

        Utiliza a TMB calculada e a multiplica pelo fator de atividade (TDEE -
        Total Daily Energy Expenditure).

        Args:
            peso_kg: Peso corporal em quilogramas
            altura_cm: Altura em centímetros
            idade_anos: Idade em anos
            sexo: Sexo biológico ("M" ou "F")
            nivel_atividade: Nível de atividade física

        Returns:
            dict com as seguintes chaves:
            - tmb: Taxa Metabólica Basal em kcal/dia
            - fator_atividade: Multiplicador utilizado
            - tdee: Gasto energético diário total em kcal/dia
            - deficit_leve: Calorias para perda leve (500 kcal/dia)
            - deficit_moderado: Calorias para perda moderada (750 kcal/dia)
            - super_avit_leve: Calorias para ganho leve (500 kcal/dia)
            - super_avit_moderado: Calorias para ganho moderado (750 kcal/dia)

        Raises:
            ValueError: Se o nível de atividade for inválido
        """
        # Fatores de atividade (Harris-Benedict)
        fatores_atividade = {
            "sedentario": 1.2,        # Pouco ou nenhum exercício
            "leve": 1.375,            # 1-3 dias por semana de exercício
            "moderado": 1.55,         # 3-5 dias por semana de exercício
            "intenso": 1.725,         # 6-7 dias por semana de exercício
            "muito_intenso": 1.9,     # Exercício intenso 2x por dia ou trabalho físico
        }

        if nivel_atividade not in fatores_atividade:
            raise ValueError(
                f"nivel_atividade deve ser um de {list(fatores_atividade.keys())}, "
                f"recebido: '{nivel_atividade}'"
            )

        # Calcular TMB
        tmb = TMBService.calcular_tmb(peso_kg, altura_cm, idade_anos, sexo)

        # Obter fator de atividade
        fator = fatores_atividade[nivel_atividade]

        # Calcular TDEE (Total Daily Energy Expenditure)
        tdee = round(tmb * fator, 2)

        # Calcular cenários de déficit e superávit calórico
        deficit_leve = round(tdee - 500, 2)
        deficit_moderado = round(tdee - 750, 2)
        superavit_leve = round(tdee + 500, 2)
        superavit_moderado = round(tdee + 750, 2)

        return {
            "tmb": tmb,
            "fator_atividade": fator,
            "nivel_atividade": nivel_atividade,
            "tdee": tdee,
            "deficit_leve": deficit_leve,
            "deficit_moderado": deficit_moderado,
            "superavit_leve": superavit_leve,
            "superavit_moderado": superavit_moderado,
        }


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo 1: Homem de 30 anos, 70kg, 180cm
    tmb_homem = TMBService.calcular_tmb(peso_kg=70, altura_cm=180, idade_anos=30, sexo="M")
    print(f"TMB Homem: {tmb_homem} kcal/dia")

    # Exemplo 2: Mulher de 25 anos, 65kg, 165cm
    tmb_mulher = TMBService.calcular_tmb(peso_kg=65, altura_cm=165, idade_anos=25, sexo="F")
    print(f"TMB Mulher: {tmb_mulher} kcal/dia")

    # Exemplo 3: Gasto calórico com nível de atividade
    print("\n=== Gasto Calórico por Nível de Atividade (Homem 70kg, 30 anos) ===")
    for nivel in ["sedentario", "leve", "moderado", "intenso", "muito_intenso"]:
        resultado = TMBService.calcular_gasto_calorico(
            peso_kg=70,
            altura_cm=180,
            idade_anos=30,
            sexo="M",
            nivel_atividade=nivel,
        )
        print(f"\n{nivel.upper()}:")
        print(f"  TMB: {resultado['tmb']} kcal/dia")
        print(f"  TDEE: {resultado['tdee']} kcal/dia")
        print(f"  Perda leve: {resultado['deficit_leve']} kcal/dia")
        print(f"  Ganho leve: {resultado['superavit_leve']} kcal/dia")
