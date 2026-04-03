"""
Testes para o serviço de TMB (Taxa Metabólica Basal).

Valida a fórmula de Mifflin-St Jeor e os cálculos de gasto calórico.
"""

import pytest
from services.tmb_service import TMBService


class TestTMBService:
    """Testes para o serviço de TMB."""

    # ========== Testes de Validação ==========

    def test_calcular_tmb_homem(self):
        """Testa TMB de um homem padrão."""
        # Dados: Homem 30 anos, 70kg, 180cm
        tmb = TMBService.calcular_tmb(70, 180, 30, "M")
        # Cálculo esperado: (10×70) + (6.25×180) - (5×30) + 5 = 700 + 1125 - 150 + 5 = 1680
        assert tmb == 1680.0

    def test_calcular_tmb_mulher(self):
        """Testa TMB de uma mulher padrão."""
        # Dados: Mulher 25 anos, 65kg, 165cm
        tmb = TMBService.calcular_tmb(65, 165, 25, "F")
        # Cálculo esperado: (10×65) + (6.25×165) - (5×25) - 161 = 650 + 1031.25 - 125 - 161 = 1395.25
        assert tmb == 1395.25

    def test_calcular_tmb_sexo_minusculo(self):
        """Testa se aceita sexo em minúscula."""
        tmb_m = TMBService.calcular_tmb(70, 180, 30, "m")
        tmb_f = TMBService.calcular_tmb(65, 165, 25, "f")
        assert tmb_m == 1680.0
        assert tmb_f == 1395.25

    def test_calcular_tmb_valores_extremos_minimos(self):
        """Testa TMB com valores mínimos válidos."""
        # Valores mínimos: 1kg, 50cm, 1 ano
        tmb = TMBService.calcular_tmb(1, 50, 1, "M")
        # Cálculo: (10×1) + (6.25×50) - (5×1) + 5 = 10 + 312.5 - 5 + 5 = 322.5
        assert tmb == 322.5

    def test_calcular_tmb_valores_extremos_maximos(self):
        """Testa TMB com valores máximos válidos."""
        # Valores máximos: 635kg, 300cm, 150 anos
        tmb = TMBService.calcular_tmb(635, 300, 150, "M")
        # Cálculo: (10×635) + (6.25×300) - (5×150) + 5 = 6350 + 1875 - 750 + 5 = 7480
        assert tmb == 7480.0

    # ========== Testes de Validação de Erros ==========

    def test_calcular_tmb_peso_invalido_baixo(self):
        """Testa erro com peso muito baixo."""
        with pytest.raises(ValueError, match="peso_kg deve estar entre 1 e 635"):
            TMBService.calcular_tmb(0, 180, 30, "M")

    def test_calcular_tmb_peso_invalido_alto(self):
        """Testa erro com peso muito alto."""
        with pytest.raises(ValueError, match="peso_kg deve estar entre 1 e 635"):
            TMBService.calcular_tmb(700, 180, 30, "M")

    def test_calcular_tmb_altura_invalida_baixa(self):
        """Testa erro com altura muito baixa."""
        with pytest.raises(ValueError, match="altura_cm deve estar entre 50 e 300"):
            TMBService.calcular_tmb(70, 40, 30, "M")

    def test_calcular_tmb_altura_invalida_alta(self):
        """Testa erro com altura muito alta."""
        with pytest.raises(ValueError, match="altura_cm deve estar entre 50 e 300"):
            TMBService.calcular_tmb(70, 320, 30, "M")

    def test_calcular_tmb_idade_invalida_baixa(self):
        """Testa erro com idade muito baixa."""
        with pytest.raises(ValueError, match="idade_anos deve estar entre 1 e 150"):
            TMBService.calcular_tmb(70, 180, 0, "M")

    def test_calcular_tmb_idade_invalida_alta(self):
        """Testa erro com idade muito alta."""
        with pytest.raises(ValueError, match="idade_anos deve estar entre 1 e 150"):
            TMBService.calcular_tmb(70, 180, 200, "M")

    def test_calcular_tmb_sexo_invalido(self):
        """Testa erro com sexo inválido."""
        with pytest.raises(ValueError, match="sexo deve ser 'M' ou 'F'"):
            TMBService.calcular_tmb(70, 180, 30, "X")

    def test_calcular_tmb_tipo_peso_invalido(self):
        """Testa erro com tipo de peso inválido."""
        with pytest.raises(TypeError, match="peso_kg deve ser um número"):
            TMBService.calcular_tmb("70", 180, 30, "M")  # type: ignore

    def test_calcular_tmb_tipo_altura_invalida(self):
        """Testa erro com tipo de altura inválido."""
        with pytest.raises(TypeError, match="altura_cm deve ser um número"):
            TMBService.calcular_tmb(70, "180", 30, "M")  # type: ignore

    def test_calcular_tmb_tipo_idade_invalida(self):
        """Testa erro com tipo de idade inválido."""
        with pytest.raises(TypeError, match="idade_anos deve ser um inteiro"):
            TMBService.calcular_tmb(70, 180, 30.5, "M")  # type: ignore

    def test_calcular_tmb_tipo_sexo_invalido(self):
        """Testa erro com tipo de sexo inválido."""
        with pytest.raises(TypeError, match="sexo deve ser uma string"):
            TMBService.calcular_tmb(70, 180, 30, 123)  # type: ignore

    # ========== Testes de Gasto Calórico ==========

    def test_calcular_gasto_calorico_sedentario(self):
        """Testa cálculo de gasto calórico para pessoa sedentária."""
        resultado = TMBService.calcular_gasto_calorico(70, 180, 30, "M", "sedentario")
        
        assert resultado["tmb"] == 1680.0
        assert resultado["fator_atividade"] == 1.2
        assert resultado["nivel_atividade"] == "sedentario"
        assert resultado["tdee"] == round(1680.0 * 1.2, 2)

    def test_calcular_gasto_calorico_leve(self):
        """Testa cálculo de gasto calórico com atividade leve."""
        resultado = TMBService.calcular_gasto_calorico(70, 180, 30, "M", "leve")
        
        assert resultado["tmb"] == 1680.0
        assert resultado["fator_atividade"] == 1.375
        assert resultado["nivel_atividade"] == "leve"
        assert resultado["tdee"] == round(1680.0 * 1.375, 2)

    def test_calcular_gasto_calorico_moderado(self):
        """Testa cálculo de gasto calórico com atividade moderada."""
        resultado = TMBService.calcular_gasto_calorico(70, 180, 30, "M", "moderado")
        
        assert resultado["tmb"] == 1680.0
        assert resultado["fator_atividade"] == 1.55
        assert resultado["nivel_atividade"] == "moderado"
        assert resultado["tdee"] == round(1680.0 * 1.55, 2)

    def test_calcular_gasto_calorico_intenso(self):
        """Testa cálculo de gasto calórico com atividade intensa."""
        resultado = TMBService.calcular_gasto_calorico(70, 180, 30, "M", "intenso")
        
        assert resultado["tmb"] == 1680.0
        assert resultado["fator_atividade"] == 1.725
        assert resultado["nivel_atividade"] == "intenso"
        assert resultado["tdee"] == round(1680.0 * 1.725, 2)

    def test_calcular_gasto_calorico_muito_intenso(self):
        """Testa cálculo de gasto calórico com atividade muito intensa."""
        resultado = TMBService.calcular_gasto_calorico(70, 180, 30, "M", "muito_intenso")
        
        assert resultado["tmb"] == 1680.0
        assert resultado["fator_atividade"] == 1.9
        assert resultado["nivel_atividade"] == "muito_intenso"
        assert resultado["tdee"] == round(1680.0 * 1.9, 2)

    def test_gasto_calorico_deficit_e_superavit(self):
        """Testa cálculo de déficit e superávit calórico."""
        resultado = TMBService.calcular_gasto_calorico(70, 180, 30, "M", "moderado")
        
        tdee = resultado["tdee"]
        
        # Verificar déficits
        assert resultado["deficit_leve"] == tdee - 500
        assert resultado["deficit_moderado"] == tdee - 750
        
        # Verificar superávits
        assert resultado["superavit_leve"] == tdee + 500
        assert resultado["superavit_moderado"] == tdee + 750

    def test_calcular_gasto_calorico_nivel_invalido(self):
        """Testa erro com nível de atividade inválido."""
        with pytest.raises(ValueError, match="nivel_atividade deve ser um de"):
            TMBService.calcular_gasto_calorico(70, 180, 30, "M", "invalido")  # type: ignore

    # ========== Testes de Precisão ==========

    def test_tmb_precisao_duas_casas_decimais(self):
        """Testa se TMB retorna com 2 casas decimais."""
        tmb = TMBService.calcular_tmb(70.5, 180.3, 30, "M")
        # Verificar se tem no máximo 2 casas decimais
        assert len(str(tmb).split(".")[-1]) <= 2

    def test_gasto_calorico_precisao(self):
        """Testa precisão do cálculo de gasto calórico."""
        resultado = TMBService.calcular_gasto_calorico(70.5, 180.3, 30, "M", "moderado")
        
        # Verificar se todos os campos têm 2 casas decimais
        assert len(str(resultado["tdee"]).split(".")[-1]) <= 2
        assert len(str(resultado["deficit_leve"]).split(".")[-1]) <= 2

    # ========== Testes Comparativos ==========

    def test_tmb_mulher_vs_homem_mesmos_dados(self):
        """Testa que mulheres têm TMB menor que homens com mesmos dados."""
        tmb_homem = TMBService.calcular_tmb(70, 180, 30, "M")
        tmb_mulher = TMBService.calcular_tmb(70, 180, 30, "F")
        
        # A fórmula para mulheres tem -161 enquanto homens têm +5
        # Diferença esperada: 166
        diferenca = tmb_homem - tmb_mulher
        assert diferenca == 166.0

    def test_tmb_aumenta_com_idade(self):
        """Testa se TMB é inversamente proporcional à idade (quanto mais velho, menor).
        
        Esperado: TMB diminui conforme a idade aumenta.
        """
        tmb_30 = TMBService.calcular_tmb(70, 180, 30, "M")
        tmb_50 = TMBService.calcular_tmb(70, 180, 50, "M")
        
        assert tmb_30 > tmb_50
        diferenca = tmb_30 - tmb_50
        # Cada ano a menos, TMB aumenta em 5 kcal (coeficiente de -5 na fórmula)
        assert diferenca == 100  # 20 anos × 5

    def test_tmb_aumenta_com_peso(self):
        """Testa se TMB aumenta com maior peso corporal."""
        tmb_70kg = TMBService.calcular_tmb(70, 180, 30, "M")
        tmb_80kg = TMBService.calcular_tmb(80, 180, 30, "M")
        
        assert tmb_80kg > tmb_70kg
        diferenca = tmb_80kg - tmb_70kg
        # Cada kg a mais, TMB aumenta em 10 kcal
        assert diferenca == 100  # 10 kg × 10

    def test_tmb_aumenta_com_altura(self):
        """Testa se TMB aumenta com maior altura."""
        tmb_180cm = TMBService.calcular_tmb(70, 180, 30, "M")
        tmb_190cm = TMBService.calcular_tmb(70, 190, 30, "M")
        
        assert tmb_190cm > tmb_180cm
        diferenca = tmb_190cm - tmb_180cm
        # Cada cm a mais, TMB aumenta em 6.25 kcal
        assert diferenca == 62.5  # 10 cm × 6.25


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
