"""Quick test for dashboard endpoint."""
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import uuid

from main import app
from core.database import SessionLocal, engine
from models.base import Base
from models.nutricionista import Nutricionista
from models.cliente import Cliente
from models.medicao import Medicao


def test_dashboard_endpoint():
    """Test dashboard endpoint with real data."""
    # Setup database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Create test data with unique email
        email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        nut = Nutricionista(
            nome="Dra. Test",
            email=email,
            senha_hash="hash"
        )
        db.add(nut)
        db.flush()

        # Create clients
        for i in range(3):
            cliente = Cliente(
                nome=f"Cliente {i+1}",
                idade=25 + i,
                altura=170,
                nutricionista_id=nut.id
            )
            db.add(cliente)
            db.flush()

            # Add measurements
            for dias in [30, 15, 5]:
                med = Medicao(
                    cliente_id=cliente.id,
                    peso=70.0 + dias / 10,
                    data_medicao=datetime.utcnow() - timedelta(days=dias)
                )
                db.add(med)

        db.commit()

        # Test the service directly
        from services.nutricionista_service import NutricionistaService
        service = NutricionistaService(db=db)
        
        dashboard_data = service.get_dashboard_data(nut.id)
        
        print(f"✅ Dashboard loaded successfully")
        data = dashboard_data
        print(f"   Total clientes: {data['metricas']['total_clientes']}")
        print(f"   Total medições: {data['metricas']['total_medicoes']}")
        print(f"   Média peso: {data['metricas']['media_peso']:.1f}kg")
        print(f"   Clientes ativos: {data['metricas']['num_clientes_ativos']}")
        print(f"   Clientes recentes: {len(data['clientes_recentes'])}")
        
        # Validate structure
        assert "metricas" in data
        assert "clientes_recentes" in data
        assert data['metricas']['total_clientes'] == 3
        assert data['metricas']['total_medicoes'] == 9
        
        print("\n✅ All assertions passed!")
            
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    test_dashboard_endpoint()
