"""Modelo de Observação."""
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models.cliente import Cliente  # noqa: F401


class Observacao(BaseModel):
    """
    Modelo de Observação.
    
    Armazena notas e observações do nutricionista sobre o cliente.
    """

    __tablename__ = "observacoes"

    # Foreign Key
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Campos
    texto: Mapped[str] = mapped_column(Text, nullable=False)

    # Relacionamento (usar strings para evitar circular imports)
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="observacoes",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_observacao_cliente_id", "cliente_id"),
    )

    def __repr__(self) -> str:
        return f"<Observacao(id={self.id}, cliente_id={self.cliente_id})>"
