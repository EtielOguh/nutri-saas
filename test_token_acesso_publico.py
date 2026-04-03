"""Testes para sistema de token público de clientes."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import uuid

from core.database import get_db
from models.base import Base
from models.nutricionista import Nutricionista
from models.cliente import Cliente
from models.token_acesso import TokenAcessoCliente
from services.cliente_service import ClienteService


# Criar um banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    """Cria uma sessão de banco de dados para testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def nutricionista(db_session: Session) -> Nutricionista:
    """Cria um nutricionista para testes."""
    # Usar UUID para garantir email único em cada teste
    unique_id = str(uuid.uuid4())[:8]
    nutricionista = Nutricionista(
        nome="Dr. Silva",
        email=f"silva_{unique_id}@example.com",
        senha_hash="hashed_password_123",
    )
    db_session.add(nutricionista)
    db_session.commit()
    db_session.refresh(nutricionista)
    return nutricionista


@pytest.fixture
def cliente(db_session: Session, nutricionista: Nutricionista) -> Cliente:
    """Cria um cliente para testes."""
    cliente = Cliente(
        nome="João Silva",
        nutricionista_id=nutricionista.id,
        idade=30,
        altura=180,
        objetivo="Ganhar massa muscular",
    )
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    return cliente


class TestTokenAcessoService:
    """Testes para o serviço de token de acesso."""

    def test_gerar_token_para_cliente(self, db_session: Session, cliente: Cliente):
        """Testa geração de token para um cliente."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        db_session.refresh(token_obj)
        
        assert token_obj.cliente_id == cliente.id
        assert token_obj.token_unico == novo_token

    def test_buscar_cliente_por_token(self, db_session: Session, cliente: Cliente):
        """Testa busca de cliente pelo token."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        
        # Buscar cliente pelo token
        found_token = db_session.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.token_unico == novo_token
        ).first()
        
        assert found_token is not None
        assert found_token.cliente_id == cliente.id
        assert found_token.cliente.nome == cliente.nome

    def test_token_unico_por_cliente(self, db_session: Session, nutricionista: Nutricionista):
        """Testa que cada cliente tem apenas um token único."""
        # Criar dois clientes
        cliente1 = Cliente(
            nome="Cliente 1",
            nutricionista_id=nutricionista.id,
            idade=30,
            altura=180,
            objetivo="Objetivo 1",
        )
        cliente2 = Cliente(
            nome="Cliente 2",
            nutricionista_id=nutricionista.id,
            idade=25,
            altura=170,
            objetivo="Objetivo 2",
        )
        db_session.add(cliente1)
        db_session.add(cliente2)
        db_session.commit()
        db_session.refresh(cliente1)
        db_session.refresh(cliente2)
        
        # Criar tokens para cada cliente
        token1 = str(uuid.uuid4())
        token2 = str(uuid.uuid4())
        
        token_obj1 = TokenAcessoCliente(cliente_id=cliente1.id, token_unico=token1)
        token_obj2 = TokenAcessoCliente(cliente_id=cliente2.id, token_unico=token2)
        
        db_session.add(token_obj1)
        db_session.add(token_obj2)
        db_session.commit()
        
        # Verificar que tokens são diferentes
        assert token1 != token2
        
        # Verificar que cada token retorna o cliente correto
        found_token1 = db_session.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.token_unico == token1
        ).first()
        found_token2 = db_session.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.token_unico == token2
        ).first()
        
        assert found_token1.cliente_id == cliente1.id
        assert found_token2.cliente_id == cliente2.id

    def test_atualizar_token_cliente(self, db_session: Session, cliente: Cliente):
        """Testa atualização de token de um cliente."""
        # Criar token inicial
        token_inicial = str(uuid.uuid4())
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=token_inicial,
        )
        db_session.add(token_obj)
        db_session.commit()
        
        # Atualizar token
        novo_token = str(uuid.uuid4())
        token_obj.token_unico = novo_token
        db_session.commit()
        db_session.refresh(token_obj)
        
        # Verificar que novo token está salvo
        found_token = db_session.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.cliente_id == cliente.id
        ).first()
        
        assert found_token.token_unico == novo_token
        assert found_token.token_unico != token_inicial


