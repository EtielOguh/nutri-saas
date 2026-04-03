"""Testes para todas as schemas Pydantic."""

import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

# Base schemas
from schemas import (
    BaseSchema,
    TimestampSchema,
    ErrorResponse,
    PaginatedResponse,
)

# Nutricionista schemas
from schemas import (
    NutricionistaCreate,
    NutricionistaUpdate,
    NutricionistaResponse,
    NutricionistaSimpleResponse,
    NutricionistaDetailResponse,
    ConfiguracaoNutricionistaCreate,
    ConfiguracaoNutricionistaResponse,
)

# Cliente schemas
from schemas import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteSimpleResponse,
    ClienteDetailResponse,
)

# Medicao schemas
from schemas import (
    MedicaoCreate,
    MedicaoUpdate,
    MedicaoResponse,
    MedicaoHistoricoResponse,
    MedicaoSimpleResponse,
)

# Observacao schemas
from schemas import (
    ObservacaoCreate,
    ObservacaoUpdate,
    ObservacaoResponse,
    ObservacaoSimpleResponse,
)

# Token schemas
from schemas import (
    TokenAcessoClienteCreate,
    TokenAcessoClienteResponse,
    TokenValidacaoResponse,
)

# Documento schemas
from schemas import (
    DocumentoPDFCreate,
    DocumentoPDFUpdate,
    DocumentoPDFResponse,
    DocumentoPDFBulkResponse,
)


