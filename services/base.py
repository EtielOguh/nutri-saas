"""Serviço base com operações CRUD genéricas."""
from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")
SchemaT = TypeVar("SchemaT")


class BaseService(Generic[T, SchemaT]):
    """
    Serviço base genérico para operações CRUD.
    
    Tipos genéricos:
        T: Tipo do modelo SQLAlchemy
        SchemaT: Tipo do schema Pydantic
    """

    def __init__(self, model: Type[T], db: Session):
        """
        Inicializa o serviço.
        
        Args:
            model: Classe do modelo SQLAlchemy
            db: Sessão do banco de dados
        """
        self.model = model
        self.db = db

    def get_by_id(self, item_id: int) -> Optional[T]:
        """Busca um item por ID."""
        return self.db.query(self.model).filter(self.model.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        """Busca todos os itens com paginação."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_count(self) -> int:
        """Retorna o total de itens."""
        return self.db.query(self.model).count()

    def create(self, obj_in: SchemaT) -> T:
        """Cria um novo item."""
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, item_id: int, obj_in: SchemaT) -> Optional[T]:
        """Atualiza um item existente."""
        db_obj = self.get_by_id(item_id)
        if not db_obj:
            return None
        
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, item_id: int) -> bool:
        """Deleta um item."""
        db_obj = self.get_by_id(item_id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