class TestClienteServiceTokenComBuscaMetodo:
    """Testes do método de buscar cliente por token no ClienteService."""

    def test_get_cliente_por_token_valido(self, db_session: Session, cliente: Cliente):
        """Testa busca de cliente por token válido usando ClienteService."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        
        # Usar service para buscar
        service = ClienteService(db=db_session)
        cliente_encontrado = service.get_cliente_por_token(novo_token)
        
        assert cliente_encontrado is not None
        assert cliente_encontrado.id == cliente.id
        assert cliente_encontrado.nome == cliente.nome

    def test_get_cliente_por_token_invalido(self, db_session: Session):
        """Testa busca com token inválido."""
        service = ClienteService(db=db_session)
        cliente_encontrado = service.get_cliente_por_token("token_invalido_xyz")
        
        assert cliente_encontrado is None

    def test_get_cliente_por_token_uuid_valido_sem_registro(self, db_session: Session):
        """Testa busca com UUID válido mas sem registro no banco."""
        service = ClienteService(db=db_session)
        uuid_valido = str(uuid.uuid4())
        cliente_encontrado = service.get_cliente_por_token(uuid_valido)
        
        assert cliente_encontrado is None


class TestTokenValidacao:
    """Testes de validação de tokens."""

    def test_token_uuid_valido(self):
        """Testa que token gerado é sempre um UUID válido."""
        for _ in range(10):  # Testar 10 vezes
            novo_token = str(uuid.uuid4())
            
            try:
                resultado_uuid = uuid.UUID(novo_token)
                assert str(resultado_uuid) == novo_token
            except ValueError:
                pytest.fail(f"Token não é um UUID válido: {novo_token}")

    def test_token_nao_vazio(self, db_session: Session, cliente: Cliente):
        """Testa que token não é vazio."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        db_session.refresh(token_obj)
        
        assert len(token_obj.token_unico) > 0
        assert token_obj.token_unico.strip() != ""

    def test_token_comprimento_uuid4(self):
        """Testa que UUID v4 tem comprimento esperado."""
        novo_token = str(uuid.uuid4())
        
        # UUID v4 como string tem 36 caracteres (com hífens)
        # Formato: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assert len(novo_token) == 36
        assert novo_token.count("-") == 4


class TestTokenAcessoRelacionamento:
    """Testes do relacionamento entre TokenAcessoCliente e Cliente."""

    def test_token_relacionado_cliente(self, db_session: Session, cliente: Cliente):
        """Testa que token está relacionado ao cliente."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        db_session.refresh(token_obj)
        
        # Acessar cliente através do token
        cliente_do_token = token_obj.cliente
        assert cliente_do_token is not None
        assert cliente_do_token.id == cliente.id
        assert cliente_do_token.nome == cliente.nome
        assert cliente_do_token.idade == cliente.idade

    def test_cliente_pode_acessar_seu_token(self, db_session: Session, cliente: Cliente):
        """Testa que cliente pode acessar seu token."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        db_session.refresh(token_obj)
        
        # Recarregar cliente
        cliente_recarregado = db_session.query(Cliente).filter(
            Cliente.id == cliente.id
        ).first()
        
        # Acessar token através do cliente
        token_do_cliente = cliente_recarregado.token_acesso
        assert token_do_cliente is not None
        assert token_do_cliente.token_unico == novo_token

    def test_deletar_cliente_deleta_token(self, db_session: Session, cliente: Cliente):
        """Testa que deletar cliente também deleta seu token (CASCADE)."""
        novo_token = str(uuid.uuid4())
        
        token_obj = TokenAcessoCliente(
            cliente_id=cliente.id,
            token_unico=novo_token,
        )
        db_session.add(token_obj)
        db_session.commit()
        token_id = token_obj.id
        
        # Verificar que token existe
        token_encontrado = db_session.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.id == token_id
        ).first()
        assert token_encontrado is not None
        
        # Deletar cliente
        db_session.delete(cliente)
        db_session.commit()
        
        # Verificar que token foi deletado (CASCADE)
        token_encontrado_apos = db_session.query(TokenAcessoCliente).filter(
            TokenAcessoCliente.id == token_id
        ).first()
        assert token_encontrado_apos is None


class TestTokenDataset:
    """Testes de dataset completo com múltiplos clientes e tokens."""

    def test_16_clientes_com_tokens(self, db_session: Session, nutricionista: Nutricionista):
        """Testa dataset com 16 clientes e seus tokens."""
        clientes_criados = []
        tokens_criados = {}
        
        # Criar 16 clientes
        for i in range(16):
            cliente = Cliente(
                nome=f"Cliente {i+1}",
                nutricionista_id=nutricionista.id,
                idade=20 + i,
                altura=160 + (i % 30),
                objetivo=f"Objetivo {i+1}",
            )
            db_session.add(cliente)
            db_session.flush()  # Para obter ID sem commitar
            clientes_criados.append(cliente)
        
        db_session.commit()
        
        # Criar token para cada cliente
        for cliente in clientes_criados:
            novo_token = str(uuid.uuid4())
            token_obj = TokenAcessoCliente(
                cliente_id=cliente.id,
                token_unico=novo_token,
            )
            db_session.add(token_obj)
            tokens_criados[cliente.id] = novo_token
        
        db_session.commit()
        
        # Verificar que todos os tokens foram criados para este nutricionista
        total_tokens_nutricionista = (
            db_session.query(TokenAcessoCliente)
            .join(Cliente)
            .filter(Cliente.nutricionista_id == nutricionista.id)
            .count()
        )
        assert total_tokens_nutricionista == 16
        
        # Verificar que cada token retorna o cliente correto
        service = ClienteService(db=db_session)
        for cliente_id, token in tokens_criados.items():
            cliente_encontrado = service.get_cliente_por_token(token)
            assert cliente_encontrado is not None
            assert cliente_encontrado.id == cliente_id
