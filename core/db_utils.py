"""Utilitários para operações com banco de dados."""
from typing import Optional, Type, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import inspect

T = TypeVar("T")


class DBHealthCheck:
    """Verificação de saúde do banco de dados."""
    
    @staticmethod
    def check_connection(db: Session) -> bool:
        """
        Verifica se a conexão com banco está ativa.
        
        Args:
            db: Sessão do banco
            
        Returns:
            bool: True se conexão está ativa, False caso contrário
        """
        try:
            db.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"❌ Erro ao verificar conexão com BD: {e}")
            return False


class DBTransaction:
    """Context manager para transações de banco de dados."""
    
    def __init__(self, db: Session):
        """
        Inicializa o gerenciador de transação.
        
        Args:
            db: Sessão do banco
        """
        self.db = db
    
    def __enter__(self):
        """Inicia transação."""
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit ou rollback baseado em exceção."""
        if exc_type is None:
            self.db.commit()
        else:
            self.db.rollback()
            print(f"❌ Transação revertida: {exc_val}")


class DBBulkOperations:
    """Operações em lote para otimizar performance."""
    
    @staticmethod
    def bulk_insert(db: Session, objects: list, batch_size: int = 1000) -> int:
        """
        Insere múltiplos objetos em lotes.
        
        Args:
            db: Sessão do banco
            objects: Lista de objetos para inserir
            batch_size: Tamanho de cada lote
            
        Returns:
            int: Total de objetos inseridos
        """
        total = 0
        for i in range(0, len(objects), batch_size):
            batch = objects[i : i + batch_size]
            db.add_all(batch)
            total += len(batch)
        db.commit()
        return total
    
    @staticmethod
    def bulk_delete(db: Session, query_result) -> int:
        """
        Deleta múltiplos objetos.
        
        Args:
            db: Sessão do banco
            query_result: Resultado de query.all()
            
        Returns:
            int: Total de objetos deletados
        """
        total = len(query_result)
        for obj in query_result:
            db.delete(obj)
        db.commit()
        return total


class DBSchema:
    """Utilitários para inspecionar schema do banco."""
    
    @staticmethod
    def get_table_columns(db: Session, model: Type[T]) -> dict:
        """
        Retorna informações sobre colunas de uma tabela.
        
        Args:
            db: Sessão do banco
            model: Modelo SQLAlchemy
            
        Returns:
            dict: Mapeamento de colunas e seus tipos
        """
        mapper = inspect(model)
        columns = {}
        for column in mapper.columns:
            columns[column.name] = str(column.type)
        return columns
    
    @staticmethod
    def get_all_tables(db: Session) -> list:
        """
        Retorna lista de todas as tabelas do banco.
        
        Args:
            db: Sessão do banco
            
        Returns:
            list: Nomes das tabelas
        """
        from sqlalchemy import inspect
        inspector = inspect(db.get_bind())
        return inspector.get_table_names()


class DBMigration:
    """Utilitários para verificação de migrations."""
    
    @staticmethod
    def check_migrations_needed() -> bool:
        """
        Verifica se há migrations pendentes.
        
        Returns:
            bool: True se há migrations a aplicar
        """
        # Esta função seria usada com Alembic
        # Implementação específica depende de como alembic está configurado
        from core.database import engine
        from models.base import Base
        
        inspector = inspect(engine)
        current_tables = set(inspector.get_table_names())
        expected_tables = set(Base.metadata.tables.keys())
        
        return current_tables != expected_tables


# Type hints para melhor suporte de IDE
__all__ = [
    "DBHealthCheck",
    "DBTransaction",
    "DBBulkOperations",
    "DBSchema",
    "DBMigration",
]
