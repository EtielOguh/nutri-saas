"""Script para testar configuração de banco de dados."""
import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa se os imports funcionam."""
    print("🧪 Testando imports...")
    try:
        from core.config import settings
        from core.database import engine, SessionLocal, get_db
        from models.base import Base, BaseModel
        from core.db_utils import DBHealthCheck
        print("✅ Imports OK\n")
        return True
    except Exception as e:
        print(f"❌ Erro em imports: {e}\n")
        return False


def test_config():
    """Testa configurações."""
    print("🧪 Testando configurações...")
    from core.config import settings
    
    print(f"   App: {settings.APP_NAME}")
    print(f"   Env: {settings.ENVIRONMENT}")
    print(f"   Debug: {settings.DEBUG}")
    print(f"   DB Host: {settings.DB_HOST}")
    print(f"   DB Name: {settings.DB_NAME}")
    print(f"   Pool Size: {settings.DB_POOL_SIZE}")
    
    db_url = settings.get_database_url
    # Mascarar senha
    masked_url = db_url.replace(settings.DB_PASSWORD, "***")
    print(f"   DB URL: {masked_url}")
    print("✅ Configurações OK\n")
    return True


def test_engine():
    """Testa engine do SQLAlchemy."""
    print("🧪 Testando engine...")
    from core.database import engine
    from sqlalchemy import text
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"   Conexão test: SELECT 1 = {value}")
        print("✅ Engine OK\n")
        return True
    except Exception as e:
        print(f"❌ Erro engine: {e}\n")
        return False


def test_session():
    """Testa SessionLocal."""
    print("🧪 Testando SessionLocal...")
    from core.database import SessionLocal
    
    try:
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ SessionLocal OK\n")
        return True
    except Exception as e:
        print(f"❌ Erro SessionLocal: {e}\n")
        return False


def test_models():
    """Testa modelos base."""
    print("🧪 Testando modelos...")
    from models.base import Base, BaseModel
    from sqlalchemy.orm import DeclarativeBase
    
    if not issubclass(Base, DeclarativeBase):
        print("❌ Base não é DeclarativeBase")
        return False
    
    if not hasattr(BaseModel, '__abstract__'):
        print("❌ BaseModel não tem __abstract__")
        return False
    
    print("✅ Modelos OK\n")
    return True


def test_db_utils():
    """Testa utilitários de DB."""
    print("🧪 Testando utilitários...")
    from core.db_utils import (
        DBHealthCheck, DBTransaction, DBBulkOperations,
        DBSchema, DBMigration
    )
    print("✅ Utilitários OK\n")
    return True


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("🧪 TESTE DE CONFIGURAÇÃO DO BANCO DE DADOS")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_config,
        test_engine,
        test_session,
        test_models,
        test_db_utils,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"❌ Erro em {test.__name__}: {e}\n")
            results.append((test.__name__, False))
    
    # Resumo
    print("="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Tudo funcionando! Banco de dados está pronto para uso.\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam\n")
        return 1


if __name__ == "__main__":
    exit(main())
