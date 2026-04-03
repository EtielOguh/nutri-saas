"""Exemplos de uso das Schemas Pydantic."""
from datetime import datetime, timedelta
from schemas import (
    # Base
    BaseSchema,
    ErrorResponse,
    PaginatedResponse,
    # Nutricionista
    NutricionistaCreate,
    NutricionistaUpdate,
    NutricionistaResponse,
    NutricionistaDetailResponse,
    NutricionistaSimpleResponse,
    ConfiguracaoNutricionistaCreate,
    ConfiguracaoNutricionistaResponse,
    # Cliente
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteDetailResponse,
    ClienteSimpleResponse,
    # Medicao
    MedicaoCreate,
    MedicaoUpdate,
    MedicaoResponse,
    MedicaoHistoricoResponse,
    MedicaoSimpleResponse,
    # Observacao
    ObservacaoCreate,
    ObservacaoUpdate,
    ObservacaoResponse,
    ObservacaoSimpleResponse,
    # Token
    TokenAcessoClienteCreate,
    TokenAcessoClienteGenerateResponse,
    TokenValidacaoResponse,
    # Documento
    DocumentoPDFCreate,
    DocumentoPDFUpdate,
    DocumentoPDFResponse,
    DocumentoPDFBulkResponse,
)


class ExemplosNutricionista:
    """Exemplos de uso de schemas do Nutricionista."""

    @staticmethod
    def criar_nutricionista():
        """Exemplo 1: Criar novo nutricionista."""
        data = {
            "nome": "Dr. João Silva",
            "email": "joao.silva@example.com",
            "senha": "senhaSegura123!",
        }
        nutricionista = NutricionistaCreate(**data)
        print(f"✅ Nutricionista criado: {nutricionista.nome}")
        return nutricionista

    @staticmethod
    def atualizar_nutricionista():
        """Exemplo 2: Atualizar nutricionista (apenas alguns campos)."""
        # Atualização parcial - apenas nome
        update_data = {"nome": "Dr. João Silva Santos"}
        update = NutricionistaUpdate(**update_data)
        print(f"✅ Nutricionista atualizado: {update.nome}")
        return update

    @staticmethod
    def resposta_nutricionista_com_timestamps():
        """Exemplo 3: Resposta com timestamps (típico de GET)."""
        response_data = {
            "id": 1,
            "nome": "Dr. João Silva",
            "email": "joao.silva@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        response = NutricionistaResponse(**response_data)
        print(f"✅ Resposta: {response.nome} (ID: {response.id})")
        return response

    @staticmethod
    def criar_configuracao():
        """Exemplo 4: Criar configuração de nutricionista."""
        config_data = {
            "cor_primaria": "#1E90FF",
            "valor_consulta": 150.00,
            "logo_url": "https://example.com/logo.png",
        }
        config = ConfiguracaoNutricionistaCreate(**config_data)
        print(f"✅ Configuração criada: Cor {config.cor_primaria}, Valor R$ {config.valor_consulta}")
        return config

    @staticmethod
    def resposta_detalhada():
        """Exemplo 5: Resposta detalhada com total de clientes."""
        detail_data = {
            "id": 1,
            "nome": "Dr. João Silva",
            "email": "joao.silva@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "total_clientes": 15,
        }
        detail = NutricionistaDetailResponse(**detail_data)
        print(f"✅ Nutricionista {detail.nome} tem {detail.total_clientes} clientes")
        return detail


class ExemplosCliente:
    """Exemplos de uso de schemas do Cliente."""

    @staticmethod
    def criar_cliente():
        """Exemplo 1: Criar novo cliente."""
        client_data = {
            "nutricionista_id": 1,
            "nome": "João da Silva",
            "idade": 35,
            "altura": 180.0,
            "objetivo": "Perda de peso",
        }
        cliente = ClienteCreate(**client_data)
        print(f"✅ Cliente criado: {cliente.nome} ({cliente.idade} anos, {cliente.altura}cm)")
        return cliente

    @staticmethod
    def atualizar_cliente_parcial():
        """Exemplo 2: Atualizar apenas idade do cliente."""
        update_data = {"idade": 36}  # Apenas idade
        update = ClienteUpdate(**update_data)
        print(f"✅ Cliente atualizado: nova idade {update.idade}")
        return update

    @staticmethod
    def resposta_cliente_com_nutricionista():
        """Exemplo 3: Resposta com nutricionista relacionado."""
        nutricionista = {
            "id": 1,
            "nome": "Dr. João Silva",
            "email": "joao@example.com",
        }
        response_data = {
            "id": 10,
            "nutricionista_id": 1,
            "nome": "João da Silva",
            "idade": 35,
            "altura": 180.0,
            "objetivo": "Perda de peso",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "nutricionista": NutricionistaSimpleResponse(**nutricionista),
        }
        response = ClienteResponse(**response_data)
        print(f"✅ Cliente {response.nome} de {response.nutricionista.nome}")
        return response

    @staticmethod
    def resposta_detalhada():
        """Exemplo 4: Resposta detalhada com estatísticas."""
        detail_data = {
            "id": 10,
            "nutricionista_id": 1,
            "nome": "João da Silva",
            "idade": 35,
            "altura": 180.0,
            "objetivo": "Perda de peso",
            "created_at": datetime.now() - timedelta(days=90),
            "updated_at": datetime.now(),
            "total_medicoes": 12,
            "total_observacoes": 25,
            "total_documentos": 3,
            "ultimo_peso": 78.5,
            "data_ultima_medicao": datetime.now(),
        }
        detail = ClienteDetailResponse(**detail_data)
        print(f"✅ {detail.nome}: {detail.total_medicoes} medições, último peso: {detail.ultimo_peso}kg")
        return detail


class ExemplosMedicao:
    """Exemplos de uso de schemas de Medição."""

    @staticmethod
    def criar_medicao():
        """Exemplo 1: Registrar nova medição."""
        medicao_data = {
            "cliente_id": 10,
            "peso": 78.5,
        }
        medicao = MedicaoCreate(**medicao_data)
        print(f"✅ Medição criada: Cliente {medicao.cliente_id}, Peso {medicao.peso}kg")
        return medicao

    @staticmethod
    def atualizar_medicao():
        """Exemplo 2: Corrigir peso registrado."""
        update_data = {"peso": 79.0}
        update = MedicaoUpdate(**update_data)
        print(f"✅ Medição atualizada: Novo peso {update.peso}kg")
        return update

    @staticmethod
    def resposta_medicao():
        """Exemplo 3: Resposta de medição com cliente."""
        cliente = {
            "id": 10,
            "nome": "João da Silva",
        }
        medicao_data = {
            "id": 50,
            "cliente_id": 10,
            "peso": 78.5,
            "data_medicao": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "cliente": ClienteSimpleResponse(**cliente),
        }
        response = MedicaoResponse(**medicao_data)
        print(f"✅ Medição ID {response.id}: {response.peso}kg em {response.data_medicao.date()}")
        return response

    @staticmethod
    def historico_medicoes():
        """Exemplo 4: Histórico de 5 últimas medições."""
        medicoes_responses = [
            MedicaoResponse(
                id=i,
                cliente_id=10,
                peso=80.0 - (i * 0.5),
                data_medicao=datetime.now() - timedelta(days=7-i),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            for i in range(1, 6)
        ]
        historico = MedicaoHistoricoResponse(
            total=5,
            medicoes=medicoes_responses,
            variacao_total=-2.0,
            percentual_variacao=-2.5,
        )
        print(f"✅ Histórico: {historico.total} medições, variação: {historico.variacao_total}kg")
        return historico


class ExemplosObservacao:
    """Exemplos de uso de schemas de Observação."""

    @staticmethod
    def criar_observacao():
        """Exemplo 1: Registrar observação sobre cliente."""
        obs_data = {
            "cliente_id": 10,
            "texto": "Cliente apresentou bom progresso esta semana. Mantém disciplina com alimentação.",
        }
        observacao = ObservacaoCreate(**obs_data)
        print(f"✅ Observação criada: {observacao.texto[:50]}...")
        return observacao

    @staticmethod
    def atualizar_observacao():
        """Exemplo 2: Editar observação."""
        update_data = {
            "texto": "Cliente apresentou excelente progresso. Aumentar intensidade do treino.",
        }
        update = ObservacaoUpdate(**update_data)
        print(f"✅ Observação atualizada: {update.texto[:50]}...")
        return update

    @staticmethod
    def resposta_observacao():
        """Exemplo 3: Resposta com cliente."""
        obs_data = {
            "id": 1,
            "cliente_id": 10,
            "texto": "Bom progresso esta semana.",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "cliente": ClienteSimpleResponse(
                id=10,
                nome="João da Silva",
            ),
        }
        response = ObservacaoResponse(**obs_data)
        print(f"✅ Observação ao cliente {response.cliente.nome}")
        return response


class ExemplosToken:
    """Exemplos de uso de schemas de Token."""

    @staticmethod
    def criar_token():
        """Exemplo 1: Solicitar criação de token (será gerado pelo serviço)."""
        token_data = {"cliente_id": 10}
        token = TokenAcessoClienteCreate(**token_data)
        print(f"✅ Requisição de token para cliente {token.cliente_id}")
        return token

    @staticmethod
    def token_gerado():
        """Exemplo 2: Token gerado (resposta do serviço)."""
        token_data = {
            "token_unico": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "cliente_id": 10,
            "mensagem": "Token gerado com sucesso",
        }
        response = TokenAcessoClienteGenerateResponse(**token_data)
        print(f"✅ Token gerado para cliente {response.cliente_id}")
        print(f"   Token: {response.token_unico[:50]}...")
        return response

    @staticmethod
    def validacao_token():
        """Exemplo 3: Resposta ao validar token."""
        validacao_data = {
            "valido": True,
            "cliente_id": 10,
            "cliente_nome": "João da Silva",
        }
        validation = TokenValidacaoResponse(**validacao_data)
        print(f"✅ Token válido para {validation.cliente_nome}")
        return validation

    @staticmethod
    def validacao_token_expirado():
        """Exemplo 4: Token expirado."""
        validacao_data = {
            "valido": False,
            "cliente_id": None,
            "cliente_nome": None,
        }
        validation = TokenValidacaoResponse(**validacao_data)
        print(f"❌ Token inválido ou expirado")
        return validation


class ExemplosDocumento:
    """Exemplos de uso de schemas de Documento."""

    @staticmethod
    def enviar_documento():
        """Exemplo 1: Registrar envio de documento."""
        doc_data = {
            "cliente_id": 10,
            "url_pdf": "https://storage.example.com/docs/plano-nutricional-jan-2024.pdf",
        }
        documento = DocumentoPDFCreate(**doc_data)
        print(f"✅ Documento registrado: {documento.url_pdf.split('/')[-1]}")
        return documento

    @staticmethod
    def atualizar_documento():
        """Exemplo 2: Atualizar URL do documento."""
        update_data = {
            "url_pdf": "https://storage.example.com/docs/plano-nutricional-jan-2024-v2.pdf",
        }
        update = DocumentoPDFUpdate(**update_data)
        print(f"✅ Documento atualizado")
        return update

    @staticmethod
    def resposta_documento():
        """Exemplo 3: Resposta com cliente."""
        doc_data = {
            "id": 5,
            "cliente_id": 10,
            "url_pdf": "https://storage.example.com/docs/plano-nutricional-jan-2024.pdf",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "cliente": ClienteSimpleResponse(id=10, nome="João da Silva"),
        }
        response = DocumentoPDFResponse(**doc_data)
        print(f"✅ Documento para {response.cliente.nome}")
        return response

    @staticmethod
    def upload_em_lote():
        """Exemplo 4: Resposta de upload em lote."""
        bulk = DocumentoPDFBulkResponse(
            total=3,
            sucesso=3,
            erro=0,
        )
        print(f"✅ Upload em lote: {bulk.sucesso}/{bulk.total} documentos")
        return bulk

    @staticmethod
    def upload_com_erros():
        """Exemplo 5: Upload em lote com alguns erros."""
        bulk = DocumentoPDFBulkResponse(
            total=5,
            sucesso=3,
            erro=2,
            detalhes=["Documento 2: arquivo muito grande", "Documento 5: formato inválido"],
        )
        print(f"⚠️ Upload: {bulk.sucesso}/{bulk.total} OK, {bulk.erro} erros")
        return bulk


class ExemplosRespostas:
    """Exemplos de respostas comuns."""

    @staticmethod
    def erro_validacao():
        """Exemplo 1: Resposta de erro de validação."""
        erro = ErrorResponse(
            error="ValidationError",
            detail="Campo 'email' deve ser um email válido",
            status_code=422,
        )
        print(f"❌ Erro {erro.status_code}: {erro.detail}")
        return erro

    @staticmethod
    def erro_nao_encontrado():
        """Exemplo 2: Resposta de recurso não encontrado."""
        erro = ErrorResponse(
            error="NotFoundError",
            detail="Cliente com ID 999 não encontrado",
            status_code=404,
        )
        print(f"❌ Erro {erro.status_code}: {erro.detail}")
        return erro

    @staticmethod
    def lista_paginada():
        """Exemplo 3: Resposta paginada de clientes."""
        clientes = [
            ClienteSimpleResponse(
                id=i,
                nome=f"Cliente {i}",
                idade=20 + i,
                altura=170 + i,
            )
            for i in range(1, 6)
        ]
        paginated = PaginatedResponse(
            total=50,
            page=1,
            page_size=5,
            items=clientes,
        )
        print(f"✅ Página {paginated.page}: {len(paginated.items)} items de {paginated.total}")
        return paginated


def executar_todos_exemplos():
    """Executar todos os exemplos."""
    print("\n" + "="*60)
    print("EXEMPLOS DE USO DAS SCHEMAS - NUTRI SAAS")
    print("="*60 + "\n")

    # Nutricionista
    print("\n📋 EJEMPLOS - NUTRICIONISTA")
    print("-" * 60)
    ExemplosNutricionista.criar_nutricionista()
    ExemplosNutricionista.atualizar_nutricionista()
    ExemplosNutricionista.resposta_nutricionista_com_timestamps()
    ExemplosNutricionista.criar_configuracao()
    ExemplosNutricionista.resposta_detalhada()

    # Cliente
    print("\n\n👥 EJEMPLOS - CLIENTE")
    print("-" * 60)
    ExemplosCliente.criar_cliente()
    ExemplosCliente.atualizar_cliente_parcial()
    ExemplosCliente.resposta_cliente_com_nutricionista()
    ExemplosCliente.resposta_detalhada()

    # Medição
    print("\n\n⚖️ EJEMPLOS - MEDIÇÃO")
    print("-" * 60)
    ExemplosMedicao.criar_medicao()
    ExemplosMedicao.atualizar_medicao()
    ExemplosMedicao.resposta_medicao()
    ExemplosMedicao.historico_medicoes()

    # Observação
    print("\n\n📝 EJEMPLOS - OBSERVAÇÃO")
    print("-" * 60)
    ExemplosObservacao.criar_observacao()
    ExemplosObservacao.atualizar_observacao()
    ExemplosObservacao.resposta_observacao()

    # Token
    print("\n\n🔑 EJEMPLOS - TOKEN DE ACESSO")
    print("-" * 60)
    ExemplosToken.criar_token()
    ExemplosToken.token_gerado()
    ExemplosToken.validacao_token()
    ExemplosToken.validacao_token_expirado()

    # Documento
    print("\n\n📄 EJEMPLOS - DOCUMENTO PDF")
    print("-" * 60)
    ExemplosDocumento.enviar_documento()
    ExemplosDocumento.atualizar_documento()
    ExemplosDocumento.resposta_documento()
    ExemplosDocumento.upload_em_lote()
    ExemplosDocumento.upload_com_erros()

    # Respostas comuns
    print("\n\n🔄 EJEMPLOS - RESPOSTAS COMUNS")
    print("-" * 60)
    ExemplosRespostas.erro_validacao()
    ExemplosRespostas.erro_nao_encontrado()
    ExemplosRespostas.lista_paginada()

    print("\n\n" + "="*60)
    print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO")
    print("="*60 + "\n")


if __name__ == "__main__":
    executar_todos_exemplos()
