"""Script para testar modelos SQLAlchemy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa imports dos modelos."""
    print("🧪 Testando imports dos modelos...")
    try:
        from models import (
            Base,
            BaseModel,
            Nutricionista,
            ConfiguracaoNutricionista,
            Cliente,
            Medicao,
            Observacao,
            TokenAcessoCliente,
            DocumentoPDF,
        )
        print("✅ Todos os modelos importados com sucesso\n")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar modelos: {e}\n")
        return False


def test_model_structure():
    """Testa estrutura dos modelos."""
    print("🧪 Testando estrutura dos modelos...")
    from models import (
        Nutricionista,
        ConfiguracaoNutricionista,
        Cliente,
        Medicao,
        Observacao,
        TokenAcessoCliente,
        DocumentoPDF,
    )

    models_to_check = [
        ("Nutricionista", Nutricionista, ["nome", "email", "senha_hash"]),
        ("ConfiguracaoNutricionista", ConfiguracaoNutricionista, ["nutricionista_id", "valor_consulta"]),
        ("Cliente", Cliente, ["nutricionista_id", "nome", "idade", "altura"]),
        ("Medicao", Medicao, ["cliente_id", "peso", "data_medicao"]),
        ("Observacao", Observacao, ["cliente_id", "texto"]),
        ("TokenAcessoCliente", TokenAcessoCliente, ["cliente_id", "token_unico"]),
        ("DocumentoPDF", DocumentoPDF, ["cliente_id", "url_pdf"]),
    ]

    for model_name, model_class, expected_columns in models_to_check:
        mapper = model_class.__mapper__
        columns = [col.name for col in mapper.columns]
        
        # Verificar se colunas esperadas existem
        missing = set(expected_columns) - set(columns)
        if missing:
            print(f"❌ {model_name} faltam colunas: {missing}")
            return False
        
        print(f"✅ {model_name}: {len(columns)} colunas - {columns}")

    print()
    return True


def test_relationships():
    """Testa relacionamentos."""
    print("🧪 Testando relacionamentos...")
    from models import (
        Nutricionista,
        Cliente,
        Medicao,
        Observacao,
        TokenAcessoCliente,
        DocumentoPDF,
    )

    relationships_check = [
        ("Nutricionista", Nutricionista, ["clientes", "configuracao"]),
        ("Cliente", Cliente, ["nutricionista", "medicoes", "observacoes", "token_acesso", "documentos"]),
        ("Medicao", Medicao, ["cliente"]),
        ("Observacao", Observacao, ["cliente"]),
        ("TokenAcessoCliente", TokenAcessoCliente, ["cliente"]),
        ("DocumentoPDF", DocumentoPDF, ["cliente"]),
    ]

    for model_name, model_class, expected_relationships in relationships_check:
        mapper = model_class.__mapper__
        relationships = [rel.key for rel in mapper.relationships]
        
        missing = set(expected_relationships) - set(relationships)
        if missing:
            print(f"❌ {model_name} faltam relacionamentos: {missing}")
            return False
        
        print(f"✅ {model_name}: {len(relationships)} relacionamentos - {relationships}")

    print()
    return True


def test_foreign_keys():
    """Testa foreign keys."""
    print("🧪 Testando foreign keys...")
    from models import Cliente, Medicao, Observacao, TokenAcessoCliente, DocumentoPDF
    from sqlalchemy import inspect

    fk_check = [
        ("Cliente", Cliente, "nutricionista_id"),
        ("Medicao", Medicao, "cliente_id"),
        ("Observacao", Observacao, "cliente_id"),
        ("TokenAcessoCliente", TokenAcessoCliente, "cliente_id"),
        ("DocumentoPDF", DocumentoPDF, "cliente_id"),
    ]

    for model_name, model_class, expected_fk in fk_check:
        mapper = inspect(model_class)
        fks = []
        for col in mapper.columns:
            if col.foreign_keys:
                fks.append(col.name)
        
        if expected_fk not in fks:
            print(f"❌ {model_name} falta FK: {expected_fk}")
            return False
        
        print(f"✅ {model_name}: FK {expected_fk} -> {fks}")

    print()
    return True


def test_table_creation():
    """Testa criação de tabelas."""
    print("🧪 Testando criação de tabelas...")
    from models import Base
    from core.database import engine
    
    try:
        # Não vamos realmente criar as tabelas aqui, mas verificar metadata
        tables = list(Base.metadata.tables.keys())
        print(f"✅ {len(tables)} tabelas no metadata: {sorted(tables)}\n")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}\n")
        return False


def main():
    """Executa todos os testes."""
    print("\n" + "="*70)
    print("🧪 TESTE DE MODELOS SQLAlchemy")
    print("="*70 + "\n")

    tests = [
        test_imports,
        test_model_structure,
        test_relationships,
        test_foreign_keys,
        test_table_creation,
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
    print("="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print(f"\n{passed}/{total} testes passaram")

    if passed == total:
        print("\n🎉 Todos os modelos estão corretos e prontos para uso!\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam\n")
        return 1


if __name__ == "__main__":
    exit(main())
