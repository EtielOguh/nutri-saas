"""
Exemplo de serviço de usuário.

Este é um arquivo de exemplo mostrando como implementar um serviço
que herda de BaseService e adiciona lógica específica de negócio.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user_example import User
from schemas.user_example import UserCreate, UserUpdate, UserResponse
from services.base import BaseService


class UserService(BaseService[User, UserCreate]):
    """Serviço de gerenciamento de usuários."""

    def __init__(self, db: Session):
        """Inicializa o serviço com o modelo User."""
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email."""
        return self.db.query(self.model).filter(self.model.email == email).first()

    def create_user(self, user_data: UserCreate) -> User:
        """Cria um novo usuário com validações."""
        # Verificar se email já existe
        if self.get_by_email(user_data.email):
            raise ValueError(f"Email {user_data.email} já está registrado")

        # Aqui você implementaria a hash da senha
        # user_data.password = hash_password(user_data.password)

        return self.create(user_data)

    def get_active_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """Busca apenas usuários ativos."""
        return (
            self.db.query(self.model)
            .filter(self.model.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Desativa um usuário."""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            self.db.refresh(user)
        return user

    def activate_user(self, user_id: int) -> Optional[User]:
        """Ativa um usuário."""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = True
            self.db.commit()
            self.db.refresh(user)
        return user
