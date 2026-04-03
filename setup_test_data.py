"""Script para criar dados de teste no banco de dados."""
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.nutricionista import Nutricionista, ConfiguracaoNutricionista
from models.cliente import Cliente
from services.auth_service import AuthService
import uuid


def criar_dados_teste():
    """Cria dados de teste no banco de dados."""
    db = SessionLocal()
    
    try:
        print("🌱 Criando dados de teste...")
        
        # Inicializar banco de dados (criar tabelas)
        print("\n  ✓ Inicializando banco de dados...")
        from core.database import init_db
        init_db()
        
        # Verificar se já existe
        nutricionista = db.query(Nutricionista).filter(
            Nutricionista.email == "teste@nutricionista.com"
        ).first()
        
        if not nutricionista:
            print("\n  ✓ Criando nutricionista de teste...")
            
            # Hash da senha
            senha_hash = AuthService.hash_password("senha123456")
            
            nutricionista = Nutricionista(
                nome="Dr. Silva",
                email="teste@nutricionista.com",
                senha_hash=senha_hash
            )
            db.add(nutricionista)
            db.flush()
            
            # Skip ConfiguracaoNutricionista for now due to schema issues
            # TODO: Fix ConfiguracaoNutricionista model
            # config = ConfiguracaoNutricionista(
            #     nutricionista_id=nutricionista.id,
            #     cor_primaria="#2e7d32",
            #     valor_consulta=150.00,
            #     link_agendamento="https://calendly.com/drsilva"
            # )
            # db.add(config)
            # db.flush()
            
            print(f"    Email: teste@nutricionista.com")
            print(f"    Senha: senha123456")
            print(f"    ID: {nutricionista.id}")
            
            # Criar clientes de teste
            print("\n  ✓ Criando clientes de teste...")
            
            clientes_dados = [
                {
                    "nome": "João Silva",
                    "idade": 30,
                    "altura": 1.80,
                    "objetivo": "Perder peso e ganhar massa muscular",
                },
                {
                    "nome": "Maria Santos",
                    "idade": 25,
                    "altura": 1.65,
                    "objetivo": "Ganhar definição muscular",
                },
                {
                    "nome": "Pedro Costa",
                    "idade": 45,
                    "altura": 1.75,
                    "objetivo": "Melhorar saúde e perder peso",
                }
            ]
            
            for dados in clientes_dados:
                cliente = Cliente(
                    nutricionista_id=nutricionista.id,
                    nome=dados["nome"],
                    idade=dados["idade"],
                    altura=dados["altura"],
                    objetivo=dados["objetivo"],
                )
                db.add(cliente)
                db.flush()
                print(f"    ✓ {dados['nome']} (ID: {cliente.id})")
            
            db.commit()
            
            print("\n" + "="*60)
            print("✅ Dados de teste criados com sucesso!")
            print("="*60)
            print(f"""
Credenciais de teste:
  Email: teste@nutricionista.com
  Senha: senha123456

Clientes criados:
  - João Silva
  - Maria Santos
  - Pedro Costa

Próximos passos:
  1. Inicie o backend: python main.py
  2. Inicie o frontend: cd frontend && npm run dev
  3. Faça login com as credenciais acima
  4. Execute o teste de integração: python test_integration.py
""")
            
        else:
            print(f"\n⚠️  Nutricionista de teste já existe!")
            print(f"   Email: {nutricionista.email}")
            print(f"   Senha: senha123456")
            
    except Exception as e:
        print(f"\n❌ Erro ao criar dados de teste: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    criar_dados_teste()
