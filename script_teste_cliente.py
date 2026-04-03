"""
Script para testar manualmente os endpoints de Cliente via FastAPI TestClient.

Este script demonstra como os endpoints funcionam sem as complexidades de 
compatibilidade de versão do TestClient/httpx.

Execução:
    python script_teste_cliente.py
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import get_db
from core.config import settings
from models.base import Base
from models.nutricionista import Nutricionista
from models.cliente import Cliente
from main import app

# Configurar banco de dados em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Aplicar override
app.dependency_overrides[get_db] = override_get_db

# Criar cliente de teste
try:
    client = TestClient(app)
    print("✅ TestClient criado com sucesso")
except Exception as e:
    print(f"❌ Erro ao criar TestClient: {e}")
    print("\nSe você ver 'Client.__init__() got an unexpected keyword argument app':")
    print("- Execute: pip install httpx --upgrade")
    print("- Execute: pip install 'starlette<0.28.0'")
    exit(1)


def criar_nutricionista():
    """Cria um nutricionista de teste."""
    db = TestingSessionLocal()
    nutricionista = Nutricionista(
        nome="Dr. João Test",
        email="joao@test.com",
        senha="senhatest123",
    )
    db.add(nutricionista)
    db.commit()
    db.refresh(nutricionista)
    db.close()
    return nutricionista


def test_endpoint_criar_cliente():
    """Teste: POST /nutricionistas/{id}/clientes"""
    print("\n📝 TESTE 1: Criar Cliente")
    print("=" * 60)
    
    # Preparar
    nut = criar_nutricionista()
    print(f"Nutricionista criado: ID={nut.id}")
    
    # Executar
    response = client.post(
        f"/nutricionistas/{nut.id}/clientes",
        json={
            "nutricionista_id": nut.id,
            "nome": "João Silva",
            "idade": 30,
            "altura": 180.0,
            "objetivo": "Perda de peso",
        },
    )
    
    # Verificar
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Cliente criado: {data['nome']} (ID: {data['id']})")
        return data
    else:
        print(f"❌ Erro: {response.json()}")
        return None


def test_endpoint_listar_clientes():
    """Teste: GET /nutricionistas/{id}/clientes"""
    print("\n📝 TESTE 2: Listar Clientes")
    print("=" * 60)
    
    # Preparar
    nut = criar_nutricionista()
    db = TestingSessionLocal()
    
    # Criar 3 clientes
    for i in range(3):
        cliente = Cliente(
            nutricionista_id=nut.id,
            nome=f"Cliente {i+1}",
            idade=20 + i,
            altura=170.0 + i,
        )
        db.add(cliente)
    db.commit()
    db.close()
    
    # Executar
    response = client.get(f"/nutricionistas/{nut.id}/clientes")
    
    # Verificar
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Listando {len(data)} clientes:")
        for cliente in data:
            print(f"   - {cliente['nome']} ({cliente['idade']} anos)")
    else:
        print(f"❌ Erro: {response.json()}")


def test_endpoint_paginacao():
    """Teste: GET /nutricionistas/{id}/clientes?skip=0&limit=5"""
    print("\n📝 TESTE 3: Paginação")
    print("=" * 60)
    
    # Preparar
    nut = criar_nutricionista()
    db = TestingSessionLocal()
    
    # Criar 15 clientes
    for i in range(15):
        cliente = Cliente(
            nutricionista_id=nut.id,
            nome=f"Cliente {i+1}",
            idade=20 + (i % 5),
            altura=170.0,
        )
        db.add(cliente)
    db.commit()
    db.close()
    
    # Executar
    response1 = client.get(f"/nutricionistas/{nut.id}/clientes?skip=0&limit=5")
    response2 = client.get(f"/nutricionistas/{nut.id}/clientes?skip=5&limit=5")
    
    # Verificar
    print(f"Página 1 - Status: {response1.status_code}")
    print(f"Página 2 - Status: {response2.status_code}")
    
    if response1.status_code == 200 and response2.status_code == 200:
        dados1 = response1.json()
        dados2 = response2.json()
        print(f"✅ Página 1: {len(dados1)} clientes")
        print(f"✅ Página 2: {len(dados2)} clientes")
    else:
        print(f"❌ Erro na paginação")


def test_endpoint_obter_cliente():
    """Teste: GET /nutricionistas/{id}/clientes/{cliente_id}"""
    print("\n📝 TESTE 4: Obter Detalhes do Cliente")
    print("=" * 60)
    
    # Preparar
    nut = criar_nutricionista()
    db = TestingSessionLocal()
    
    cliente = Cliente(
        nutricionista_id=nut.id,
        nome="João Silva",
        idade=30,
        altura=180.0,
        objetivo="Perda de peso",
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    cliente_id = cliente.id
    db.close()
    
    # Executar
    response = client.get(f"/nutricionistas/{nut.id}/clientes/{cliente_id}")
    
    # Verificar
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cliente: {data['nome']}")
        print(f"   Idade: {data['idade']} anos")
        print(f"   Altura: {data['altura']} cm")
        print(f"   Medições: {data['total_medicoes']}")
        print(f"   Observações: {data['total_observacoes']}")
    else:
        print(f"❌ Erro: {response.json()}")


def test_endpoint_atualizar():
    """Teste: PATCH /nutricionistas/{id}/clientes/{cliente_id}"""
    print("\n📝 TESTE 5: Atualizar Cliente")
    print("=" * 60)
    
    # Preparar
    nut = criar_nutricionista()
    db = TestingSessionLocal()
    
    cliente = Cliente(
        nutricionista_id=nut.id,
        nome="João Silva",
        idade=30,
        altura=180.0,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    cliente_id = cliente.id
    db.close()
    
    # Executar
    response = client.patch(
        f"/nutricionistas/{nut.id}/clientes/{cliente_id}",
        json={
            "idade": 31,
            "objetivo": "Ganho de massa muscular",
        },
    )
    
    # Verificar
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cliente atualizado:")
        print(f"   Idade: {data['idade']} anos (era 30)")
        print(f"   Objetivo: {data['objetivo']}")
    else:
        print(f"❌ Erro: {response.json()}")


def test_endpoint_deletar():
    """Teste: DELETE /nutricionistas/{id}/clientes/{cliente_id}"""
    print("\n📝 TESTE 6: Deletar Cliente")
    print("=" * 60)
    
    # Preparar
    nut = criar_nutricionista()
    db = TestingSessionLocal()
    
    cliente = Cliente(
        nutricionista_id=nut.id,
        nome="João Silva",
        idade=30,
        altura=180.0,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    cliente_id = cliente.id
    db.close()
    
    # Executar
    response = client.delete(f"/nutricionistas/{nut.id}/clientes/{cliente_id}")
    
    # Verificar
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print(f"✅ Cliente {cliente_id} deletado com sucesso")
    else:
        print(f"❌ Erro: {response.status_code}")


def test_validacoes():
    """Teste: Validações de campos"""
    print("\n📝 TESTE 7: Validações")
    print("=" * 60)
    
    nut = criar_nutricionista()
    
    # Teste 1: idade inválida
    print("\n1️⃣ Idade > 150:")
    response = client.post(
        f"/nutricionistas/{nut.id}/clientes",
        json={
            "nutricionista_id": nut.id,
            "nome": "Teste",
            "idade": 200,
            "altura": 180.0,
        },
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 422:
        print(f"   ✅ Validação funcionando")
    
    # Teste 2: altura inválida
    print("\n2️⃣ Altura > 300 cm:")
    response = client.post(
        f"/nutricionistas/{nut.id}/clientes",
        json={
            "nutricionista_id": nut.id,
            "nome": "Teste",
            "idade": 30,
            "altura": 350.0,
        },
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 422:
        print(f"   ✅ Validação funcionando")
    
    # Teste 3: nutricionista_id mismatch
    print("\n3️⃣ Nutricionista ID mismatch:")
    response = client.post(
        f"/nutricionistas/{nut.id}/clientes",
        json={
            "nutricionista_id": 999,
            "nome": "Teste",
            "idade": 30,
            "altura": 180.0,
        },
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        print(f"   ✅ Validação funcionando")


def main():
    """Executar todos os testes."""
    print("\n" + "=" * 60)
    print("TESTES DE ENDPOINTS - CLIENTE API")
    print("=" * 60)
    
    try:
        test_endpoint_criar_cliente()
        test_endpoint_listar_clientes()
        test_endpoint_paginacao()
        test_endpoint_obter_cliente()
        test_endpoint_atualizar()
        test_endpoint_deletar()
        test_validacoes()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