class TestNutricionistaSchemas:
    """Testes para schemas do Nutricionista."""

    def test_nutricionista_create_valid(self):
        """Teste criar nutricionista com dados válidos."""
        data = {
            "nome": "Dr. João Silva",
            "email": "joao@example.com",
            "senha": "senhaSegura123",
        }
        nutricionista = NutricionistaCreate(**data)
        assert nutricionista.nome == "Dr. João Silva"
        assert nutricionista.email == "joao@example.com"

    def test_nutricionista_create_email_invalid(self):
        """Teste criar nutricionista com email inválido."""
        data = {
            "nome": "Dr. João Silva",
            "email": "email_invalido",
            "senha": "senhaSegura123",
        }
        with pytest.raises(ValidationError) as exc_info:
            NutricionistaCreate(**data)
        assert "email" in str(exc_info.value).lower()

    def test_nutricionista_create_password_too_short(self):
        """Teste criar nutricionista com senha curta."""
        data = {
            "nome": "Dr. João Silva",
            "email": "joao@example.com",
            "senha": "short",
        }
        with pytest.raises(ValidationError):
            NutricionistaCreate(**data)

    def test_nutricionista_update_partial(self):
        """Teste atualização parcial de nutricionista."""
        data = {
            "nome": "Dr. Novo Nome",
        }
        update = NutricionistaUpdate(**data)
        assert update.nome == "Dr. Novo Nome"
        assert update.email is None

    def test_configuracao_nutricionista_create(self):
        """Teste criar configuração de nutricionista."""
        data = {
            "cor_primaria": "#FF5733",
            "valor_consulta": 150.00,
        }
        config = ConfiguracaoNutricionistaCreate(**data)
        assert config.cor_primaria == "#FF5733"
        assert config.valor_consulta == 150.00

    def test_configuracao_nutricionista_invalid_color(self):
        """Teste cor hexadecimal inválida."""
        data = {
            "nutricionista_id": 1,
            "cor_primaria": "XXXXXX",  # Inválido
            "cor_secundaria": "#33FF57",
            "notificacoes_ativadas": True,
            "timezone": "America/Sao_Paulo",
            "idioma": "PT-BR",
            "tema": "dark",
        }
        with pytest.raises(ValidationError):
            ConfiguracaoNutricionistaCreate(**data)

    def test_nutricionista_simple_response(self):
        """Teste resposta simples do nutricionista (sem relacionamentos)."""
        data = {
            "id": 1,
            "nome": "Dr. João Silva",
            "email": "joao@example.com",
            "crn": "123456",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        response = NutricionistaSimpleResponse(**data)
        assert response.id == 1
        assert response.nome == "Dr. João Silva"


class TestClienteSchemas:
    """Testes para schemas do Cliente."""

    def test_cliente_create_valid(self):
        """Teste criar cliente com dados válidos."""
        data = {
            "nutricionista_id": 1,
            "nome": "João Cliente",
            "idade": 30,
            "altura": 180,
            "objetivo": "Emagrecimento",
        }
        cliente = ClienteCreate(**data)
        assert cliente.nome == "João Cliente"
        assert cliente.idade == 30
        assert cliente.altura == 180

    def test_cliente_create_age_invalid(self):
        """Teste criar cliente com idade inválida."""
        data = {
            "nutricionista_id": 1,
            "nome": "João Cliente",
            "idade": 200,  # Inválido (> 150)
            "altura": 180,
            "objetivo": "Emagrecimento",
        }
        with pytest.raises(ValidationError):
            ClienteCreate(**data)

    def test_cliente_update_partial(self):
        """Teste atualização parcial de cliente."""
        data = {"idade": 31}
        update = ClienteUpdate(**data)
        assert update.idade == 31
        assert update.nome is None

    def test_cliente_height_validation(self):
        """Teste validação de altura (máximo 300cm)."""
        data = {
            "nutricionista_id": 1,
            "nome": "Cliente Alto",
            "idade": 25,
            "altura": 350,  # Muito alto (> 300)
            "objetivo": "Ganho de massa",
        }
        with pytest.raises(ValidationError):
            ClienteCreate(**data)


class TestMedicaoSchemas:
    """Testes para schemas de Medicao."""

    def test_medicao_create_valid(self):
        """Teste criar medição com dados válidos."""
        data = {
            "cliente_id": 1,
            "peso": 75.5,
        }
        medicao = MedicaoCreate(**data)
        assert medicao.peso == 75.5
        assert medicao.cliente_id == 1

    def test_medicao_weight_validation(self):
        """Teste validação de peso."""
        data = {
            "cliente_id": 1,
            "peso": 1500,  # Muito pesado (> 1000)
        }
        with pytest.raises(ValidationError):
            MedicaoCreate(**data)

    def test_medicao_zero_weight_validation(self):
        """Teste validação de peso zero."""
        data = {
            "cliente_id": 1,
            "peso": 0,  # Inválido (deve ser > 0)
        }
        with pytest.raises(ValidationError):
            MedicaoCreate(**data)

    def test_medicao_historico_response(self):
        """Teste resposta histórico de medições."""
        medicoes_data = [
            {
                "id": 1,
                "cliente_id": 1,
                "peso": 75.5,
                "data_medicao": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ]
        medicoes_response = [MedicaoResponse(**m) for m in medicoes_data]
        data = {
            "total": 1,
            "medicoes": medicoes_response,
            "variacao_total": 2.5,
        }
        historico = MedicaoHistoricoResponse(**data)
        assert historico.total == 1
        assert len(historico.medicoes) == 1
        assert historico.variacao_total == 2.5


class TestObservacaoSchemas:
    """Testes para schemas de Observacao."""

    def test_observacao_create_valid(self):
        """Teste criar observação com dados válidos."""
        data = {
            "cliente_id": 1,
            "texto": "Cliente apresentou bom progresso na perda de peso.",
        }
        observacao = ObservacaoCreate(**data)
        assert observacao.texto == "Cliente apresentou bom progresso na perda de peso."

    def test_observacao_content_required(self):
        """Teste que texto é obrigatório."""
        data = {
            "cliente_id": 1,
            # Falta texto
        }
        with pytest.raises(ValidationError):
            ObservacaoCreate(**data)


class TestTokenSchemas:
    """Testes para schemas de Token."""

    def test_token_create_valid(self):
        """Teste criar token com dados válidos."""
        data = {
            "cliente_id": 1,
        }
        token = TokenAcessoClienteCreate(**data)
        assert token.cliente_id == 1

    def test_token_generate_response(self):
        """Teste resposta ao gerar token."""
        from schemas import TokenAcessoClienteGenerateResponse
        data = {
            "token_unico": "abc123def456ghi789klm",
            "cliente_id": 1,
        }
        response = TokenAcessoClienteGenerateResponse(**data)
        assert response.token_unico == "abc123def456ghi789klm"
        assert response.cliente_id == 1

    def test_token_validation_response(self):
        """Teste resposta de validação de token."""
        data = {
            "valido": True,
            "cliente_id": 1,
            "expiracao": datetime.now() + timedelta(days=30),
        }
        validation = TokenValidacaoResponse(**data)
        assert validation.valido is True
        assert validation.cliente_id == 1


class TestDocumentoSchemas:
    """Testes para schemas de Documento PDF."""

    def test_documento_create_valid(self):
        """Teste criar documento com dados válidos."""
        data = {
            "cliente_id": 1,
            "url_pdf": "https://storage.example.com/docs/documento.pdf",
        }
        documento = DocumentoPDFCreate(**data)
        assert documento.url_pdf == "https://storage.example.com/docs/documento.pdf"

    def test_documento_update_partial(self):
        """Teste atualização parcial de documento."""
        data = {
            "url_pdf": "https://storage.example.com/docs/novo_documento.pdf"
        }
        update = DocumentoPDFUpdate(**data)
        assert update.url_pdf == "https://storage.example.com/docs/novo_documento.pdf"

    def test_documento_bulk_response(self):
        """Teste resposta bulk de documentos."""
        docs = [
            {
                "id": 1,
                "cliente_id": 1,
                "url_pdf": "https://storage.example.com/doc1.pdf",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "id": 2,
                "cliente_id": 1,
                "url_pdf": "https://storage.example.com/doc2.pdf",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        ]
        bulk_response = DocumentoPDFBulkResponse(
            total=2,
            sucesso=2,
            erro=0,
        )
        assert bulk_response.total == 2
        assert bulk_response.sucesso == 2


class TestBaseSchemas:
    """Testes para schemas base."""

    def test_error_response(self):
        """Teste schema de erro."""
        error = ErrorResponse(
            error="ValidationError",
            message="Campo obrigatório ausente",
            status_code=400,
        )
        assert error.error == "ValidationError"
        assert error.status_code == 400

    def test_paginated_response(self):
        """Teste schema de paginação."""
        paginated = PaginatedResponse(
            total=100,
            page=1,
            page_size=10,
            items=["item1", "item2"],
        )
        assert paginated.total == 100
        assert paginated.page == 1
        assert len(paginated.items) == 2


class TestSchemaIntegration:
    """Testes de integração entre schemas."""

    def test_nutricionista_simple_in_cliente(self):
        """Teste nutricionista simples dentro de cliente."""
        nutricionista_data = {
            "id": 1,
            "nome": "Dr. João",
            "email": "joao@example.com",
            "crn": "123456",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        nutricionista = NutricionistaSimpleResponse(**nutricionista_data)

        cliente_data = {
            "id": 1,
            "nutricionista_id": 1,
            "nome": "Cliente João",
            "email": "cliente@example.com",
            "idade": 30,
            "altura": 180,
            "meta_peso": 75.0,
            "notas": "Test",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "nutricionista": nutricionista,  # Relacionamento
        }
        cliente = ClienteResponse(**cliente_data)
        assert cliente.nutricionista.nome == "Dr. João"

    def test_medicao_list_response(self):
        """Teste lista de medições."""
        medicoes_data = [
            {
                "id": 1,
                "cliente_id": 1,
                "peso": 75.0,
                "data_medicao": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "id": 2,
                "cliente_id": 1,
                "peso": 74.5,
                "data_medicao": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        ]
        medicoes = [MedicaoResponse(**m) for m in medicoes_data]
        assert len(medicoes) == 2
        assert medicoes[0].peso == 75.0
        assert medicoes[1].peso == 74.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
