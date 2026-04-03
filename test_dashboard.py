"""Testes para o dashboard do nutricionista."""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.nutricionista import Nutricionista, ConfiguracaoNutricionista
from models.cliente import Cliente
from models.medicao import Medicao
from services.nutricionista_service import NutricionistaService
from core.database import SessionLocal, engine, init_db
from models.base import Base


# Setup para testes
@pytest.fixture(scope="function")
def db():
    """Cria banco de dados de teste."""
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    yield db
    
    db.close()
    
    # Limpar banco
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def nutricionista(db: Session):
    """Cria um nutricionista de teste."""
    nut = Nutricionista(
        nome="Dra. Maria Silva",
        email="maria.silva@teste.com",
        senha_hash="senha_hash_segura",
    )
    db.add(nut)
    db.commit()
    db.refresh(nut)
    
    return nut


@pytest.fixture
def clientes_com_medicoes(db: Session, nutricionista: Nutricionista):
    """Cria clientes com medições de teste."""
    clientes = []
    
    # Criar 5 clientes
    for i in range(1, 6):
        cliente = Cliente(
            nome=f"Cliente {i}",
            idade=25 + i,
            altura=170 + i,
            objetivo="Perder peso",
            nutricionista_id=nutricionista.id,
        )
        db.add(cliente)
        db.flush()
        
        # Adicionar medições (últimas 3 meses)
        for dias_atras in [90, 60, 30, 15]:
            medicao = Medicao(
                cliente_id=cliente.id,
                peso=80.0 + dias_atras / 10,
                data_medicao=datetime.utcnow() - timedelta(days=dias_atras),
            )
            db.add(medicao)
        
        clientes.append(cliente)
    
    db.commit()
    for cliente in clientes:
        db.refresh(cliente)
    
    return clientes


class TestDashboardQueries:
    """Testes para queries eficientes do dashboard."""

    def test_dashboard_data_structure(self, db: Session, nutricionista: Nutricionista, clientes_com_medicoes):
        """Verifica que get_dashboard_data retorna estrutura correta."""
        service = NutricionistaService(db=db)
        
        dashboard = service.get_dashboard_data(nutricionista.id)
        
        # Verificar estrutura
        assert "nutricionista_id" in dashboard
        assert "nome" in dashboard
        assert "email" in dashboard
        assert "metricas" in dashboard
        assert "clientes_recentes" in dashboard
        assert "configuracao" in dashboard

    def test_dashboard_metricas(self, db: Session, nutricionista: Nutricionista, clientes_com_medicoes):
        """Verifica que métricas são calculadas corretamente."""
        service = NutricionistaService(db=db)
        
        dashboard = service.get_dashboard_data(nutricionista.id)
        metricas = dashboard["metricas"]
        
        # 5 clientes
        assert metricas["total_clientes"] == 5
        
        # 4 medições por cliente = 20 medições
        assert metricas["total_medicoes"] == 20
        
        # Todos os clientes têm medições no último mês
        assert metricas["num_clientes_ativos"] >= 5
        
        # Média de peso deve ser um número válido
        assert metricas["media_peso"] is not None
        assert isinstance(metricas["media_peso"], float)
        assert metricas["media_peso"] > 0

    def test_dashboard_clientes_recentes(self, db: Session, nutricionista: Nutricionista, clientes_com_medicoes):
        """Verifica que clientes recentes são retornados em ordem."""
        service = NutricionistaService(db=db)
        
        dashboard = service.get_dashboard_data(nutricionista.id)
        clientes_recentes = dashboard["clientes_recentes"]
        
        # Deve retornar até 5 clientes
        assert len(clientes_recentes) <= 5
        
        # Cada cliente deve ter os campos esperados
        for cliente in clientes_recentes:
            assert "id" in cliente
            assert "nome" in cliente
            assert "idade" in cliente
            assert "objetivo" in cliente
            assert "ultima_medicao" in cliente
            assert "data_ultima_medicao" in cliente

    def test_dashboard_nutricionista_nao_existe(self, db: Session):
        """Verifica erro quando nutricionista não existe."""
        service = NutricionistaService(db=db)
        
        with pytest.raises(ValueError, match="Nutricionista com ID 999 não encontrado"):
            service.get_dashboard_data(999)

    def test_dashboard_sem_medicoes(self, db: Session):
        """Verifica dashboard de nutricionista sem medições."""
        # Criar nutricionista sem clientes/medições
        nut = Nutricionista(
            nome="Dr. João",
            email="joao@teste.com",
            senha_hash="hash",
        )
        db.add(nut)
        db.commit()
        db.refresh(nut)
        
        service = NutricionistaService(db=db)
        dashboard = service.get_dashboard_data(nut.id)
        
        metricas = dashboard["metricas"]
        assert metricas["total_clientes"] == 0
        assert metricas["total_medicoes"] == 0
        assert metricas["media_peso"] is None
        assert metricas["num_clientes_ativos"] == 0
        assert len(dashboard["clientes_recentes"]) == 0

    def test_dashboard_ordenacao_clientes(self, db: Session, nutricionista: Nutricionista, clientes_com_medicoes):
        """Verifica que clientes são ordenados por data de medição recente."""
        service = NutricionistaService(db=db)
        
        dashboard = service.get_dashboard_data(nutricionista.id)
        clientes_recentes = dashboard["clientes_recentes"]
        
        # Verificar que estão ordenados (primeira tem medição mais recente)
        if len(clientes_recentes) > 1:
            for i in range(len(clientes_recentes) - 1):
                data_i = clientes_recentes[i]["data_ultima_medicao"]
                data_i_next = clientes_recentes[i + 1]["data_ultima_medicao"]
                
                # Se ambas existem, a primeira deve ser mais recente
                if data_i and data_i_next:
                    assert data_i >= data_i_next


class TestDashboardSchema:
    """Testes para validação do schema."""

    def test_schema_validates(self, db: Session, nutricionista: Nutricionista, clientes_com_medicoes):
        """Verifica que schema valida dados do dashboard."""
        from schemas.nutricionista import DashboardNutricionistaResponse
        
        service = NutricionistaService(db=db)
        dashboard = service.get_dashboard_data(nutricionista.id)
        
        # Deve validar sem erros
        response = DashboardNutricionistaResponse.model_validate(dashboard)
        
        assert response.nutricionista_id == nutricionista.id
        assert response.nome == nutricionista.nome
        assert response.metricas.total_clientes == 5

    def test_schema_serialization(self, db: Session, nutricionista: Nutricionista, clientes_com_medicoes):
        """Verifica que schema pode ser serializado para JSON."""
        from schemas.nutricionista import DashboardNutricionistaResponse
        import json
        
        service = NutricionistaService(db=db)
        dashboard = service.get_dashboard_data(nutricionista.id)
        
        response = DashboardNutricionistaResponse.model_validate(dashboard)
        
        # Deve serializar sem erros
        json_str = response.model_dump_json()
        data = json.loads(json_str)
        
        assert data["nutricionista_id"] == nutricionista.id
        assert data["metricas"]["total_clientes"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
