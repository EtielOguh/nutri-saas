"""Testes para endpoints de Cliente."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import app
from core.database import get_db
from models.base import Base
from models.nutricionista import Nutricionista
from models.cliente import Cliente


# Criar um banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Criar todas as tabelas
Base.metadata.create_all(bind=engine)


# Override da dependency de database para testes
def override_get_db():
    """Dependency override para usar banco em memória nos testes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def test_client():
    """Cria um cliente TestClient para testes."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Cria uma sessão de banco de dados para testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def nutricionista(db_session):
    """Cria um nutricionista de teste."""
    nutricionista = Nutricionista(
        nome="Dr. Test",
        email="test@example.com",
        senha="testpassword123",
    )
    db_session.add(nutricionista)
    db_session.commit()
    db_session.refresh(nutricionista)
    return nutricionista


class TestClienteRoutes:
    """Testes para as rotas de Cliente."""

    def test_criar_cliente(self, test_client, nutricionista):
        """Teste: Criar novo cliente."""
        cliente_data = {
            "nutricionista_id": nutricionista.id,
            "nome": "João Cliente",
            "idade": 30,
            "altura": 180.0,
            "objetivo": "Perda de peso",
        }
        
        response = test_client.post(
            f"/nutricionistas/{nutricionista.id}/clientes",
            json=cliente_data,
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Cliente"
        assert data["idade"] == 30
        assert data["nutricionista_id"] == nutricionista.id
        assert "id" in data
        assert "created_at" in data

    def test_criar_cliente_nutricionista_id_mismatch(self, test_client, nutricionista):
        """Teste: Erro ao tentar criar cliente com nutricionista_id diferente."""
        cliente_data = {
            "nutricionista_id": 999,  # ID diferente
            "nome": "João Cliente",
            "idade": 30,
            "altura": 180.0,
            "objetivo": "Perda de peso",
        }
        
        response = test_client.post(
            f"/nutricionistas/{nutricionista.id}/clientes",
            json=cliente_data,
        )
        
        assert response.status_code == 400
        assert "nutricionista" in response.json()["detail"].lower()

    def test_criar_cliente_validacao_idade(self, test_client, nutricionista):
        """Teste: Validação de idade (máximo 150)."""
        cliente_data = {
            "nutricionista_id": nutricionista.id,
            "nome": "João Cliente",
            "idade": 200,  # Inválido
            "altura": 180.0,
            "objetivo": "Perda de peso",
        }
        
        response = test_client.post(
            f"/nutricionistas/{nutricionista.id}/clientes",
            json=cliente_data,
        )
        
        assert response.status_code == 422

    def test_criar_cliente_validacao_altura(self, test_client, nutricionista):
        """Teste: Validação de altura (máximo 300cm)."""
        cliente_data = {
            "nutricionista_id": nutricionista.id,
            "nome": "João Cliente",
            "idade": 30,
            "altura": 350.0,  # Inválido
            "objetivo": "Perda de peso",
        }
        
        response = test_client.post(
            f"/nutricionistas/{nutricionista.id}/clientes",
            json=cliente_data,
        )
        
        assert response.status_code == 422

    def test_listar_clientes_vazio(self, test_client, nutricionista):
        """Teste: Listar clientes quando não há nenhum."""
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes"
        )
        
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_clientes_com_dados(self, test_client, nutricionista, db_session):
        """Teste: Listar clientes existentes."""
        # Criar alguns clientes
        for i in range(3):
            cliente = Cliente(
                nutricionista_id=nutricionista.id,
                nome=f"Cliente {i+1}",
                idade=20 + i,
                altura=170.0 + i,
                objetivo=f"Objetivo {i+1}",
            )
            db_session.add(cliente)
        db_session.commit()
        
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes"
        )
        
        assert response.status_code == 200
        clientes = response.json()
        assert len(clientes) == 3
        assert clientes[0]["nome"] == "Cliente 1"

    def test_listar_clientes_paginacao(self, test_client, nutricionista, db_session):
        """Teste: Paginação ao listar clientes."""
        # Criar 15 clientes
        for i in range(15):
            cliente = Cliente(
                nutricionista_id=nutricionista.id,
                nome=f"Cliente {i+1}",
                idade=20 + i,
                altura=170.0,
                objetivo=f"Objetivo {i+1}",
            )
            db_session.add(cliente)
        db_session.commit()
        
        # Primeira página
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes?skip=0&limit=5"
        )
        assert response.status_code == 200
        assert len(response.json()) == 5
        
        # Segunda página
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes?skip=5&limit=5"
        )
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_obter_cliente(self, test_client, nutricionista, db_session):
        """Teste: Obter detalhes de um cliente."""
        cliente = Cliente(
            nutricionista_id=nutricionista.id,
            nome="João Cliente",
            idade=30,
            altura=180.0,
            objetivo="Perda de peso",
        )
        db_session.add(cliente)
        db_session.commit()
        
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes/{cliente.id}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Cliente"
        assert data["idade"] == 30
        assert "total_medicoes" in data
        assert "total_observacoes" in data
        assert "total_documentos" in data

    def test_obter_cliente_nao_encontrado(self, test_client, nutricionista):
        """Teste: Erro ao buscar cliente inexistente."""
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes/999"
        )
        
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()

    def test_obter_cliente_nutricionista_diferente(
        self,
        test_client,
        nutricionista,
        db_session,
    ):
        """Teste: Erro ao buscar cliente de outro nutricionista."""
        # Criar outro nutricionista
        outro_nutricionista = Nutricionista(
            nome="Dr. Outro",
            email="outro@example.com",
            senha="senhaoutra123",
        )
        db_session.add(outro_nutricionista)
        db_session.flush()
        
        # Criar cliente do primeiro nutricionista
        cliente = Cliente(
            nutricionista_id=nutricionista.id,
            nome="Cliente 1",
            idade=30,
            altura=180.0,
        )
        db_session.add(cliente)
        db_session.commit()
        
        # Tentar acessar com ID do outro nutricionista
        response = test_client.get(
            f"/nutricionistas/{outro_nutricionista.id}/clientes/{cliente.id}"
        )
        
        assert response.status_code == 404

    def test_atualizar_cliente(self, test_client, nutricionista, db_session):
        """Teste: Atualizar cliente."""
        cliente = Cliente(
            nutricionista_id=nutricionista.id,
            nome="João Cliente",
            idade=30,
            altura=180.0,
            objetivo="Perda de peso",
        )
        db_session.add(cliente)
        db_session.commit()
        
        update_data = {
            "idade": 31,
            "objetivo": "Ganho de massa",
        }
        
        response = test_client.patch(
            f"/nutricionistas/{nutricionista.id}/clientes/{cliente.id}",
            json=update_data,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["idade"] == 31
        assert data["objetivo"] == "Ganho de massa"
        assert data["nome"] == "João Cliente"  # Não foi alterado

    def test_atualizar_cliente_nao_encontrado(self, test_client, nutricionista):
        """Teste: Erro ao atualizar cliente inexistente."""
        response = test_client.patch(
            f"/nutricionistas/{nutricionista.id}/clientes/999",
            json={"idade": 31},
        )
        
        assert response.status_code == 404

    def test_deletar_cliente(self, test_client, nutricionista, db_session):
        """Teste: Deletar cliente."""
        cliente = Cliente(
            nutricionista_id=nutricionista.id,
            nome="João Cliente",
            idade=30,
            altura=180.0,
        )
        db_session.add(cliente)
        db_session.commit()
        cliente_id = cliente.id
        
        response = test_client.delete(
            f"/nutricionistas/{nutricionista.id}/clientes/{cliente_id}"
        )
        
        assert response.status_code == 204
        
        # Verificar que foi deletado
        cliente_deletado = db_session.query(Cliente).filter_by(id=cliente_id).first()
        assert cliente_deletado is None

    def test_deletar_cliente_nao_encontrado(self, test_client, nutricionista):
        """Teste: Erro ao deletar cliente inexistente."""
        response = test_client.delete(
            f"/nutricionistas/{nutricionista.id}/clientes/999"
        )
        
        assert response.status_code == 404

    def test_criar_multiplos_clientes(self, test_client, nutricionista):
        """Teste: Criar múltiplos clientes e listar."""
        # Criar os dados
        clientes_data = [
            {
                "nutricionista_id": nutricionista.id,
                "nome": f"Cliente {i+1}",
                "idade": 20 + i,
                "altura": 170.0 + i,
                "objetivo": f"Objetivo {i+1}",
            }
            for i in range(5)
        ]
        
        # Criar cada cliente
        for cliente_data in clientes_data:
            response = test_client.post(
                f"/nutricionistas/{nutricionista.id}/clientes",
                json=cliente_data,
            )
            assert response.status_code == 201
        
        # Listar e verificar
        response = test_client.get(
            f"/nutricionistas/{nutricionista.id}/clientes"
        )
        assert response.status_code == 200
        assert len(response.json()) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
