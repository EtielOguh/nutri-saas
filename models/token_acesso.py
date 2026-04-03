"""Modelo de Token de Acesso do Cliente."""
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models.cliente import Cliente  # noqa: F401


class TokenAcessoCliente(BaseModel):
    """
    Modelo de Token de Acesso.
    
    Armazena tokens únicos para acesso restrito de clientes ao sistema.
    Relação 1:1 com Cliente.
    """

    __tablename__ = "tokens_acesso_cliente"

    # Foreign Key (uselist=False garante 1:1)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,  # Garante 1:1
    )

    # Campos
    token_unico: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    # Relacionamento (usar strings para evitar circular imports)
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="token_acesso",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_token_cliente_id", "cliente_id"),
        Index("idx_token_unico", "token_unico"),
    )

    def __repr__(self) -> str:
        return f"<TokenAcessoCliente(cliente_id={self.cliente_id})>"
